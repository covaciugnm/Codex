"""Package the additional iFLYTEK analysis and toolchain; run with Linux Python.

Only allowlisted project directories are read. Signing material, device logs,
operating-system images, Git internals and build caches are never inputs.
Each ZIP includes a SHA-256 inventory of its uncompressed files.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

EXCLUDED = {".git", "__pycache__", ".pytest_cache"}


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def archive(target, roots, provenance):
    inventory = []
    names = set()
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as out:
        for source, prefix in roots:
            if not source.exists():
                raise FileNotFoundError(source)
            files = [source] if source.is_file() else sorted(source.rglob("*"))
            for item in files:
                relative = Path(item.name) if source.is_file() else item.relative_to(source)
                if any(part in EXCLUDED for part in relative.parts):
                    continue
                if item.is_symlink():
                    raise ValueError(f"Symlink needs explicit handling: {item}")
                if not item.is_file():
                    continue
                name = prefix + ("/" + relative.as_posix() if not source.is_file() else "")
                if name in names:
                    raise ValueError(f"Duplicate archive entry: {name}")
                names.add(name)
                digest = sha(item)
                inventory.append({"path": name, "bytes": item.stat().st_size, "sha256": digest})
                out.write(item, name, compress_type=zipfile.ZIP_STORED if item.suffix in {".zip", ".jar"} else zipfile.ZIP_DEFLATED)
        out.writestr("CONTENTS-SHA256.json", json.dumps({"schemaVersion": 1, "provenance": provenance, "files": inventory}, indent=2) + "\n")
    # Validate both ZIP integrity and the full uncompressed inventory.
    with zipfile.ZipFile(target) as check:
        for entry in inventory:
            with check.open(entry["path"]) as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            assert digest == entry["sha256"], entry["path"]
    result = {"name": target.name, "bytes": target.stat().st_size, "sha256": sha(target),
              "files": len(inventory), "uncompressedBytes": sum(x["bytes"] for x in inventory)}
    target.with_suffix(target.suffix + ".sha256").write_text(result["sha256"] + "  " + target.name + "\n")
    print(json.dumps(result), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    for name in ("project", "analysis", "blutter", "windows-tools", "patch-work"):
        parser.add_argument("--" + name, required=True, type=Path)
    args = parser.parse_args()
    dist = args.project / "dist"
    dist.mkdir(exist_ok=True)
    variant = args.project / "variants/romania-40"
    results = []
    results.append(archive(dist / "iflytek-1.0.3899-aot-analysis.zip", [
        (args.analysis, "analysis-original"),
        (args.patch_work / "libapp.so", "romania40/libapp.so"),
        *[(args.patch_work / "patch" / name, "romania40/patch/" + name)
          for name in ("patch.elf", "patch.o", "patch.ld")],
        *[(variant / "reports" / name, "romania40/patch/" + name)
          for name in ("native-patch.json", "native-tests.json", "patch-disassembly.txt")],
    ], {
        "inputApkSha256": "73170cdc5c3331cd6055607015c04ed8e0a314f4c0bd2fd4651e2b732d1b3da2",
        "originalLibrarySha256": "17745c9106afa9fbdf3077ea2d0771437b1435371aec73d8ad13ef5e71ad2f06",
        "patchedLibrarySha256": "804d43836a21f5ac3e8946f9e7bd78cf7ebac472b67922684c7953acf0046d8e",
        "dartVersion": "3.10.9", "blutterCommit": "4a60ac648bf448c5a7596437243bcd0b9376fdf0",
        "limits": "AOT analysis and binary patch; not recovered original Dart source. Device testing pending."
    }))
    tool_roots = [(args.windows_tools / name, "windows-downloads/" + name) for name in
                  ("apktool_3.0.3.jar", "build-tools_r36_windows.zip", "platform-tools_r37.0.1-win.zip")]
    tool_roots.append((args.windows_tools / "pydeps", "windows-python-deps"))
    tool_roots.extend((args.blutter / name, "linux-blutter/" + name) for name in
                      ("LICENSE", "README.md", "blutter.py", "dartvm_fetch_build.py", "extract_dart_info.py",
                       "blutter", "scripts", "bin", "dartsdk", "packages"))
    results.append(archive(dist / "iflytek-20261031-analysis-toolchain.zip", tool_roots, {
        "blutterRepository": "https://github.com/worawit/blutter",
        "blutterCommit": "4a60ac648bf448c5a7596437243bcd0b9376fdf0",
        "blutterLocalChange": "Limit Ninja to -j4 in blutter.py and dartvm_fetch_build.py; no C++ changes.",
        "linuxEnvironment": "Ubuntu 24.04.5 x86_64; GNU binutils AArch64 2.42, GCC 13, CMake, Ninja, ICU and Capstone development packages.",
        "pythonPackages": {"capstone": "5.0.9", "pyelftools": "0.33", "unicorn": "2.1.4"},
        "limits": "Windows archives/dependencies and Linux Blutter are separate. No OS image, JDK, signing key, credentials or device logs."
    }))
    (args.project / "reports/handoff-archives.json").write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
