"""All archive inputs/outputs are synthetic and confined to TemporaryDirectory."""

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

sys.dont_write_bytecode = True
import archive_round
import gatekeeper
import test_gatekeeper as fixtures


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.GatekeeperTests(methodName='runTest')
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.root = self.f.root

    def snapshot(self, round_id='round-001', **kwargs):
        self.f.persist()
        return archive_round.archive(self.root, 'novel', round_id, **kwargs)

    def assertIndexValid(self, result):
        snapshot = Path(result['snapshot_path'])
        index_bytes = (snapshot / 'index.json').read_bytes()
        digest = hashlib.sha256(index_bytes).hexdigest()
        self.assertEqual(digest, result['index_sha256'])
        self.assertEqual(digest, (snapshot / 'index.sha256').read_text(encoding='ascii').strip())
        index = json.loads(index_bytes)
        self.assertFalse(index['editorial_approval_issued'])
        self.assertTrue(index['supplied_result_is_not_certified'])
        paths = set()
        for entry in index['entries']:
            path = snapshot / entry['path']
            self.assertTrue(path.resolve().is_relative_to(snapshot.resolve()))
            data = path.read_bytes()
            self.assertEqual(entry['sha256'], hashlib.sha256(data).hexdigest())
            self.assertEqual(entry['size_bytes'], len(data))
            self.assertNotIn(entry['path'], paths)
            paths.add(entry['path'])
        # Test-only traversal, confined to this TemporaryDirectory snapshot.
        actual = {p.relative_to(snapshot).as_posix() for p in snapshot.rglob('*') if p.is_file()}
        self.assertEqual(actual, paths | {'index.json', 'index.sha256'})
        return snapshot, index

    def test_snapshot_preserves_manifest_registries_audits_and_artifacts(self):
        result = self.snapshot()
        snapshot, index = self.assertIndexValid(result)
        self.assertEqual(json.loads((snapshot / 'manifest.json').read_bytes()), self.f.item)
        for entry in index['entries']:
            if 'source_path' in entry:
                self.assertEqual((snapshot / entry['path']).read_bytes(),
                                 (self.root / entry['source_path']).read_bytes())
        self.assertEqual(snapshot, self.root / '08_ARHIVA/novel/round-001')

    def test_existing_round_is_never_overwritten(self):
        result = self.snapshot()
        snapshot, _ = self.assertIndexValid(result)
        before = {p.relative_to(snapshot): p.read_bytes() for p in snapshot.rglob('*') if p.is_file()}
        with self.assertRaisesRegex(gatekeeper.Rejection, 'EXISTS'):
            self.snapshot()
        after = {p.relative_to(snapshot): p.read_bytes() for p in snapshot.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_existing_empty_round_is_not_reused(self):
        path = self.root / '08_ARHIVA/novel/round-001'
        path.mkdir(parents=True)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'EXISTS'):
            self.snapshot()
        self.assertEqual(list(path.iterdir()), [])

    def test_second_round_keeps_rejected_first_version(self):
        self.f.first_report()['verdict'] = 'RETURN'
        first = self.snapshot('round-001')
        first_path, _ = self.assertIndexValid(first)
        original = (first_path / 'sources/artifacts/novel.txt').read_bytes()
        self.f.write('artifacts/novel.txt', 'Revised narrative version.')
        self.f.refresh()
        second = self.snapshot('round-002')
        second_path, _ = self.assertIndexValid(second)
        self.assertEqual((first_path / 'sources/artifacts/novel.txt').read_bytes(), original)
        self.assertNotEqual((second_path / 'sources/artifacts/novel.txt').read_bytes(), original)

    def test_rejected_audit_is_preserved_without_granting_pass(self):
        self.f.first_report()['verdict'] = 'RETURN'
        self.f.first_report()['criteria'][0]['score'] = 950
        self.f.first_report()['findings'] = [self.f.finding()]
        result = self.snapshot()
        snapshot, _ = self.assertIndexValid(result)
        report = json.loads((snapshot / 'sources/audits/novel-1.json').read_bytes())
        self.assertEqual(report['verdict'], 'RETURN')
        self.assertEqual(report['criteria'][0]['score'], 950)
        self.assertFalse(result['editorial_approval_issued'])
        self.assertNotIn('passed', result)

    def test_round_without_audits_can_be_archived_without_approval(self):
        self.f.item['audits'] = []
        self.f.policy['require_meta_audit'] = True
        self.assertIndexValid(self.snapshot())

    def test_result_is_preserved_exactly_including_rejection(self):
        self.f.first_report()['verdict'] = 'RETURN'
        self.f.persist()
        result_bytes = json.dumps(gatekeeper.validate(self.root, 'novel'), indent=2).encode('utf-8')
        self.f.write('results/return.json', result_bytes)
        result = self.snapshot(result_path='results/return.json')
        snapshot, index = self.assertIndexValid(result)
        self.assertEqual((snapshot / 'result.json').read_bytes(), result_bytes)
        self.assertFalse(json.loads((snapshot / 'result.json').read_bytes())['passed'])
        self.assertTrue(index['result_provided'])

    def test_result_for_wrong_deliverable_is_rejected_before_writing(self):
        self.f.persist()
        result = gatekeeper.validate(self.root, 'novel')
        result['deliverable_id'] = 'other'
        self.f.write('results/result.json', json.dumps(result))
        with self.assertRaisesRegex(gatekeeper.Rejection, 'matching deliverable_id'):
            self.snapshot(result_path='results/result.json')
        self.assertFalse((self.root / '08_ARHIVA').exists())

    def test_repeated_extras_are_copied_and_hashed(self):
        extras = ['plans/measures.md', 'results/retest.json', 'mandates/prompt.txt', 'messages/final.md']
        for path in extras:
            self.f.write(path, 'Synthetic process record: ' + path)
        snapshot, index = self.assertIndexValid(self.snapshot(extras=extras))
        indexed = {entry['path']: entry for entry in index['entries']}
        for rel in extras:
            self.assertEqual(indexed['sources/' + rel]['kind'], 'extra')
            self.assertEqual((snapshot / 'sources' / rel).read_bytes(), (self.root / rel).read_bytes())

    def test_duplicate_extra_argument_is_rejected(self):
        with self.assertRaisesRegex(gatekeeper.Rejection, 'DUPLICATE'):
            self.snapshot(extras=['artifacts/note.md', 'artifacts/note.md'])
        self.assertFalse((self.root / '08_ARHIVA').exists())

    def test_extra_already_in_manifest_is_copied_once(self):
        _, index = self.assertIndexValid(self.snapshot(extras=['artifacts/note.md']))
        self.assertEqual(sum(e['path'] == 'sources/artifacts/note.md' for e in index['entries']), 1)

    def test_missing_extra_is_rejected(self):
        with self.assertRaisesRegex(gatekeeper.Rejection, 'FILE'):
            self.snapshot(extras=['missing.txt'])
        self.assertFalse((self.root / '08_ARHIVA').exists())

    def test_extra_directory_is_rejected_without_recursive_discovery(self):
        with self.assertRaisesRegex(gatekeeper.Rejection, 'regular file'):
            self.snapshot(extras=['artifacts'])

    def test_extra_and_result_traversal_are_rejected(self):
        for kwargs in ({'extras': ['../outside.txt']}, {'result_path': '../outside.json'}):
            with self.subTest(kwargs=kwargs), self.assertRaisesRegex(gatekeeper.Rejection, 'PATH'):
                self.snapshot(**kwargs)

    def test_absolute_extra_outside_is_rejected(self):
        path = self.f.write('outside.txt', 'Outside ROOT, inside temporary test directory.', outside=True)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'PATH'):
            self.snapshot(extras=[str(path)])

    def test_extra_symlink_escape_is_rejected(self):
        outside = self.f.write('outside.txt', 'Outside ROOT.', outside=True)
        self.f.symlink(self.root / 'artifacts/escape.txt', outside)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'escapes ROOT'):
            self.snapshot(extras=['artifacts/escape.txt'])

    def test_stale_artifact_hash_is_rejected_before_creating_archive(self):
        self.f.write('artifacts/novel.txt', 'Changed after audit.')
        with self.assertRaisesRegex(gatekeeper.Rejection, 'HASH'):
            self.snapshot()
        self.assertFalse((self.root / '08_ARHIVA').exists())

    def test_stale_audit_claim_is_rejected(self):
        self.f.write('artifacts/novel.txt', 'Changed after audit.')
        self.f.item['files'][0] = self.f.file_entry('artifacts/novel.txt')
        with self.assertRaisesRegex(gatekeeper.Rejection, 'HASH'):
            self.snapshot()

    def test_malformed_hash_is_rejected(self):
        self.f.item['files'][0]['sha256'] = True
        with self.assertRaisesRegex(gatekeeper.Rejection, 'SHA-256'):
            self.snapshot()

    def test_missing_artifact_is_rejected(self):
        (self.root / 'artifacts/novel.txt').unlink()
        with self.assertRaisesRegex(gatekeeper.Rejection, 'FILE'):
            self.snapshot()

    def test_unsafe_round_identifiers_are_rejected(self):
        for identifier in ('../escape', '..', '/absolute', 'a/b', 'a\\b', 'a:b', 'CON', 'aux.txt', 'end.'):
            with self.subTest(identifier=identifier), self.assertRaisesRegex(gatekeeper.Rejection, 'PATH'):
                self.snapshot(identifier)
        self.assertFalse((self.root / '08_ARHIVA').exists())

    def test_unsafe_deliverable_identifier_is_rejected(self):
        self.f.persist()
        with self.assertRaisesRegex(gatekeeper.Rejection, 'PATH'):
            archive_round.archive(self.root, '../novel', 'round-001')

    def test_destination_symlink_escape_is_rejected(self):
        outside = self.f.sandbox / 'outside-archive'
        outside.mkdir()
        self.f.symlink(self.root / '08_ARHIVA', outside)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'PATH'):
            self.snapshot()
        self.assertEqual(list(outside.iterdir()), [])

    def test_internal_destination_symlink_is_also_rejected(self):
        internal = self.root / 'internal-directory'
        internal.mkdir()
        self.f.symlink(self.root / '08_ARHIVA', internal)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'PATH'):
            self.snapshot()
        self.assertEqual(list(internal.iterdir()), [])

    def test_existing_round_symlink_is_never_followed(self):
        parent = self.root / '08_ARHIVA/novel'
        parent.mkdir(parents=True)
        self.f.symlink(parent / 'round-001', self.root / 'artifacts')
        with self.assertRaisesRegex(gatekeeper.Rejection, 'EXISTS'):
            self.snapshot()

    def test_cannot_ingest_previous_archive_as_extra(self):
        self.snapshot('round-001')
        with self.assertRaisesRegex(gatekeeper.Rejection, 'cannot ingest the archive tree'):
            self.snapshot('round-002', extras=['08_ARHIVA/novel/round-001/index.json'])

    def test_dependency_artifacts_and_manifests_are_preserved(self):
        self.f.dependency()
        snapshot, index = self.assertIndexValid(self.snapshot())
        self.assertEqual(index['dependencies'], ['draft'])
        self.assertEqual(json.loads((snapshot / 'dependency_manifests/draft.json').read_bytes())['id'], 'draft')
        self.assertTrue((snapshot / 'sources/audits/draft-1.json').is_file())

    def test_rejected_cycle_can_be_preserved_without_recursing_forever(self):
        self.f.dependency()['dependencies'] = ['novel']
        self.f.persist()
        result = gatekeeper.validate(self.root, 'novel')
        self.assertFalse(result['passed'])
        self.f.write('results/cycle.json', json.dumps(result))
        self.assertIndexValid(self.snapshot(result_path='results/cycle.json', preserve_rejected=True))

    def test_meta_report_is_copied_and_indexed(self):
        self.f.enable_meta()
        snapshot, index = self.assertIndexValid(self.snapshot())
        path = 'sources/05_AUDIT/meta.json'
        self.assertEqual((snapshot / path).read_bytes(), (self.root / '05_AUDIT/meta.json').read_bytes())
        entry = next(e for e in index['entries'] if e['path'] == path)
        self.assertEqual(entry['kind'], 'meta_audit_report')

    def test_rejected_meta_report_can_be_preserved(self):
        self.f.enable_meta()['verdict'] = 'RETURN'
        snapshot, _ = self.assertIndexValid(self.snapshot())
        report = json.loads((snapshot / 'sources/05_AUDIT/meta.json').read_bytes())
        self.assertEqual(report['verdict'], 'RETURN')

    def test_stale_meta_hash_is_rejected(self):
        self.f.enable_meta()
        self.f.first_report()['verdict'] = 'RETURN'
        with self.assertRaisesRegex(gatekeeper.Rejection, 'HASH'):
            self.snapshot()

    def test_input_change_before_snapshot_is_rejected_without_writes(self):
        with mock.patch.object(gatekeeper.Gatekeeper, 'verify_unchanged', return_value=['CHANGED: synthetic']):
            with self.assertRaisesRegex(gatekeeper.Rejection, 'CHANGED'):
                self.snapshot()
        self.assertFalse((self.root / '08_ARHIVA').exists())

    def test_input_change_during_copy_leaves_incomplete_round_never_reused(self):
        with mock.patch.object(gatekeeper.Gatekeeper, 'verify_unchanged', side_effect=[[], ['changed']]):
            with self.assertRaisesRegex(gatekeeper.Rejection, 'INCOMPLETE'):
                self.snapshot()
        path = self.root / '08_ARHIVA/novel/round-001'
        self.assertTrue(path.is_dir())
        self.assertFalse((path / 'index.sha256').exists())
        with self.assertRaisesRegex(gatekeeper.Rejection, 'EXISTS'):
            self.snapshot()

    def test_archive_writes_only_beneath_08_arhiva(self):
        self.f.persist()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.snapshot()
        for rel, data in before.items():
            self.assertEqual((self.root / rel).read_bytes(), data)
        for path in self.root.rglob('*'):
            if path.is_file() and path.relative_to(self.root) not in before:
                self.assertTrue(path.is_relative_to(self.root / '08_ARHIVA'))

    def test_cli_repeated_extras_and_duplicate_round_exit_codes(self):
        self.f.persist()
        self.f.write('plans/measures.md', 'Synthetic plan.')
        self.f.write('messages/final.txt', 'Synthetic message.')
        command = [sys.executable, '-B', str(Path(archive_round.__file__).resolve()),
                   '--root', str(self.root), '--deliverable', 'novel', '--round', 'round-cli',
                   '--extra', 'plans/measures.md', '--extra', 'messages/final.txt']
        for expected in (0, 2):
            process = subprocess.run(command, cwd=self.f.sandbox, text=True, capture_output=True, check=False)
            self.assertEqual(process.returncode, expected, process.stdout + process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['archived'], expected == 0)
            self.assertEqual(process.stderr, '')

    def test_index_exposes_tampering_when_trusted_hash_is_kept_separately(self):
        snapshot, index = self.assertIndexValid(self.snapshot())
        entry = next(e for e in index['entries'] if e['path'] == 'sources/artifacts/novel.txt')
        self.f.write('08_ARHIVA/novel/round-001/sources/artifacts/novel.txt', 'Tampered synthetic copy.')
        self.assertNotEqual(hashlib.sha256((snapshot / entry['path']).read_bytes()).hexdigest(), entry['sha256'])


class ArchiveAdversarialR02Tests(unittest.TestCase):
    """TEST: F02/P23 and F03/P12 preserve bytes, never rewrite declared approval."""

    assertIndexValid = ArchiveTests.assertIndexValid

    def setUp(self):
        self.a = fixtures.AdversarialR02Tests(methodName='runTest')
        self.a.setUp()
        self.addCleanup(self.a.doCleanups)
        self.f, self.root = self.a.f, self.a.f.root

    def reject_result(self):
        result = gatekeeper.validate(self.root, 'novel')
        self.assertFalse(result['passed'], result)
        data = json.dumps(result, ensure_ascii=True, indent=2).encode('utf-8')
        self.f.write('results/original-return.json', data)
        return data

    def preserve(self, round_id='rejected-r02', extras=()):
        return archive_round.archive(self.root, 'novel', round_id,
                                     result_path='results/original-return.json', extras=extras,
                                     preserve_rejected=True)

    def test_F03_P12_RETURN_HASH_preserved_with_declared_and_observed_separate(self):
        declared = (self.root / '06_REGISTRU/deliverables.json').read_bytes()
        reports = self.a.parent_reports()
        old_hash = self.f.item['files'][0]['sha256']
        self.f.write('artifacts/novel.txt', 'Changed after audit; TEST incident.')
        original_result = self.reject_result()
        with self.assertRaisesRegex(gatekeeper.Rejection, 'HASH'):
            archive_round.archive(self.root, 'novel', 'strict-refused',
                                  result_path='results/original-return.json')
        snapshot, index = self.assertIndexValid(self.preserve())
        self.assertEqual(index['archive_kind'], 'rejected_evidence_snapshot')
        self.assertEqual(index['source_consistency'], 'NOT_CERTIFIED')
        self.assertEqual(index['supplied_result_verdict'], 'RETURN')
        self.assertEqual((snapshot / 'result.json').read_bytes(), original_result)
        self.assertEqual((snapshot / 'sources/06_REGISTRU/deliverables.json').read_bytes(), declared)
        self.assertEqual((self.root / '06_REGISTRU/deliverables.json').read_bytes(), declared)
        self.assertEqual(self.a.parent_reports(), reports)
        self.assertEqual(json.loads((snapshot / 'manifest.json').read_bytes())['files'][0]['sha256'], old_hash)
        row = next(r for r in index['observations'] if r['source_path'] == 'artifacts/novel.txt')
        self.assertEqual(row['declared_sha256'], old_hash)
        self.assertEqual(row['observed_sha256'], self.f.file_entry('artifacts/novel.txt')['sha256'])
        self.assertNotEqual(row['declared_sha256'], row['observed_sha256'])
        self.assertEqual(row['diagnostics'][0]['code'], 'HASH_MISMATCH')
        restored = gatekeeper.validate(snapshot / 'sources', 'novel')
        self.assertFalse(restored['passed'])
        self.assertIn('HASH', str(restored['errors']))

    def test_F03_missing_artifact_is_recorded_without_fake_bytes_or_hash(self):
        (self.root / 'artifacts/novel.txt').unlink()
        self.reject_result()
        snapshot, index = self.assertIndexValid(self.preserve())
        row = next(r for r in index['observations'] if r['source_path'] == 'artifacts/novel.txt')
        self.assertIsNone(row['observed_sha256'])
        self.assertIsNone(row['copied_path'])
        self.assertFalse((snapshot / 'sources/artifacts/novel.txt').exists())
        self.assertEqual(row['availability'], 'UNAVAILABLE')
        self.assertEqual(index['observed_availability'], 'PARTIAL')

    def test_F03_invalid_declared_hash_is_preserved_not_repaired(self):
        self.f.item['files'][0]['sha256'] = 'INVALID-DECLARED-HASH'
        self.f.persist(freeze=False)
        self.reject_result()
        snapshot, index = self.assertIndexValid(self.preserve())
        manifest = json.loads((snapshot / 'manifest.json').read_bytes())
        self.assertEqual(manifest['files'][0]['sha256'], 'INVALID-DECLARED-HASH')
        row = next(r for r in index['observations'] if r['source_path'] == 'artifacts/novel.txt')
        self.assertEqual(row['diagnostics'][0]['code'], 'HASH_INVALID')
        self.assertIsNotNone(row['observed_sha256'])

    def test_F03_unsafe_path_is_recorded_without_reading_outside_root(self):
        self.f.write('outside.txt', 'TEST outside root.', outside=True)
        self.f.item['files'][0]['path'] = '../outside.txt'
        self.f.persist(freeze=False)
        self.reject_result()
        snapshot, index = self.assertIndexValid(self.preserve())
        row = next(r for r in index['observations'] if r['source_path'] == '../outside.txt')
        self.assertEqual(row['diagnostics'][0]['code'], 'UNSAFE_PATH')
        self.assertIsNone(row['copied_path'])
        self.assertIsNone(row['observed_sha256'])
        self.assertFalse((snapshot / 'outside.txt').exists())

    def test_F03_symlink_escape_is_recorded_without_copying_target(self):
        outside = self.f.write('outside.txt', 'TEST outside root.', outside=True)
        link = self.root / 'artifacts/novel.txt'
        link.unlink()
        self.f.symlink(link, outside)
        self.reject_result()
        _, index = self.assertIndexValid(self.preserve())
        row = next(r for r in index['observations'] if r['source_path'] == 'artifacts/novel.txt')
        self.assertEqual(row['diagnostics'][0]['code'], 'UNSAFE_PATH')
        self.assertIsNone(row['observed_sha256'])

    def test_F03_preservation_does_not_allow_destination_symlink(self):
        self.f.write('artifacts/novel.txt', 'Changed.')
        self.reject_result()
        outside = self.f.sandbox / 'outside-destination'
        outside.mkdir()
        self.f.symlink(self.root / '08_ARHIVA', outside)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'PATH'):
            self.preserve()
        self.assertEqual(list(outside.iterdir()), [])

    def test_F03_no_result_or_PASS_result_cannot_enter_preservation_mode(self):
        with self.assertRaisesRegex(gatekeeper.Rejection, '--result'):
            archive_round.archive(self.root, 'novel', 'absent-result', preserve_rejected=True)
        self.f.write('results/original-return.json', json.dumps(gatekeeper.validate(self.root, 'novel')))
        with self.assertRaisesRegex(gatekeeper.Rejection, 'passed=false'):
            self.preserve()

    def test_F03_wrong_deliverable_or_boolean_number_result_is_rejected(self):
        for result in (dict(deliverable_id='other', passed=False, errors=['HASH']),
                       dict(deliverable_id='novel', passed=0, errors=['HASH'])):
            with self.subTest(result=result):
                self.f.write('results/original-return.json', json.dumps(result))
                with self.assertRaisesRegex(gatekeeper.Rejection, 'passed=false'):
                    self.preserve()

    def test_F03_legacy_r01_RETURN_is_preserved_without_promoting_schema(self):
        self.f.policy['schema_version'] = 1
        self.f.persist(freeze=False)
        legacy = dict(deliverable_id='novel', passed=False, errors=['HASH: original r01'],
                      weighted_scores=[], word_count=None, checked_files=[], dependencies=[])
        data = json.dumps(legacy, indent=2).encode('utf-8')
        self.f.write('results/original-return.json', data)
        # Simulate the unversioned r01 registry; retain its exact bytes as history.
        item = copy.deepcopy(self.f.item)
        for key in ('version_id', 'contract', 'evidence_files'):
            item.pop(key)
        raw_registry = json.dumps(dict(deliverables=[item])).encode('utf-8')
        self.f.write('06_REGISTRU/deliverables.json', raw_registry)
        snapshot, index = self.assertIndexValid(self.preserve())
        self.assertEqual((snapshot / 'result.json').read_bytes(), data)
        self.assertEqual((snapshot / 'sources/06_REGISTRU/deliverables.json').read_bytes(), raw_registry)
        self.assertNotIn('schema_version', json.loads((snapshot / 'result.json').read_bytes()))
        self.assertFalse(gatekeeper.validate(snapshot / 'sources', 'novel')['passed'])
        self.assertFalse(index['editorial_approval_issued'])

    def test_F03_changed_meta_is_preserved_with_old_claims(self):
        self.f.first_report()['limitations'] = ['TEST changed after meta review.']
        self.f.persist(freeze=False)
        result_bytes = self.reject_result()
        snapshot, index = self.assertIndexValid(self.preserve())
        self.assertEqual((snapshot / 'result.json').read_bytes(), result_bytes)
        self.assertTrue(any(any(d['code'] == 'HASH_MISMATCH' for d in row['diagnostics'])
                            for row in index['observations'] if row['source_path'] == 'audits/novel-1.json'))

    def test_F03_rejected_round_is_never_overwritten(self):
        self.f.write('artifacts/novel.txt', 'Changed.')
        self.reject_result()
        snapshot, _ = self.assertIndexValid(self.preserve())
        before = (snapshot / 'index.json').read_bytes()
        with self.assertRaisesRegex(gatekeeper.Rejection, 'EXISTS'):
            self.preserve()
        self.assertEqual((snapshot / 'index.json').read_bytes(), before)

    def test_F03_malformed_report_bytes_preserved_with_incomplete_traversal_flag(self):
        self.f.write('audits/novel-1.json', '{TEST invalid JSON')
        self.reject_result()
        snapshot, index = self.assertIndexValid(self.preserve())
        self.assertEqual((snapshot / 'sources/audits/novel-1.json').read_bytes(), b'{TEST invalid JSON')
        self.assertFalse(index['declaration_traversal_complete'])
        self.assertTrue(any(any(d['code'] == 'SCHEMA_INVALID' for d in row['diagnostics'])
                            for row in index['observations']))

    def test_F03_preservation_keeps_extras_and_original_rejected_reports(self):
        self.f.first_report()['verdict'] = 'RETURN'
        self.f.first_report()['findings'] = [self.f.finding()]
        self.a.approve_fixture()  # refresh meta bytes, intentionally retaining the RETURN
        self.reject_result()
        self.f.write('measures.md', 'TEST planned remediation; not closed.')
        snapshot, _ = self.assertIndexValid(self.preserve(extras=['measures.md']))
        audit = json.loads((snapshot / 'sources/audits/novel-1.json').read_bytes())
        self.assertEqual(audit['verdict'], 'RETURN')
        self.assertEqual(audit['findings'][0]['status'], 'open')
        self.assertEqual((snapshot / 'sources/measures.md').read_bytes(), (self.root / 'measures.md').read_bytes())

    def test_F02_P23_auto_archived_evidence_restores_without_original_root(self):
        self.f.write('sources/proof.txt', 'TEST frozen evidence.')
        self.f.item['evidence_files'] = [self.f.file_entry('sources/proof.txt')]
        for path in self.f.item['audits']:
            for criterion in self.f.reports[path]['criteria']:
                criterion['evidence'] = [self.f.proof('sources/proof.txt:L1-L1')]
        self.a.approve_fixture()
        self.assertTrue(gatekeeper.validate(self.root, 'novel')['passed'])
        result = archive_round.archive(self.root, 'novel', 'complete-proof')
        snapshot, index = self.assertIndexValid(result)
        entry = next(e for e in index['entries'] if e.get('source_path') == 'sources/proof.txt')
        self.assertEqual(entry['sha256'], self.f.file_entry('sources/proof.txt')['sha256'])
        # Delete the original evidence (inside TemporaryDirectory), so restoration cannot use it.
        (self.root / 'sources/proof.txt').unlink()
        restored = gatekeeper.validate(snapshot / 'sources', 'novel')
        self.assertTrue(restored['passed'], restored)

    def test_F02_missing_frozen_evidence_refuses_strict_but_preserves_incident(self):
        self.f.write('sources/proof.txt', 'TEST proof.')
        self.f.item['evidence_files'] = [self.f.file_entry('sources/proof.txt')]
        self.a.approve_fixture()
        (self.root / 'sources/proof.txt').unlink()
        self.reject_result()
        with self.assertRaisesRegex(gatekeeper.Rejection, 'FILE'):
            archive_round.archive(self.root, 'novel', 'missing-proof-strict')
        _, index = self.assertIndexValid(self.preserve())
        self.assertEqual(index['observed_availability'], 'PARTIAL')

    def test_F02_paired_MD_is_preserved_with_exact_digest(self):
        self.f.write('audits/novel-1.md', '# TEST paired review\nNo hash of its JSON.\n')
        self.f.item['evidence_files'] = [self.f.file_entry('audits/novel-1.md')]
        self.f.first_report()['criteria'][0]['evidence'] = [self.f.proof('audits/novel-1.md#review')]
        self.a.approve_fixture()
        snapshot, _ = self.assertIndexValid(archive_round.archive(self.root, 'novel', 'paired-md'))
        self.assertEqual((snapshot / 'sources/audits/novel-1.md').read_bytes(),
                         (self.root / 'audits/novel-1.md').read_bytes())
        self.assertTrue(gatekeeper.validate(snapshot / 'sources', 'novel')['passed'])

    def test_strict_archive_does_not_silently_accept_legacy_report(self):
        self.f.first_report()['schema_version'] = 1
        self.f.persist(freeze=False)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'schema_version'):
            archive_round.archive(self.root, 'novel', 'legacy-refused')

    def test_F03_cli_preserve_rejected_returns_operation_success_not_PASS(self):
        self.f.write('artifacts/novel.txt', 'Changed after audit.')
        self.reject_result()
        process = subprocess.run([sys.executable, '-B', str(Path(archive_round.__file__).resolve()),
                                  '--root', str(self.root), '--deliverable', 'novel', '--round', 'cli-rejected',
                                  '--result', 'results/original-return.json', '--preserve-rejected'],
                                 cwd=self.f.sandbox, capture_output=True, text=True, check=False)
        self.assertEqual(process.returncode, 0, process.stderr + process.stdout)
        result = json.loads(process.stdout)
        self.assertTrue(result['archived'])
        self.assertFalse(result['editorial_approval_issued'])
        self.assertNotIn('passed', result)
        self.assertIndexValid(result)


class SupplementalArchiveTests(unittest.TestCase):
    """TEST: normal auditor supplement chain is captured without --extra or refreezing."""

    assertIndexValid = ArchiveTests.assertIndexValid

    def setUp(self):
        self.s = fixtures.SupplementalEvidenceTests(methodName='runTest')
        self.s.setUp()
        self.addCleanup(self.s.doCleanups)
        self.f, self.root = self.s.f, self.s.f.root
        self.supplements = self.s.normal_workflow()

    def capture(self, name='supplement-round'):
        return archive_round.archive(self.root, 'novel', name)

    def test_all_audit_and_meta_supplements_auto_archived_and_restored(self):
        self.assertTrue(self.s.result()['passed'])
        snapshot, index = self.assertIndexValid(self.capture())
        for path in self.supplements:
            entry = next(e for e in index['entries'] if e.get('source_path') == path)
            self.assertEqual(entry['kind'], 'supplemental_evidence_source')
            self.assertEqual(entry['sha256'], self.f.file_entry(path)['sha256'])
            self.assertEqual((snapshot / 'sources' / path).read_bytes(), (self.root / path).read_bytes())
        self.assertEqual((snapshot / 'sources' / self.f.item['contract']['path']).read_bytes(), self.s.frozen_contract)
        self.assertEqual((snapshot / 'sources/06_REGISTRU/deliverables.json').read_bytes(), self.s.frozen_registry)
        # The unused test logs must be copied too. No access to originals is possible now.
        for path in self.supplements:
            (self.root / path).unlink()
        restored = gatekeeper.validate(snapshot / 'sources', 'novel')
        self.assertTrue(restored['passed'], restored)

    def test_strict_archive_rejects_changed_audit_supplement(self):
        self.f.write(self.supplements[0], 'TEST changed primary MD.')
        with self.assertRaisesRegex(gatekeeper.Rejection, 'HASH: supplemental evidence changed'):
            self.capture()
        self.assertFalse((self.root / '08_ARHIVA').exists())

    def test_strict_archive_rejects_changed_meta_supplement(self):
        self.f.write(self.supplements[-1], 'TEST changed meta MD.')
        with self.assertRaisesRegex(gatekeeper.Rejection, 'HASH: supplemental evidence changed'):
            self.capture()

    def test_strict_archive_checks_unused_supplement_and_missing_source(self):
        log = self.supplements[1]
        (self.root / log).unlink()
        with self.assertRaisesRegex(gatekeeper.Rejection, 'FILE'):
            self.capture()

    def test_restored_supplement_tamper_invalidates_gate(self):
        snapshot, _ = self.assertIndexValid(self.capture())
        self.f.write('08_ARHIVA/novel/supplement-round/sources/' + self.supplements[-1], 'TEST tampered copy.')
        result = gatekeeper.validate(snapshot / 'sources', 'novel')
        self.assertFalse(result['passed'])
        self.assertIn('HASH: supplemental evidence changed', str(result['errors']))

    def test_preserve_RETURN_HASH_keeps_original_supplement_claim_and_observed_bytes(self):
        path = self.supplements[-1]
        declared_hash = self.f.file_entry(path)['sha256']
        reports_before = self.s.a.parent_reports()
        self.f.write(path, 'TEST meta supplement drift.')
        original_result = json.dumps(self.s.result(), indent=2).encode('utf-8')
        self.assertFalse(json.loads(original_result)['passed'])
        self.f.write('results/return-supplement.json', original_result)
        result = archive_round.archive(self.root, 'novel', 'supplement-return',
                                       result_path='results/return-supplement.json', preserve_rejected=True)
        snapshot, index = self.assertIndexValid(result)
        self.assertEqual(self.s.a.parent_reports(), reports_before)
        self.assertEqual((snapshot / 'result.json').read_bytes(), original_result)
        row = next(r for r in index['observations']
                   if r['source_path'] == path and r['declared_sha256'] == declared_hash)
        self.assertEqual(row['observed_sha256'], self.f.file_entry(path)['sha256'])
        self.assertNotEqual(row['observed_sha256'], row['declared_sha256'])
        self.assertIn('HASH_MISMATCH', [d['code'] for d in row['diagnostics']])
        self.assertFalse(gatekeeper.validate(snapshot / 'sources', 'novel')['passed'])

    def test_preserve_missing_supplement_marks_partial_without_fabricated_hash(self):
        path = self.supplements[1]
        (self.root / path).unlink()
        self.f.write('results/return-supplement.json', json.dumps(self.s.result()))
        _, index = self.assertIndexValid(archive_round.archive(
            self.root, 'novel', 'missing-supplement', result_path='results/return-supplement.json',
            preserve_rejected=True))
        self.assertEqual(index['observed_availability'], 'PARTIAL')
        row = next(r for r in index['observations'] if r['source_path'] == path)
        self.assertIsNone(row['observed_sha256'])
        self.assertIsNone(row['copied_path'])

    def test_strict_archive_rejects_unlisted_reference_despite_file_existing(self):
        self.f.write('audits/not-declared.md', 'TEST undeclared review note.')
        meta = self.f.reports[self.s.meta_path]
        meta['checks'][0]['evidence'] = [self.f.proof('audits/not-declared.md')]
        self.s.write_report(self.s.meta_path)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'EVIDENCE: source not frozen'):
            self.capture()

    def test_strict_archive_rejects_supplement_override_and_alias(self):
        meta = self.f.reports[self.s.meta_path]
        meta['supplemental_evidence_files'].append(self.f.file_entry('artifacts/novel.txt'))
        self.s.write_report(self.s.meta_path)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'SUPPLEMENTAL: duplicate/override'):
            self.capture()
        meta['supplemental_evidence_files'].pop()
        self.f.symlink(self.root / 'audits/product-alias.txt', self.root / 'artifacts/novel.txt')
        meta['supplemental_evidence_files'].append(self.f.file_entry('audits/product-alias.txt'))
        self.s.write_report(self.s.meta_path)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'SUPPLEMENTAL: alias/override'):
            self.capture()

    def test_strict_archive_rejects_own_JSON_as_supplement(self):
        meta = self.f.reports[self.s.meta_path]
        meta['supplemental_evidence_files'].append(self.f.file_entry(self.s.meta_path))
        self.s.write_report(self.s.meta_path)
        with self.assertRaisesRegex(gatekeeper.Rejection, 'SUPPLEMENTAL: circular'):
            self.capture()

    def test_same_source_explicitly_declared_by_audit_and_meta_is_copied_once(self):
        path = self.supplements[0]
        meta = self.f.reports[self.s.meta_path]
        meta['supplemental_evidence_files'].append(self.f.file_entry(path))
        meta['checks'][1]['evidence'] = [self.f.proof(path)]
        self.s.write_report(self.s.meta_path)
        self.assertTrue(self.s.result()['passed'])
        _, index = self.assertIndexValid(self.capture())
        self.assertEqual(sum(e.get('source_path') == path for e in index['entries']), 1)


if __name__ == '__main__':
    unittest.main()
