"""TEST only: original 17 cases plus r03 end-to-end/adversarial regressions.
Every written file, including synthetic sources outside the synthetic ROOT,
is under a validated TemporaryDirectory. No real session logs are opened.
"""
import contextlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

import export_istoric_observabil as exporter
from export_istoric_observabil import select, redact, config_path


class SandboxFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="P-SYSTEMS-export-r03-TEST-")
        self.sandbox = Path(self.temp.name).resolve(strict=True)
        self.root = self.sandbox / "ROOT"
        self.outside = self.sandbox / "OUTSIDE_ROOT"
        self.links = []
        self.root.mkdir()
        self.outside.mkdir()
        (self.outside / "sentinel.txt").write_bytes(b"TEST sentinel unchanged")
        self.sources = []
        self.addCleanup(self.safe_cleanup)
        self.add_source()
        self.config = self.root / "06_REGISTRU/surse_export_istoric.json"
        self.save_config()

    def bounded(self, path):
        path = Path(path).absolute()
        self.assertNotEqual(path, self.sandbox)
        self.assertTrue(path.is_relative_to(self.sandbox), path)
        self.assertTrue(path.resolve().is_relative_to(self.sandbox), path)
        return path

    def safe_cleanup(self):
        # Validate the exact TemporaryDirectory and every link target BEFORE cleanup.
        self.assertEqual(Path(self.temp.name).absolute(), self.sandbox)
        self.assertEqual(self.sandbox.resolve(), self.sandbox)
        for link in reversed(self.links):
            self.bounded(link)
            if os.path.lexists(link):
                info = link.lstat()
                self.assertTrue(stat.S_ISLNK(info.st_mode) or
                                getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
                if link.is_symlink():
                    link.unlink()
                else:
                    link.rmdir()  # Windows junction itself, never a recursive target delete.
        for path in (self.root, self.outside, self.sandbox / "logs"):
            self.bounded(path)
        self.temp.cleanup()

    def event(self, text="TEST public", **payload):
        item = {"type": "message", "role": "assistant", "phase": "final_answer",
                "channel": "final", "content": [{"type": "output_text", "text": text}]}
        item.update(payload)
        return {"timestamp": "2026-09-24T01:00:00Z", "type": "response_item", "payload": item}

    def encoded(self, event=None):
        return json.dumps(event or self.event(), ensure_ascii=False).encode("utf-8")

    def add_source(self, role="A-TEST", raw=None, agent=None):
        agent = agent or str(uuid.UUID(int=len(self.sources) + 1))
        path = self.bounded(self.sandbox / "logs" / ("synthetic-" + agent + ".jsonl"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(self.encoded() + b"\n" if raw is None else raw)
        self.sources.append({"role": role, "agent_id": agent, "path": str(path)})
        return path

    def save_config(self):
        self.bounded(self.config)
        self.config.parent.mkdir(parents=True, exist_ok=True)
        self.config.write_text(json.dumps(self.sources), encoding="utf-8")

    def source(self):
        return self.bounded(Path(self.sources[0]["path"]))

    def capture(self, round_id="round-TEST", root=None):
        self.save_config()
        return exporter.export_capture(self.root if root is None else root, round_id)

    def checked_capture(self, raw, expected_records):
        self.source().write_bytes(raw)
        before = self.source().read_bytes()
        result = self.capture()
        dest = self.bounded(Path(result["capture"]))
        self.assertTrue(dest.is_relative_to(self.root))
        index_raw = (dest / "index.json").read_bytes()
        index = json.loads(index_raw)
        self.assertEqual((dest / "index.sha256").read_text("ascii").strip(), exporter.digest(index_raw))
        self.assertEqual(result["index_sha256"], exporter.digest(index_raw))
        entry = index["sources"][0]
        expected = raw[:raw.rfind(b"\n") + 1]
        self.assertEqual(entry["source_prefix_bytes"], len(expected))
        self.assertLessEqual(entry["source_prefix_bytes"], len(raw))
        self.assertEqual(entry["source_prefix_sha256"], exporter.digest(raw[:len(expected)]))
        self.assertEqual(entry["captured_records"], expected_records)
        for key in ("output", "readable_messages"):
            reference = entry[key]
            path = self.bounded(dest / reference["path"])
            data = path.read_bytes()
            self.assertEqual(len(data), reference["bytes"])
            self.assertEqual(exporter.digest(data), reference["sha256"])
        self.assertEqual(self.source().read_bytes(), before)
        self.assertFalse(result["source_logs_modified"])
        return dest, index

    def no_external_writes(self):
        self.assertEqual(sorted(p.name for p in self.outside.iterdir()), ["sentinel.txt"])
        self.assertEqual((self.outside / "sentinel.txt").read_bytes(), b"TEST sentinel unchanged")

    def link(self, path, target, junction=False):
        path, target = self.bounded(path), self.bounded(target)
        path.parent.mkdir(parents=True, exist_ok=True)
        if junction:
            if os.name != "nt":
                self.skipTest("Windows junction requires Windows")
            process = subprocess.run(["cmd", "/c", "mklink", "/J", str(path), str(target)],
                                     capture_output=True, text=True, check=False,
                                     cwd=self.sandbox)
            if process.returncode:
                self.skipTest("OS does not permit junction: " + process.stderr.strip())
        else:
            try:
                path.symlink_to(target, target_is_directory=target.is_dir())
            except OSError as exc:
                self.skipTest(f"OS does not permit symlink: {exc}")
        self.links.append(path)
        return path


class ObservableExportTests(SandboxFixture):
    def test_config_inside_workshop(self):
        self.assertEqual(config_path("06_REGISTRU/config-new.json", self.root),self.root/"06_REGISTRU/config-new.json")
    def test_config_parent_escape_rejected(self):
        with self.assertRaises(ValueError):config_path("../outside.json", self.root)
    def test_absolute_external_config_rejected(self):
        with self.assertRaises(ValueError):config_path(str(self.root.parent/"outside.json"), self.root)
    def test_reasoning_event_excluded(self):
        self.assertIsNone(select({"type":"reasoning","summary":"hidden"}))
    def test_system_message_excluded(self):
        self.assertIsNone(select({"type":"message","role":"system","content":[]}))
    def test_developer_message_excluded(self):
        self.assertIsNone(select({"type":"message","role":"developer","content":[]}))
    def test_analysis_message_excluded(self):
        self.assertIsNone(select({"type":"message","role":"assistant","channel":"analysis","content":[]}))
    def test_unknown_assistant_phase_excluded(self):
        self.assertIsNone(select({"type":"message","role":"assistant","content":[]}))
    def test_commentary_message_included(self):
        self.assertEqual(select({"type":"message","role":"assistant","phase":"commentary","content":[{"type":"output_text","text":"status"}]})["content"][0]["text"],"status")
    def test_final_message_included(self):
        self.assertEqual(select({"type":"message","role":"assistant","phase":"final_answer","content":[]})["phase"],"final_answer")
    def test_user_text_preserved(self):
        self.assertEqual(select({"type":"message","role":"user","content":[{"type":"input_text","text":"cerință exactă"}]})["content"][0]["text"],"cerință exactă")
    def test_internal_message_metadata_omitted(self):
        self.assertNotIn("internal_chat_message_metadata_passthrough",select({"type":"message","role":"user","content":[],"internal_chat_message_metadata_passthrough":"hidden"}))
    def test_tool_call_allowlist(self):
        d=select({"type":"custom_tool_call","name":"functions.exec","call_id":"c1","input":"public code","encrypted_content":"hidden"})
        self.assertEqual(d,{"type":"custom_tool_call","call_id":"c1","name":"functions.exec","input":"public code"})
    def test_tool_result_allowlist(self):
        d=select({"type":"custom_tool_call_output","call_id":"c1","output":"public result","internal_chat_message_metadata_passthrough":"hidden"})
        self.assertEqual(d,{"type":"custom_tool_call_output","call_id":"c1","output":"public result"})
    def test_secret_patterns_redacted(self):
        d,n=redact({"output":"Bearer "+"A"*25+" "+"sk-"+"B"*25})
        self.assertEqual(n,2);self.assertNotIn("A"*25,d["output"]);self.assertNotIn("B"*25,d["output"])
    def test_nested_private_keys_removed(self):
        d,n=redact({"output":{"encrypted_content":"hidden","reasoning":"hidden","public":"kept"}})
        self.assertEqual(d,{"output":{"public":"kept"}})
    def test_media_not_copied_as_hidden_payload(self):
        d=select({"type":"message","role":"user","content":[{"type":"image","data":"not copied"}]})
        self.assertNotIn("data",d["content"][0])

class PrefixRegressionTests(SandboxFixture):
    def test_F05_H04_empty_source_has_zero_prefix(self):
        self.checked_capture(b"", 0)

    def test_F05_H03_complete_JSON_without_LF_is_not_a_complete_line(self):
        self.checked_capture(self.encoded(), 0)

    def test_F05_first_partial_line_has_zero_prefix(self):
        self.checked_capture(b'{"unfinished', 0)

    def test_F05_H01_LF_positive_control(self):
        self.checked_capture(self.encoded() + b"\n", 1)

    def test_F05_CRLF_positive_control_preserves_CR_bytes(self):
        self.checked_capture(self.encoded() + b"\r\n", 1)

    def test_F05_H02_incomplete_tail_after_LF_is_excluded(self):
        self.checked_capture(self.encoded() + b'\n{"unfinished', 1)

    def test_F05_CRLF_with_incomplete_UTF8_tail(self):
        self.checked_capture(self.encoded(self.event("TEST română")) + b"\r\n\xe2\x82", 1)

    def test_F05_CR_without_LF_is_not_completed(self):
        self.checked_capture(self.encoded() + b"\r", 0)

    def test_F05_blank_complete_lines_are_retained_in_prefix(self):
        self.checked_capture(b"\n\r\n", 0)

    def test_F05_multiple_records_final_unterminated_record_excluded(self):
        self.checked_capture(self.encoded() + b"\n" + self.encoded() + b"\n" + self.encoded(), 2)

    def test_F05_prefix_property_over_arbitrary_bytes(self):
        for raw in (b"", b"x", b"\r", b"\n", b"\x00\n\xff", bytes(range(256)),
                    b"\n\npartial", b"\ncomplete\r\nlast", b"\r\n"):
            with self.subTest(raw_length=len(raw)):
                prefix = exporter.complete_prefix(raw)
                self.assertTrue(raw.startswith(prefix))
                self.assertLessEqual(len(prefix), len(raw))
                self.assertTrue(not prefix or prefix.endswith(b"\n"))
                self.assertNotIn(b"\n", raw[len(prefix):])

    def test_complete_malformed_JSON_rejects_without_capture(self):
        self.source().write_bytes(b'{"broken\n')
        with self.assertRaises(ValueError):
            self.capture()
        self.assertFalse((self.root / "06_REGISTRU/ISTORIC").exists())


class DestinationRegressionTests(SandboxFixture):
    def test_F06_H05_role_parent_escape_rejected(self):
        self.sources[0]["role"] = "../ESCAPED"
        with self.assertRaisesRegex(ValueError, "Unsafe role"):
            self.capture()
        self.assertFalse((self.root / "06_REGISTRU/ISTORIC").exists())
        self.no_external_writes()

    def test_F06_H06_role_outside_ROOT_rejected(self):
        self.sources[0]["role"] = "../../../../../OUTSIDE_ROOT/ESCAPED"
        with self.assertRaisesRegex(ValueError, "Unsafe role"):
            self.capture()
        self.no_external_writes()

    def test_F06_role_path_absolute_ADS_alias_and_reserved_variants(self):
        roles = ["/absolute", r"C:\outside", r"\\server\share", r"..\ESCAPED",
                 "A/child", "A\\child", "A:stream", ".", "..", "A.", "A ", " A",
                 "CON", "nul", "Lpt1", "COM9", "A~1", "A\x00B", "A\nB",
                 "index", "INDEX", "index.json", "index.sha256", "", True, "é"]
        for role in roles:
            with self.subTest(role=role):
                self.sources[0]["role"] = role
                with self.assertRaisesRegex(ValueError, "Unsafe role"):
                    self.capture()
                self.assertFalse((self.root / "06_REGISTRU/ISTORIC").exists())
                self.no_external_writes()

    def test_F06_round_path_reserved_alias_variants(self):
        for value in ("../OUTSIDE_ROOT", "/abs", r"C:\abs", "CON", "nul", "COM1",
                      "LPT9", "round.", "round ", "r:ads", "round~1", ".", "", "x", "r" * 62):
            with self.subTest(round_id=value):
                with self.assertRaisesRegex(ValueError, "Unsafe round"):
                    self.capture(value)
                self.no_external_writes()

    def test_F06_duplicate_roles_and_case_aliases_rejected(self):
        self.add_source("A-TEST")
        for role in ("A-TEST", "a-test"):
            with self.subTest(role=role):
                self.sources[1]["role"] = role
                with self.assertRaisesRegex(ValueError, "Duplicate/aliased role"):
                    self.capture()
                self.assertFalse((self.root / "06_REGISTRU/ISTORIC").exists())

    def test_F06_duplicate_agent_rejected(self):
        self.sources.append({**self.sources[0], "role": "B-TEST"})
        with self.assertRaisesRegex(ValueError, "agent_id"):
            self.capture()

    def test_F06_duplicate_source_symlink_alias_rejected(self):
        second = self.add_source("B-TEST")
        second.unlink()
        self.link(second, self.source())
        with self.assertRaisesRegex(ValueError, "Duplicate/aliased source"):
            self.capture()

    def test_F06_duplicate_source_hardlink_alias_rejected(self):
        second = self.add_source("B-TEST")
        second.unlink()
        try:
            os.link(self.bounded(self.source()), self.bounded(second))
        except OSError as exc:
            self.skipTest(f"OS does not permit hardlink: {exc}")
        with self.assertRaisesRegex(ValueError, "Duplicate/aliased source"):
            self.capture()

    def test_F06_index_and_sidecar_namespace_collisions(self):
        for names in (["index.json", "index.sha256", "index.json"],
                      ["index.json", "INDEX.JSON"],
                      ["index.json", "index.sha256", "INDEX.SHA256"],
                      ["A-TEST.md", "a-test.MD"],
                      ["index.json", "../index.sha256"]):
            with self.subTest(names=names):
                with self.assertRaises(ValueError):
                    exporter.validate_output_names(names)

    def test_F06_H07_destination_parent_symlink_escape(self):
        parent = self.root.joinpath(*exporter.CAPTURE_PARTS)
        self.link(parent, self.outside)
        with self.assertRaisesRegex(ValueError, "Symlink/reparse"):
            self.capture()
        self.no_external_writes()

    def test_F06_destination_ancestor_symlink_escape(self):
        self.link(self.root / "06_REGISTRU/ISTORIC", self.outside)
        with self.assertRaisesRegex(ValueError, "Symlink/reparse"):
            self.capture()
        self.no_external_writes()

    def test_F06_inside_root_symlink_alias_also_refused(self):
        target = self.bounded(self.root / "OTHER")
        target.mkdir()
        self.link(self.root.joinpath(*exporter.CAPTURE_PARTS), target)
        with self.assertRaisesRegex(ValueError, "Symlink/reparse"):
            self.capture()
        self.assertEqual(list(target.iterdir()), [])

    def test_F06_destination_parent_Windows_junction_escape(self):
        self.link(self.root.joinpath(*exporter.CAPTURE_PARTS), self.outside, junction=True)
        with self.assertRaisesRegex(ValueError, "Symlink/reparse"):
            self.capture()
        self.no_external_writes()

    def test_F06_root_symlink_is_not_hidden_by_resolve(self):
        alias = self.link(self.sandbox / "ROOT-ALIAS", self.root)
        with self.assertRaisesRegex(ValueError, "Symlink/reparse"):
            self.capture(root=alias)
        self.no_external_writes()

    def test_F06_root_parent_junction_is_not_hidden_by_resolve(self):
        nested = self.bounded(self.root / "NESTED")
        nested.mkdir()
        alias = self.link(self.sandbox / "PARENT-ALIAS", self.root, junction=True)
        with self.assertRaisesRegex(ValueError, "Symlink/reparse"):
            exporter.checked_root(alias / "NESTED")
        self.no_external_writes()

    def test_F06_existing_round_symlink_refused(self):
        parent = self.root.joinpath(*exporter.CAPTURE_PARTS)
        self.link(parent / "round-TEST", self.outside)
        with self.assertRaisesRegex(ValueError, "no overwrite"):
            self.capture()
        self.no_external_writes()

    def test_F06_dangling_round_symlink_refused(self):
        missing = self.bounded(self.outside / "missing")
        self.link(self.root.joinpath(*exporter.CAPTURE_PARTS) / "round-TEST", missing)
        with self.assertRaisesRegex(ValueError, "no overwrite"):
            self.capture()
        self.no_external_writes()

    def test_F06_existing_round_and_case_alias_preserved(self):
        result = self.capture()
        dest = Path(result["capture"])
        before = {p.name: p.read_bytes() for p in dest.iterdir()}
        for value in ("round-TEST", "ROUND-test"):
            with self.subTest(round_id=value):
                with self.assertRaisesRegex(ValueError, "no overwrite"):
                    self.capture(value)
        self.assertEqual({p.name: p.read_bytes() for p in dest.iterdir()}, before)

    def test_F06_file_in_capture_ancestor_refused(self):
        blocker = self.bounded(self.root / "06_REGISTRU/ISTORIC")
        blocker.write_bytes(b"TEST blocking file")
        with self.assertRaisesRegex(ValueError, "Not a directory"):
            self.capture()
        self.assertEqual(blocker.read_bytes(), b"TEST blocking file")

    def test_F06_index_collisions_at_write_are_not_overwritten(self):
        for number, name in enumerate(("index.json", "index.sha256", "INDEX.JSON", "INDEX.SHA256")):
            with self.subTest(name=name):
                dest = exporter.destination(self.root, f"collision-{number}", create=True)
                target = self.bounded(dest / name)
                target.write_bytes(b"TEST existing")
                with self.assertRaisesRegex(ValueError, "no overwrite"):
                    exporter.write_new(self.root, dest, name.lower(), b"must not replace")
                self.assertEqual(target.read_bytes(), b"TEST existing")

    def test_F06_index_output_symlink_and_hardlink_preserve_targets(self):
        for number, name in enumerate(("index.json", "index.sha256")):
            with self.subTest(name=name):
                dest = exporter.destination(self.root, f"links-{number}", create=True)
                target = self.outside / "sentinel.txt"
                link = self.bounded(dest / name)
                if number == 0:
                    self.link(link, target)
                else:
                    try:
                        os.link(self.bounded(target), link)
                    except OSError as exc:
                        self.skipTest(f"OS does not permit hardlink: {exc}")
                with self.assertRaisesRegex(ValueError, "no overwrite"):
                    exporter.write_new(self.root, dest, name, b"must not replace")
                self.no_external_writes()

    def test_F06_parent_redirected_after_preflight_is_rechecked(self):
        original = exporter.prepare_sources
        def inject(config):
            result = original(config)
            self.link(self.root.joinpath(*exporter.CAPTURE_PARTS), self.outside)
            return result
        with patch.object(exporter, "prepare_sources", side_effect=inject):
            with self.assertRaisesRegex(ValueError, "Symlink/reparse"):
                self.capture()
        self.no_external_writes()

    def test_F06_injected_index_collision_prevents_success_result(self):
        original = exporter.write_new
        def inject(root, dest, name, data):
            if name == "index.json":
                self.bounded(dest / "INDEX.JSON").write_bytes(b"TEST collision")
            return original(root, dest, name, data)
        with patch.object(exporter, "write_new", side_effect=inject):
            with self.assertRaisesRegex(ValueError, "no overwrite"):
                self.capture()
        dest = self.root.joinpath(*exporter.CAPTURE_PARTS) / "round-TEST"
        self.assertFalse((dest / "index.sha256").exists())
        self.assertEqual((dest / "INDEX.JSON").read_bytes(), b"TEST collision")
        self.no_external_writes()


class CompatibilityRegressionTests(SandboxFixture):
    def test_real_authorized_nine_roles_with_synthetic_sources(self):
        # Real role spelling/schema; IDs/bytes/paths are exclusively synthetic.
        self.sources = []
        roles = ["P-MANAGER", "P-CANON", "P-RESEARCH", "P-SYSTEMS", "A-GOVERNANCE",
                 "A-SYSTEMS", "A-CANON", "A-SOURCES", "A-QAMANAGER"]
        for role in roles:
            self.add_source(role)
        result = self.capture("history-r02-03")
        self.assertEqual((result["sources"], result["records"]), (9, 9))
        dest = Path(result["capture"])
        self.assertEqual({p.name for p in dest.iterdir()},
                         {name for role in roles for name in (role + ".md", role + ".jsonl")}
                         | {"index.json", "index.sha256"})
        index = json.loads((dest / "index.json").read_bytes())
        self.assertEqual([s["role"] for s in index["sources"]], roles)
        self.assertEqual(index["start_inclusive"], exporter.START)

    def test_H08_public_filter_end_to_end_and_no_raw_copy(self):
        private = [self.event("TEST PRIVATE", channel="analysis", phase=None),
                   self.event("TEST SYSTEM", role="system"),
                   self.event("TEST DEVELOPER", role="developer"),
                   self.event("TEST UNKNOWN", channel=None, phase=None)]
        rows = private + [self.event("TEST public")]
        raw = b"\n".join(self.encoded(row) for row in rows) + b"\n"
        dest, index = self.checked_capture(raw, 1)
        for path in (dest / "A-TEST.md", dest / "A-TEST.jsonl"):
            content = path.read_bytes()
            for marker in (b"TEST PRIVATE", b"TEST SYSTEM", b"TEST DEVELOPER", b"TEST UNKNOWN"):
                self.assertNotIn(marker, content)
            self.assertNotEqual(content, raw)
        self.assertEqual(sum(index["sources"][0]["omitted_categories"].values()), 4)

    def test_observable_tools_redaction_and_source_line_preserved(self):
        rows = [self.event("TEST public"), {"timestamp": "2026-09-24T01:00:00Z",
                "type": "response_item", "payload": {"type": "custom_tool_call_output",
                "call_id": "c1", "output": {"public": "Bearer " + "A" * 25,
                "reasoning": "TEST hidden", "encrypted_content": "TEST encrypted"}}}]
        dest, index = self.checked_capture(b"\n".join(self.encoded(row) for row in rows) + b"\n", 2)
        data = [json.loads(line) for line in (dest / "A-TEST.jsonl").read_text("utf-8").splitlines()]
        self.assertEqual([r["source_line"] for r in data], [1, 2])
        self.assertEqual(data[1]["output"], {"public": "[SECRET_REDACTED]"})
        self.assertEqual(index["sources"][0]["redactions"], 1)
        self.assertNotIn("c1", (dest / "A-TEST.md").read_text("utf-8"))

    def test_original_timestamp_cutoff_is_unchanged(self):
        older = self.event("TEST before cutoff")
        older["timestamp"] = "2026-09-23T01:00:00Z"
        dest, _ = self.checked_capture(self.encoded(older) + b"\n" + self.encoded() + b"\n", 1)
        self.assertNotIn("before cutoff", (dest / "A-TEST.md").read_text("utf-8"))

    def test_alternate_authorized_configuration_inside_root(self):
        alternate = self.bounded(self.root / "new-sources.json")
        alternate.write_text(json.dumps(self.sources), encoding="utf-8")
        result = exporter.export_capture(self.root, "new-config", "new-sources.json")
        self.assertEqual(result["sources"], 1)

    def test_config_symlink_escape_rejected(self):
        outside_config = self.bounded(self.outside / "config.json")
        outside_config.write_text(json.dumps(self.sources), encoding="utf-8")
        self.link(self.root / "config-alias.json", outside_config)
        with self.assertRaisesRegex(ValueError, "Config outside workshop"):
            exporter.export_capture(self.root, "new-config", "config-alias.json")

    def test_duplicate_configuration_key_rejected(self):
        self.config.write_text('[{"role":"A-TEST","role":"B-TEST"}]', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate configuration key"):
            exporter.export_capture(self.root, "new-config")

    def test_identity_path_mismatch_is_still_rejected(self):
        self.sources[0]["agent_id"] = str(uuid.UUID(int=99))
        with self.assertRaisesRegex(ValueError, "Identity/path mismatch"):
            self.capture()

    def test_all_sources_preflight_before_any_capture_write(self):
        self.add_source("../ESCAPED")
        before = self.source().read_bytes()
        with self.assertRaisesRegex(ValueError, "Unsafe role"):
            self.capture()
        self.assertFalse((self.root / "06_REGISTRU/ISTORIC").exists())
        self.assertEqual(self.source().read_bytes(), before)

    def test_staging_CLI_explicit_synthetic_root(self):
        process = subprocess.run([sys.executable, "-B", str(Path(exporter.__file__).resolve()),
                                  "--root", str(self.root), "--round", "cli-TEST"],
                                 cwd=self.sandbox, capture_output=True, text=True, check=False)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)["sources"], 1)
        self.no_external_writes()

    def test_staging_requires_explicit_root_and_emits_no_success(self):
        with patch.object(exporter, "ROOT", None), contextlib.redirect_stdout(io.StringIO()) as output:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as caught:
                    exporter.main(["--round", "not-run"])
        self.assertEqual(caught.exception.code, 2)
        self.assertEqual(output.getvalue(), "")

    def test_integrated_default_root_retains_original_CLI(self):
        with patch.object(exporter, "ROOT", self.root), contextlib.redirect_stdout(io.StringIO()) as output:
            exporter.main(["--round", "integrated-TEST"])
        self.assertEqual(json.loads(output.getvalue())["sources"], 1)

    def test_CLI_refusal_has_exit_two_without_success_JSON(self):
        self.sources[0]["role"] = "../ESCAPED"
        self.save_config()
        process = subprocess.run([sys.executable, "-B", str(Path(exporter.__file__).resolve()),
                                  "--root", str(self.root), "--round", "cli-refused"],
                                 cwd=self.sandbox, capture_output=True, text=True, check=False)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, "")
        self.no_external_writes()


if __name__ == "__main__":
    unittest.main()
