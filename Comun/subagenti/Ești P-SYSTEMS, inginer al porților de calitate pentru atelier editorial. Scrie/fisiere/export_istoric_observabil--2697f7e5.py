"""Observable-history exporter r03: TEST staging, no raw-log export.
Selection/redaction rules are unchanged from r02. Writes are confined to a fresh
capture under the supplied workshop; source logs are read-only.
"""
from pathlib import Path, PureWindowsPath
from datetime import datetime, timezone
from collections import Counter
import argparse
import hashlib
import json
import os
import re
import stat
import uuid

# Integrated location: ROOT/06_REGISTRU/script.py. Staging requires an explicit root.
_SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = _SCRIPT_DIR.parent if _SCRIPT_DIR.name == "06_REGISTRU" else None
START = "2026-09-24T00:35:17.566Z"
CAPTURE_PARTS = ("06_REGISTRU", "ISTORIC", "EXPORT_OBSERVABIL")
RESERVED = {"con", "prn", "aux", "nul", "clock$", "conin$", "conout$",
            *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def complete_prefix(raw):
    """Return only existing bytes through the last LF; no complete line => b''."""
    return raw[:raw.rfind(b"\n") + 1]


def safe_component(value, label):
    minimum = 1 if label == "round" else 0  # Preserve the existing 2..61 round length.
    if (not isinstance(value, str)
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{" + str(minimum) + r",60}", value)
            or value.casefold() in RESERVED
            or (label == "role" and value.casefold() == "index")):
        raise ValueError(f"Unsafe {label}")
    return value


def plain_directory(path):
    info = path.lstat()
    if (stat.S_ISLNK(info.st_mode)
            or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
        raise ValueError(f"Symlink/reparse directory refused: {path}")
    if not stat.S_ISDIR(info.st_mode):
        raise ValueError(f"Not a directory: {path}")


def checked_root(root=None):
    root = ROOT if root is None else root
    if root is None:
        raise ValueError("--root is required when running the staging copy")
    path = Path(root).absolute()
    if ".." in path.parts or path == Path(path.anchor):
        raise ValueError("Unsafe workshop root")
    # Check lexical ancestors BEFORE resolve, so resolution cannot hide a junction.
    for parent in [*reversed(path.parents), path]:
        plain_directory(parent)
    if path.resolve(strict=True) != path:
        raise ValueError("Aliased workshop root")
    return path


def config_path(relative, root=None):
    root = checked_root(root)
    if not isinstance(relative, str) or not relative:
        raise ValueError("Unsafe config path")
    win = PureWindowsPath(relative)
    parts = relative.replace("\\", "/").split("/")
    if (win.drive or win.root or relative.startswith("/")
            or any(not p or p in (".", "..") or ":" in p for p in parts)):
        raise ValueError("Config outside workshop or unsafe relative path")
    candidate = root.joinpath(*parts).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError("Config outside workshop")
    return candidate


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate configuration key: {key}")
        result[key] = value
    return result


def validate_output_names(names):
    """Reserve/check the full namespace, including both index files."""
    seen = set()
    for name in names:
        if (not isinstance(name, str)
                or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,60}\.(?:md|jsonl|json|sha256)", name)
                or name.split(".", 1)[0].casefold() in RESERVED):
            raise ValueError("Unsafe output name")
        folded = name.casefold()
        if folded in seen:
            raise ValueError(f"Output collision: {name}")
        seen.add(folded)


def prepare_sources(config):
    if not isinstance(config, list):
        raise ValueError("Sources must be a list")
    prepared, roles, agents, identities, paths = [], set(), set(), set(), set()
    names = ["index.json", "index.sha256"]
    # Validate the entire configuration before reading logs or creating output.
    for source in config:
        if not isinstance(source, dict) or not {"role", "agent_id", "path"} <= source.keys():
            raise ValueError("Each source needs role, agent_id and path")
        role = safe_component(source["role"], "role")
        if role.casefold() in roles:
            raise ValueError("Duplicate/aliased role")
        roles.add(role.casefold())
        agent = source["agent_id"]
        try:
            parsed = uuid.UUID(agent)
        except (ValueError, AttributeError, TypeError) as exc:
            raise ValueError("Invalid source agent_id") from exc
        if str(parsed) != agent or not parsed.int or agent in agents:
            raise ValueError("Duplicate or noncanonical source agent_id")
        agents.add(agent)
        if not isinstance(source["path"], str) or not source["path"]:
            raise ValueError("Invalid source path")
        path = Path(source["path"])
        if not path.is_absolute() or not path.name.endswith(agent + ".jsonl"):
            raise ValueError("Identity/path mismatch")
        resolved = path.resolve(strict=True)
        info = resolved.stat()
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("Source must be a regular file")
        identity = (info.st_dev, info.st_ino)
        if resolved in paths or identity in identities:
            raise ValueError("Duplicate/aliased source path")
        paths.add(resolved)
        identities.add(identity)
        names.extend([role + ".jsonl", role + ".md"])
        prepared.append((source, path))
    validate_output_names(names)
    return prepared


def checked_tree(root, parts, create=False):
    root = checked_root(root)
    current = root
    for part in parts:
        current = current / part
        try:
            plain_directory(current)
        except FileNotFoundError:
            if not create:
                # No later component can exist through a nonexistent parent.
                return root.joinpath(*parts)
            current.mkdir()  # Never parents=True; each component is checked separately.
            plain_directory(current)
        if not current.resolve(strict=True).is_relative_to(root):
            raise ValueError("Capture parent escapes workshop")
    return current


def require_absent(parent, name):
    # Case-insensitive uniqueness also on case-sensitive filesystems. Includes
    # dangling symlinks, files, directories and names reserved for the index.
    if any(entry.name.casefold() == name.casefold() for entry in parent.iterdir()):
        raise ValueError(f"Existing capture/output; no overwrite: {name}")


def destination(root, round_id, create=False):
    safe_component(round_id, "round")
    parent = checked_tree(root, CAPTURE_PARTS, create=create)
    if parent.exists():
        plain_directory(parent)
        require_absent(parent, round_id)
    dest = parent / round_id
    if create:
        dest.mkdir()
        checked_tree(root, (*CAPTURE_PARTS, round_id))
    return dest


def write_new(root, dest, name, data):
    validate_output_names([name])
    # Recheck parents immediately before each exclusive file creation.
    checked = checked_tree(root, (*CAPTURE_PARTS, dest.name))
    if checked != dest:
        raise ValueError("Wrong capture directory")
    require_absent(dest, name)
    target = dest / name
    if target.parent != dest or not target.resolve().is_relative_to(dest):
        raise ValueError("Output escapes capture")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(target, flags, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(data)
    checked_tree(root, (*CAPTURE_PARTS, dest.name))


def clean_value(v):
    if isinstance(v,dict):
        return {k:clean_value(x) for k,x in v.items() if k not in
          {"internal_chat_message_metadata_passthrough","encrypted_content","reasoning","analysis","system_prompt","developer_instructions"}}
    if isinstance(v,list):return [clean_value(x) for x in v]
    return v
def redact(v):
    encoded=json.dumps(clean_value(v),ensure_ascii=False)
    count=0
    for pat in [r"\bsk-[A-Za-z0-9_-]{20,}",r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{20,}"]:
        encoded,n=re.subn(pat,"[SECRET_REDACTED]",encoded);count+=n
    return json.loads(encoded),count
def select(payload):
    kind=payload.get("type")
    if kind=="message":
        role=payload.get("role")
        phase=payload.get("phase")
        channel=payload.get("channel")
        if role not in {"user","assistant"}:return None
        if role=="assistant" and phase not in {"commentary","final_answer"} and channel not in {"commentary","final"}:return None
        content=[]
        for c in payload.get("content",[]):
            if c.get("type") in {"input_text","output_text","text"}:
                content.append({"type":c["type"],"text":c.get("text","")})
            else:
                content.append({"type":c.get("type"),"note":"Media omitted here; original task artifacts remain separate."})
        return {"type":"message","role":role,"phase":phase,"channel":channel,"content":content}
    if kind in {"function_call","custom_tool_call"}:
        return {k:payload[k] for k in ("type","call_id","name","arguments","input","status") if k in payload}
    if kind in {"function_call_output","custom_tool_call_output"}:
        return {k:payload[k] for k in ("type","call_id","output") if k in payload}
    return None

def export_capture(root, round_id, sources="06_REGISTRU/surse_export_istoric.json"):
    root = checked_root(root)
    destination(root, round_id)  # Preflight without creating a capture.
    config = json.loads(config_path(sources, root).read_text(encoding="utf-8"),
                        object_pairs_hook=no_duplicate_keys)
    scoped_sources = prepare_sources(config)
    prepared = []
    entries = []
    for source, path in scoped_sources:
        raw = complete_prefix(path.read_bytes())
        selected = []
        omitted = Counter()
        messages = []
        redactions = 0
        for line_no, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                continue
            item = json.loads(line)
            if str(item.get("timestamp", "")) < START:
                continue
            if item.get("type") != "response_item":
                omitted[item.get("type", "unknown")] += 1
                continue
            p = item.get("payload", {})
            record = select(p)
            if record is None:
                omitted["response_item:" + str(p.get("type")) + ":" + str(p.get("role", ""))] += 1
                continue
            record, n = redact(record)
            redactions += n
            rec = {"timestamp": item.get("timestamp"), "source_line": line_no, **record}
            selected.append(rec)
            if record["type"] == "message":
                text = "\n".join(c.get("text", "") for c in record["content"] if "text" in c)
                messages.append(f"## {item.get('timestamp')} — {record['role']} — ligne {line_no}\n\n{text}\n")
        encoded = ("\n".join(json.dumps(s, ensure_ascii=False) for s in selected) + "\n").encode("utf-8")
        readable = ("# Observable messages / " + source["role"] +
                    "\n\nRecovered from explicitly scoped task log. Original event timestamps; recovery is later. "
                    "Excludes reasoning, platform instructions and raw hidden metadata.\n\n" +
                    "\n".join(messages)).encode("utf-8")
        for ext, data in [("jsonl", encoded), ("md", readable)]:
            prepared.append((source["role"] + "." + ext, data))
        entries.append({**source, "source_prefix_bytes": len(raw), "source_prefix_sha256": digest(raw),
                        "captured_records": len(selected), "messages": len(messages), "redactions": redactions,
                        "first_event": selected[0]["timestamp"] if selected else None,
                        "last_event": selected[-1]["timestamp"] if selected else None,
                        "omitted_categories": dict(omitted),
                        "output": {"path": source["role"] + ".jsonl", "sha256": digest(encoded), "bytes": len(encoded)},
                        "readable_messages": {"path": source["role"] + ".md", "sha256": digest(readable), "bytes": len(readable)}})
    index = {"created_at": datetime.now(timezone.utc).isoformat(), "start_inclusive": START,
             "scope": "Only these nine task logs, this editorial workshop; not prior strategy turns.",
             "limits": ["Recovery from locally available log, not an external certified timestamp.",
                        "Captured prefix per source; later events require a new capture.",
                        "Raw logs, reasoning/encrypted content, system/developer messages and platform internal metadata are never copied.",
                        "Assistant messages without explicit public phase/channel are conservatively omitted and counted; inspect coverage before claiming completeness.",
                        "Primary tool output can already be truncated by the original tool; export does not recreate missing output.",
                        "Secrets matching known token patterns are redacted and counted; this is not a universal secret detector.",
                        "Readable MD contains message text only; JSONL also contains observable tool calls/results.",
                        "No source log or previous capture is changed."],
             "sources": entries}
    data = (json.dumps(index, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    prepared.extend([("index.json", data), ("index.sha256", (digest(data) + "\n").encode("ascii"))])
    validate_output_names([name for name, _ in prepared])
    dest = destination(root, round_id, create=True)
    for name, payload in prepared:
        write_new(root, dest, name, payload)
    return {"capture": str(dest), "sources": len(entries),
            "records": sum(e["captured_records"] for e in entries),
            "messages": sum(e["messages"] for e in entries),
            "index_sha256": digest(data), "source_logs_modified": False}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--round", required=True)
    parser.add_argument("--sources", default="06_REGISTRU/surse_export_istoric.json")
    parser.add_argument("--root", help="Workshop root; required for an unintegrated staging copy")
    args = parser.parse_args(argv)
    try:
        result = export_capture(args.root, args.round, args.sources)
    except (ValueError, OSError, RuntimeError) as exc:
        parser.exit(2, f"Export refused: {exc}\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()

