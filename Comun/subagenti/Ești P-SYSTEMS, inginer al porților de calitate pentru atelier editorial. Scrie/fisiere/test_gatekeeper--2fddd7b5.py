"""TEST: Synthetic fixtures only. These tests never grant real editorial approvals.

Run with python -B -m unittest -v test_gatekeeper.py.
All test-created files, including escape targets, live in TemporaryDirectory.
"""

import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import uuid

sys.dont_write_bytecode = True
import gatekeeper


class GatekeeperTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='gatekeeper-synthetic-')
        self.addCleanup(temporary.cleanup)
        self.sandbox = Path(temporary.name).resolve()
        self.root = self.sandbox / 'ROOT'
        self.root.mkdir()
        self.producer, self.auditor1, self.auditor2 = [str(uuid.uuid4()) for _ in range(3)]
        self.policy = dict(schema_version=2, threshold_exclusive=950, score_scale=1000,
                           min_independent_auditors=2, require_all_criteria_above_threshold=True,
                           require_meta_audit=False)
        self.agents = [
            dict(agent_id=self.producer, role='author', kind='producer', active=True),
            dict(agent_id=self.auditor1, role='structure', kind='auditor', active=True),
            dict(agent_id=self.auditor2, role='language', kind='auditor', active=True),
        ]
        self.write('artifacts/novel.txt', 'narațiune dialog\n')
        self.write('artifacts/note.md', '# Supporting artifact\nContext.\n')
        self.item = dict(
            id='novel', version_id='v001', stage='FINAL', status='READY', evidence_files=[],
            contract=dict(path='contracts/novel.json', sha256='0' * 64),
            files=[self.file_entry('artifacts/novel.txt'), self.file_entry('artifacts/note.md')],
            producer_agent_ids=[self.producer], required_audit_roles=['structure', 'language'],
            dependencies=[], requirements={}, criteria=[dict(id='a', weight=40), dict(id='b', weight=60)],
            audits=['audits/novel-1.json', 'audits/novel-2.json'])
        self.items = [self.item]
        self.reports = {}
        for number, reviewer in enumerate((self.auditor1, self.auditor2), 1):
            self.reports[f'audits/novel-{number}.json'] = dict(
                schema_version=2, audit_id=f'synthetic-novel-{number}', deliverable_id='novel',
                reviewer_agent_id=reviewer, reviewer_role=self.agents[number]['role'],
                files=copy.deepcopy(self.item['files']),
                criteria=[dict(id='a', score=951, weight=40, evidence=['artifacts/novel.txt#opening']),
                          dict(id='b', score=951, weight=60, evidence=['artifacts/novel.txt:L1'])],
                findings=[], verdict='PASS', limitations=[], reviewed_at='2026-09-24T12:00:00+03:00')

    def write(self, relative, content, outside=False):
        destination = (self.sandbox if outside else self.root) / relative
        self.assertTrue(destination.resolve().is_relative_to(self.sandbox))
        destination.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            destination.write_bytes(content)
        else:
            destination.write_text(content, encoding='utf-8')
        return destination

    def file_entry(self, relative):
        return dict(path=relative, sha256=hashlib.sha256((self.root / relative).read_bytes()).hexdigest())

    def proof(self, reference):
        """Explicit v2 fixture builder, not part of the engine or real audit migration."""
        if '#' in reference:
            path, fragment = reference.split('#', 1)
            anchor = '#' + fragment
        elif ':L' in reference:
            path, fragment = reference.split(':L', 1)
            anchor = ':L' + fragment
        else:
            path, anchor = reference, ''
        candidate = self.root / path
        digest = '0' * 64
        if candidate.is_file() and candidate.resolve().is_relative_to(self.root):
            digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
        return dict(path=path, sha256=digest, anchor=anchor)

    def freeze_contracts(self, update_reports=True):
        """TEST-only minting of fixture contracts. Adversarial tests freeze only once."""
        items = {item['id']: item for item in self.items}
        policy_hash = hashlib.sha256((self.root / '00_CONDUCERE/policy.json').read_bytes()).hexdigest()
        visited = set()
        def freeze(item):
            if item['id'] in visited:
                return
            visited.add(item['id'])
            for child in item['dependencies']:
                if child in items:
                    freeze(items[child])
            # Unknown/cyclic dependencies are deliberately allowed in negative fixtures.
            dependencies = []
            for child in item['dependencies']:
                dependency = items.get(child)
                dependencies.append(dict(deliverable_id=child,
                    version_id=dependency['version_id'] if dependency else 'v001',
                    contract=copy.deepcopy(dependency['contract']) if dependency else
                    dict(path='contracts/missing.json', sha256='0' * 64)))
            doc = dict(schema_version=2, deliverable_id=item['id'],
                       **{key: item[key] for key in gatekeeper.CONTRACT_FIELDS}, dependencies=dependencies,
                       policy=dict(path='00_CONDUCERE/policy.json', sha256=policy_hash))
            self.write(item['contract']['path'], gatekeeper.json_bytes(doc))
            item['contract']['sha256'] = self.file_entry(item['contract']['path'])['sha256']
            if update_reports:
                for path in item['audits'] + ([item['meta_audit']] if 'meta_audit' in item else []):
                    if path in self.reports:
                        self.reports[path]['contract'] = copy.deepcopy(item['contract'])
                        self.reports[path]['version_id'] = item['version_id']
        for item in self.items:
            freeze(item)

    def persist(self, freeze=True):
        self.write('00_CONDUCERE/policy.json', json.dumps(self.policy))
        self.write('06_REGISTRU/agents.json', json.dumps(dict(agents=self.agents)))
        if freeze:
            self.freeze_contracts()
        self.write('06_REGISTRU/deliverables.json', json.dumps(dict(schema_version=2, deliverables=self.items)))
        for path, report in self.reports.items():
            if freeze:
                for criterion in report.get('criteria', report.get('checks', [])):
                    criterion['evidence'] = [self.proof(value) if isinstance(value, str) else value
                                             for value in criterion.get('evidence', [])]
            self.write(path, json.dumps(report))

    def check(self):
        self.persist()
        return gatekeeper.validate(self.root, 'novel')

    def assertRejected(self, result, contains=None):
        self.assertFalse(result['passed'], result)
        self.assertTrue(result['errors'], result)
        if contains is not None:
            self.assertIn(contains, json.dumps(result))

    def first_report(self):
        return self.reports['audits/novel-1.json']

    def refresh(self):
        for item in self.items:
            item['files'] = [self.file_entry(entry['path']) for entry in item['files']]
            for report_path in item['audits']:
                self.reports[report_path]['files'] = copy.deepcopy(item['files'])
                for criterion in self.reports[report_path]['criteria']:
                    criterion['evidence'] = [self.proof(ref['path'] + ref['anchor'])
                                             if isinstance(ref, dict) else ref
                                             for ref in criterion['evidence']]

    def prose(self, words, prefix=''):
        self.item['requirements'] = dict(min_prose_words=50000, prose_paths=['artifacts/novel.txt'])
        self.write('artifacts/novel.txt', prefix + ' '.join(['cuvânt'] * words))
        self.refresh()

    def dependency(self, identifier='draft'):
        child = copy.deepcopy(self.item)
        child['id'] = identifier
        child['contract'] = dict(path=f'contracts/{identifier}.json', sha256='0' * 64)
        child['dependencies'] = []
        child['requirements'] = {}
        child['audits'] = [f'audits/{identifier}-1.json', f'audits/{identifier}-2.json']
        for number in (1, 2):
            report = copy.deepcopy(self.reports[f'audits/novel-{number}.json'])
            report['audit_id'] = f'synthetic-{identifier}-{number}'
            report['deliverable_id'] = identifier
            self.reports[f'audits/{identifier}-{number}.json'] = report
        self.items.append(child)
        self.item['dependencies'].append(identifier)
        return child

    def test_951_passes_and_result_has_exact_public_fields(self):
        result = self.check()
        self.assertTrue(result['passed'], result)
        self.assertEqual(set(result), {'schema_version', 'version_id', 'contract', 'deliverable_id',
                                       'passed', 'errors', 'weighted_scores',
                                       'word_count', 'checked_files', 'dependencies'})
        self.assertEqual([s['score'] for s in result['weighted_scores']], [951, 951])
        self.assertEqual(result['checked_files'], self.item['files'])
        self.assertIsNone(result['word_count'])

    def test_950_rejected_even_when_weighted_average_exceeds_threshold(self):
        self.first_report()['criteria'][0]['score'] = 950
        self.first_report()['criteria'][1]['score'] = 1000
        result = self.check()
        self.assertRejected(result, 'THRESHOLD')
        self.assertEqual(result['weighted_scores'][0]['score'], 980)

    def test_score_1000_passes(self):
        for report in self.reports.values():
            for criterion in report['criteria']:
                criterion['score'] = 1000
        self.assertTrue(self.check()['passed'])

    def test_self_audit_is_rejected(self):
        self.first_report()['reviewer_agent_id'] = self.producer
        self.first_report()['reviewer_role'] = 'author'
        self.assertRejected(self.check(), 'INDEPENDENCE')

    def test_other_registered_producer_cannot_audit(self):
        identifier = str(uuid.uuid4())
        self.agents.append(dict(agent_id=identifier, role='structure', kind='producer', active=True))
        self.first_report()['reviewer_agent_id'] = identifier
        self.assertRejected(self.check(), 'INDEPENDENCE')

    def test_duplicate_auditor_is_rejected(self):
        self.reports['audits/novel-2.json']['reviewer_agent_id'] = self.auditor1
        self.reports['audits/novel-2.json']['reviewer_role'] = 'structure'
        self.assertRejected(self.check(), 'DUPLICATE: auditor')

    def test_unregistered_auditor_is_rejected(self):
        self.first_report()['reviewer_agent_id'] = str(uuid.uuid4())
        self.assertRejected(self.check(), 'unregistered auditor')

    def test_inactive_auditor_is_rejected(self):
        self.agents[1]['active'] = False
        self.assertRejected(self.check(), 'active auditor')

    def test_forged_role_is_rejected(self):
        self.first_report()['reviewer_role'] = 'language'
        self.assertRejected(self.check(), 'ROLE')

    def test_two_people_in_one_role_do_not_cover_two_roles(self):
        self.agents[2]['role'] = 'structure'
        self.reports['audits/novel-2.json']['reviewer_role'] = 'structure'
        self.assertRejected(self.check(), 'ROLES')

    def test_non_uuid_reviewer_is_rejected(self):
        self.first_report()['reviewer_agent_id'] = 'auditor-1'
        self.assertRejected(self.check(), 'UUID')

    def test_nil_uuid_is_rejected(self):
        self.first_report()['reviewer_agent_id'] = str(uuid.UUID(int=0))
        self.assertRejected(self.check(), 'UUID')

    def test_unregistered_producer_is_rejected(self):
        self.item['producer_agent_ids'] = [str(uuid.uuid4())]
        self.assertRejected(self.check(), 'unknown producer')

    def test_outdated_artifact_hash_is_rejected(self):
        self.write('artifacts/novel.txt', 'Changed after audit.')
        self.assertRejected(self.check(), 'HASH')

    def test_updated_manifest_does_not_refresh_old_audit_hash(self):
        self.write('artifacts/novel.txt', 'Changed after audit.')
        self.item['files'][0] = self.file_entry('artifacts/novel.txt')
        self.assertRejected(self.check(), 'HASH')

    def test_second_bundle_file_is_also_hash_checked(self):
        self.write('artifacts/note.md', 'Changed supporting artifact.')
        self.assertRejected(self.check(), 'HASH')

    def test_dependency_hash_change_invalidates_parent(self):
        child = self.dependency()
        self.write('artifacts/draft.txt', 'Draft before audit.')
        child['files'] = [self.file_entry('artifacts/draft.txt')]
        child['evidence_files'] = [self.file_entry('artifacts/novel.txt')]
        for path in child['audits']:
            self.reports[path]['files'] = copy.deepcopy(child['files'])
        self.assertTrue(self.check()['passed'])
        self.write('artifacts/draft.txt', 'Draft changed after passing.')
        result = self.check()
        self.assertRejected(result, 'DEPENDENCY')
        self.assertFalse(result['dependencies'][0]['passed'])
        self.assertIn('HASH', str(result['dependencies'][0]['errors']))

    def test_dependency_status_pass_does_not_replace_audits(self):
        child = self.dependency()
        child['status'] = 'PASS'
        child['audits'] = []
        self.assertRejected(self.check(), 'DEPENDENCY')

    def test_dependency_criterion_failure_invalidates_parent(self):
        self.dependency()
        self.reports['audits/draft-1.json']['criteria'][0]['score'] = 950
        self.assertRejected(self.check(), 'THRESHOLD')

    def test_unknown_dependency_is_rejected(self):
        self.item['dependencies'] = ['absent']
        self.assertRejected(self.check(), 'unknown deliverable')

    def test_cycle_is_rejected(self):
        child = self.dependency()
        child['dependencies'] = ['novel']
        self.assertRejected(self.check(), 'CYCLE')

    def test_self_cycle_is_rejected(self):
        self.item['dependencies'] = ['novel']
        self.assertRejected(self.check(), 'CYCLE')

    def test_shared_dependency_dag_passes(self):
        first = self.dependency('draft')
        second = self.dependency('source')
        second['dependencies'] = [first['id']]
        self.assertTrue(self.check()['passed'])

    def test_malformed_scores_are_rejected(self):
        for score in (True, False, None, '951', 951.0, -1, 1001, [], {}):
            with self.subTest(score=score):
                self.first_report()['criteria'][0]['score'] = score
                self.assertRejected(self.check(), 'NUMBER')

    def test_nonfinite_json_numbers_are_rejected(self):
        for score in (float('nan'), float('inf'), float('-inf')):
            with self.subTest(score=score):
                self.first_report()['criteria'][0]['score'] = score
                self.assertRejected(self.check(), 'NUMBER')

    def test_missing_criterion_is_rejected(self):
        self.first_report()['criteria'].pop()
        self.first_report()['criteria'][0]['weight'] = 100
        self.assertRejected(self.check(), 'CRITERIA')

    def test_unknown_extra_criterion_is_rejected(self):
        self.first_report()['criteria'][1]['weight'] = 50
        self.first_report()['criteria'].append(dict(id='extra', weight=10, score=1000,
                                                    evidence=['artifacts/novel.txt']))
        self.assertRejected(self.check(), 'CRITERIA')

    def test_duplicate_audit_criterion_is_rejected(self):
        self.first_report()['criteria'].append(copy.deepcopy(self.first_report()['criteria'][0]))
        self.assertRejected(self.check(), 'DUPLICATE: criterion')

    def test_duplicate_manifest_criterion_is_rejected(self):
        self.item['criteria'].append(copy.deepcopy(self.item['criteria'][0]))
        self.assertRejected(self.check(), 'DUPLICATE: criterion')

    def test_criterion_weights_must_match_manifest(self):
        self.first_report()['criteria'][0]['weight'] = 60
        self.first_report()['criteria'][1]['weight'] = 40
        self.assertRejected(self.check(), 'WEIGHTS')

    def test_weight_sum_must_be_exactly_100(self):
        self.item['criteria'][0]['weight'] = 39
        self.assertRejected(self.check(), 'WEIGHTS')

    def test_malformed_weights_are_rejected(self):
        for value in (True, False, '40', None, -1, 0, 101):
            with self.subTest(value=value):
                self.first_report()['criteria'][0]['weight'] = value
                self.assertRejected(self.check(), 'NUMBER')

    def test_fractional_weights_pass_with_exact_sum(self):
        for criteria in [self.item['criteria']] + [r['criteria'] for r in self.reports.values()]:
            criteria[0]['weight'], criteria[1]['weight'] = 40.25, 59.75
        self.assertTrue(self.check()['passed'])

    def test_empty_or_nonstring_evidence_is_rejected(self):
        for evidence in ([], [''], ['   '], [False], ['An unsupported opinion.']):
            with self.subTest(evidence=evidence):
                self.first_report()['criteria'][0]['evidence'] = evidence
                self.assertRejected(self.check())

    def test_evidence_path_must_exist(self):
        self.first_report()['criteria'][0]['evidence'] = ['artifacts/missing.txt#passage']
        self.assertRejected(self.check(), 'EVIDENCE')

    def test_anchor_is_a_reference_not_a_claim_of_truth(self):
        self.first_report()['criteria'][0]['evidence'] = ['artifacts/novel.txt#human-must-check-anchor']
        self.assertTrue(self.check()['passed'])

    def test_empty_anchor_is_rejected(self):
        self.first_report()['criteria'][0]['evidence'] = ['artifacts/novel.txt#']
        self.assertRejected(self.check(), 'EVIDENCE')

    def test_reversed_evidence_line_range_is_rejected(self):
        self.first_report()['criteria'][0]['evidence'] = ['artifacts/novel.txt:L4-L2']
        self.assertRejected(self.check(), 'EVIDENCE')

    def finding(self, status='open', severity='minor'):
        return dict(id='F1', severity=severity, status=status, location='artifacts/novel.txt:L1',
                    description='Synthetic test condition.', remediation='Synthetic action.')

    def test_open_finding_of_any_severity_is_rejected(self):
        for severity in ('critical', 'major', 'minor', 'info', 'custom-severity'):
            with self.subTest(severity=severity):
                self.first_report()['findings'] = [self.finding(severity=severity)]
                self.assertRejected(self.check(), 'FINDING')

    def test_unrecognized_finding_status_is_unresolved(self):
        self.first_report()['findings'] = [self.finding(status='waived')]
        self.assertRejected(self.check(), 'FINDING')

    def test_closed_finding_passes(self):
        self.first_report()['findings'] = [self.finding(status='CLOSED')]
        self.assertTrue(self.check()['passed'])

    def test_duplicate_finding_ids_are_rejected(self):
        self.first_report()['findings'] = [self.finding(status='closed'), self.finding(status='resolved')]
        self.assertRejected(self.check(), 'DUPLICATE')

    def test_bogus_pass_and_released_status_do_not_authorize(self):
        self.item['audits'] = []
        for status in ('PASS', 'RELEASED'):
            with self.subTest(status=status):
                self.item['status'] = status
                self.assertRejected(self.check(), 'AUDITS')

    def test_released_status_can_pass_only_with_valid_current_audits(self):
        self.item['status'] = 'RELEASED'
        self.assertTrue(self.check()['passed'])

    def test_return_verdict_is_rejected(self):
        self.first_report()['verdict'] = 'RETURN'
        self.assertRejected(self.check(), 'VERDICT')

    def test_missing_artifact_file_is_rejected(self):
        (self.root / 'artifacts/novel.txt').unlink()
        self.assertRejected(self.check(), 'FILE')

    def test_missing_audit_file_is_rejected(self):
        self.persist()
        (self.root / 'audits/novel-1.json').unlink()
        self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'FILE')

    def test_single_audit_is_rejected(self):
        self.item['audits'].pop()
        self.assertRejected(self.check(), 'INDEPENDENCE')

    def test_duplicate_audit_ids_are_rejected(self):
        self.reports['audits/novel-2.json']['audit_id'] = self.first_report()['audit_id']
        self.assertRejected(self.check(), 'DUPLICATE: audit_id')

    def test_duplicate_audit_id_across_dependency_is_rejected(self):
        self.dependency()
        self.reports['audits/draft-1.json']['audit_id'] = self.first_report()['audit_id']
        self.assertRejected(self.check(), 'DUPLICATE: audit_id')

    def test_duplicate_deliverable_ids_are_rejected(self):
        self.items.append(copy.deepcopy(self.item))
        self.assertRejected(self.check(), 'DUPLICATE: deliverable')

    def test_duplicate_agent_ids_are_rejected(self):
        self.agents.append(copy.deepcopy(self.agents[0]))
        self.assertRejected(self.check(), 'DUPLICATE: agent_id')

    def test_duplicate_audit_paths_are_rejected(self):
        self.item['audits'].append(self.item['audits'][0])
        self.assertRejected(self.check(), 'DUPLICATE')

    def test_duplicate_manifest_files_are_rejected(self):
        self.item['files'].append(copy.deepcopy(self.item['files'][0]))
        self.assertRejected(self.check(), 'DUPLICATE: file')

    def test_duplicate_audit_files_are_rejected(self):
        self.first_report()['files'].append(copy.deepcopy(self.first_report()['files'][0]))
        self.assertRejected(self.check(), 'DUPLICATE: file')

    def test_extra_audit_file_is_rejected(self):
        self.write('artifacts/extra.txt', 'Extra file.')
        self.first_report()['files'].append(self.file_entry('artifacts/extra.txt'))
        self.assertRejected(self.check(), 'BUNDLE')

    def test_audit_must_include_entire_bundle(self):
        self.first_report()['files'].pop()
        self.assertRejected(self.check(), 'BUNDLE')

    def test_wrong_deliverable_in_audit_is_rejected(self):
        self.first_report()['deliverable_id'] = 'someone-else'
        self.assertRejected(self.check(), 'wrong deliverable')

    def test_bad_audit_schema_and_boolean_version_are_rejected(self):
        for version in (True, False, 0, 1, 3, '2', 2.0):
            with self.subTest(version=version):
                self.first_report()['schema_version'] = version
                self.assertRejected(self.check(), 'NUMBER')

    def test_extra_audit_schema_field_is_rejected(self):
        self.first_report()['approved'] = True
        self.assertRejected(self.check(), 'SCHEMA')

    def test_missing_schema_field_is_rejected(self):
        del self.first_report()['limitations']
        self.assertRejected(self.check(), 'SCHEMA')

    def test_malformed_timestamp_is_rejected(self):
        for stamp in ('yesterday', '2026-09-24', '2026-09-24T12:00:00', '2026-02-30T12:00:00Z'):
            with self.subTest(stamp=stamp):
                self.first_report()['reviewed_at'] = stamp
                self.assertRejected(self.check(), 'reviewed_at')

    def test_policy_cannot_be_weakened_or_use_boolean_numbers(self):
        for field, value in (('threshold_exclusive', 949), ('score_scale', True),
                             ('min_independent_auditors', 1), ('schema_version', True),
                             ('require_all_criteria_above_threshold', False)):
            with self.subTest(field=field):
                original = self.policy[field]
                self.policy[field] = value
                self.assertRejected(self.check(), 'POLICY')
                self.policy[field] = original

    def test_duplicate_json_keys_are_rejected(self):
        self.persist()
        self.write('00_CONDUCERE/policy.json', '{"schema_version":1,"schema_version":1}')
        self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'DUPLICATE: JSON')

    def test_invalid_json_and_non_utf8_json_are_rejected(self):
        self.persist()
        for content in ('{broken', b'\xff'):
            with self.subTest(content=content):
                self.write('00_CONDUCERE/policy.json', content)
                self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'JSON')

    def test_missing_policy_and_registry_are_rejected(self):
        for path in ('00_CONDUCERE/policy.json', '06_REGISTRU/agents.json', '06_REGISTRU/deliverables.json'):
            with self.subTest(path=path):
                self.persist()
                (self.root / path).unlink()
                self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'FILE')

    def test_49999_prose_words_rejected(self):
        self.prose(49999)
        result = self.check()
        self.assertRejected(result, 'WORD_COUNT')
        self.assertEqual(result['word_count'], 49999)

    def test_50000_prose_words_pass(self):
        self.prose(50000)
        result = self.check()
        self.assertTrue(result['passed'], result)
        self.assertEqual(result['word_count'], 50000)

    def test_headings_html_comments_and_whitespace_are_excluded(self):
        self.prose(49999, '# Three extra words\n\nSetext heading words\n===\n'
                   '<!-- hidden\n many extra words -->\n \t \n')
        result = self.check()
        self.assertRejected(result, 'WORD_COUNT')
        self.assertEqual(result['word_count'], 49999)

    def test_unclosed_html_comment_does_not_inflate_word_count(self):
        self.prose(50000, '<!-- never closed\n')
        result = self.check()
        self.assertRejected(result, 'WORD_COUNT')
        self.assertEqual(result['word_count'], 0)

    def test_dialogue_uses_whitespace_token_count(self):
        self.prose(49999)
        with (self.root / 'artifacts/novel.txt').open('a', encoding='utf-8') as stream:
            stream.write('\n—Bună!')
        self.refresh()
        result = self.check()
        self.assertTrue(result['passed'], result)
        self.assertEqual(result['word_count'], 50000)

    def test_only_explicit_prose_paths_are_counted(self):
        self.prose(49999)
        self.write('artifacts/note.md', ' '.join(['unrelated'] * 100))
        self.refresh()
        self.assertRejected(self.check(), 'WORD_COUNT')

    def test_duplicate_prose_path_is_rejected(self):
        self.prose(25000)
        self.item['requirements']['prose_paths'].append('artifacts/novel.txt')
        self.assertRejected(self.check(), 'DUPLICATE')

    def test_prose_path_must_be_in_manifest(self):
        self.prose(50000)
        self.write('artifacts/unlisted.txt', 'Text.')
        self.item['requirements']['prose_paths'] = ['artifacts/unlisted.txt']
        self.assertRejected(self.check(), 'absent from the manifest')

    def test_prose_must_be_utf8_text(self):
        self.prose(50000)
        self.write('artifacts/novel.txt', b'\xff\xfe\x00')
        self.refresh()
        self.assertRejected(self.check(), 'UTF-8')

    def test_prose_extension_must_be_md_or_txt(self):
        self.write('artifacts/novel.csv', ' '.join(['text'] * 50000))
        self.item['files'].append(self.file_entry('artifacts/novel.csv'))
        self.item['requirements'] = dict(prose_paths=['artifacts/novel.csv'])
        self.refresh()
        self.assertRejected(self.check(), '.md or .txt')

    def test_optional_minimum_defaults_to_50000_when_prose_paths_exist(self):
        self.prose(49999)
        del self.item['requirements']['min_prose_words']
        self.assertRejected(self.check(), 'WORD_COUNT')

    def test_smaller_or_boolean_word_minimum_is_rejected(self):
        self.prose(50000)
        for value in (49999, True, '50000', 50000.0):
            with self.subTest(value=value):
                self.item['requirements']['min_prose_words'] = value
                self.assertRejected(self.check(), 'NUMBER')

    def test_minimum_without_prose_paths_is_rejected(self):
        self.item['requirements'] = dict(min_prose_words=50000)
        self.assertRejected(self.check(), 'explicit prose_paths')

    def test_explicit_synopsis_heading_requires_human_review(self):
        self.prose(50000, '# Sinopsis\n')
        self.assertRejected(self.check(), 'HUMAN_REVIEW')

    def test_explicit_chapter_plan_filename_requires_human_review(self):
        self.prose(50000)
        self.write('artifacts/plan_capitole.txt', ' '.join(['text'] * 50000))
        self.item['files'].append(self.file_entry('artifacts/plan_capitole.txt'))
        self.item['requirements']['prose_paths'] = ['artifacts/plan_capitole.txt']
        self.refresh()
        self.assertRejected(self.check(), 'HUMAN_REVIEW')

    def test_manifest_path_traversal_is_rejected(self):
        for path in ('../outside.txt', '..\\outside.txt', 'artifacts/../../outside.txt',
                     'artifacts/../novel.txt', 'C:outside.txt', 'artifacts/novel.txt:stream'):
            with self.subTest(path=path):
                self.item['files'][0]['path'] = path
                self.assertRejected(self.check(), 'PATH')

    def test_audit_path_traversal_is_rejected(self):
        self.item['audits'][0] = '../outside.json'
        self.assertRejected(self.check(), 'PATH')

    def test_audit_bundle_path_traversal_is_rejected(self):
        self.first_report()['files'][0]['path'] = '../outside.txt'
        self.assertRejected(self.check(), 'PATH')

    def test_evidence_path_traversal_is_rejected(self):
        self.first_report()['criteria'][0]['evidence'] = ['../outside.txt#anchor']
        self.assertRejected(self.check(), 'PATH')

    def test_absolute_outside_paths_are_rejected(self):
        outside = self.write('outside.txt', 'Outside root, inside temporary sandbox.', outside=True)
        for path in (str(outside), '/outside.txt', 'D:\\outside.txt', '\\\\server\\share\\outside.txt'):
            with self.subTest(path=path):
                self.item['files'][0]['path'] = path
                self.assertRejected(self.check(), 'PATH')

    def symlink(self, link, target):
        try:
            link.symlink_to(target, target_is_directory=target.is_dir())
        except OSError as exc:
            self.skipTest(f'OS does not permit symlinks: {exc}')

    def test_artifact_symlink_escape_is_rejected(self):
        outside = self.write('outside.txt', 'Outside root.', outside=True)
        link = self.root / 'artifacts/novel.txt'
        link.unlink()
        self.symlink(link, outside)
        self.assertRejected(self.check(), 'escapes ROOT')

    def test_audit_symlink_escape_is_rejected(self):
        self.persist()
        outside = self.write('outside.json', json.dumps(self.first_report()), outside=True)
        link = self.root / 'audits/novel-1.json'
        link.unlink()
        self.symlink(link, outside)
        self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'escapes ROOT')

    def test_policy_symlink_escape_is_rejected(self):
        self.persist()
        outside = self.write('outside.json', json.dumps(self.policy), outside=True)
        link = self.root / '00_CONDUCERE/policy.json'
        link.unlink()
        self.symlink(link, outside)
        self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'escapes ROOT')

    def test_internal_file_alias_cannot_double_count(self):
        self.prose(25000)
        self.symlink(self.root / 'artifacts/alias.txt', self.root / 'artifacts/novel.txt')
        self.item['files'].append(self.file_entry('artifacts/alias.txt'))
        self.item['requirements']['prose_paths'].append('artifacts/alias.txt')
        self.refresh()
        self.assertRejected(self.check(), 'DUPLICATE: physical file')

    def test_hard_link_cannot_double_count(self):
        self.prose(25000)
        try:
            os.link(self.root / 'artifacts/novel.txt', self.root / 'artifacts/alias.txt')
        except OSError as exc:
            self.skipTest(f'OS does not permit hard links: {exc}')
        self.item['files'].append(self.file_entry('artifacts/alias.txt'))
        self.item['requirements']['prose_paths'].append('artifacts/alias.txt')
        self.refresh()
        self.assertRejected(self.check(), 'DUPLICATE: physical file')

    def test_change_during_validation_is_rejected(self):
        self.persist()
        original = gatekeeper.Gatekeeper.verify_unchanged
        def change_then_verify(gate):
            self.write('artifacts/note.md', 'Concurrent change.')
            return original(gate)
        with mock.patch.object(gatekeeper.Gatekeeper, 'verify_unchanged', change_then_verify):
            self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'CHANGED')

    def test_validating_does_not_modify_inputs_or_create_outputs(self):
        self.persist()
        before = {path.relative_to(self.sandbox): path.read_bytes()
                  for path in self.sandbox.rglob('*') if path.is_file()}
        self.assertTrue(gatekeeper.validate(self.root, 'novel')['passed'])
        after = {path.relative_to(self.sandbox): path.read_bytes()
                 for path in self.sandbox.rglob('*') if path.is_file()}
        self.assertEqual(before, after)

    def test_unlisted_directories_and_unrelated_deliverable_files_are_not_read(self):
        child = self.dependency('unrelated')
        self.item['dependencies'] = []
        child['files'][0]['path'] = 'does-not-exist/unrelated.txt'
        self.write('unlisted/broken.json', '{invalid and unreferenced')
        self.assertTrue(self.check()['passed'])

    def test_cli_json_exit_zero_on_pass_and_two_on_reject(self):
        script = str(Path(gatekeeper.__file__).resolve())
        for score, code in ((951, 0), (950, 2)):
            with self.subTest(score=score):
                self.first_report()['criteria'][0]['score'] = score
                self.persist()
                process = subprocess.run(
                    [sys.executable, '-B', script, '--root', str(self.root), '--deliverable', 'novel', '--json'],
                    cwd=self.sandbox, text=True, capture_output=True, check=False)
                self.assertEqual(process.returncode, code, process.stderr + process.stdout)
                result = json.loads(process.stdout)
                self.assertEqual(result['passed'], code == 0)
                self.assertEqual(process.stderr, '')

    def test_cli_text_mode_and_unknown_deliverable(self):
        self.persist()
        with contextlib.redirect_stdout(io.StringIO()) as captured:
            code = gatekeeper.main(['--root', str(self.root), '--deliverable', 'unknown'])
        self.assertEqual(code, 2)
        self.assertIn('RETURN: unknown', captured.getvalue())

    def test_nonexistent_root_is_rejected_without_creating_it(self):
        path = self.sandbox / 'absent'
        self.assertRejected(gatekeeper.validate(path, 'novel'))
        self.assertFalse(path.exists())

    def enable_meta(self):
        self.policy['require_meta_audit'] = True
        reviewer = str(uuid.uuid4())
        self.agents.append(dict(agent_id=reviewer, role='A-QAMANAGER', kind='auditor', active=True))
        self.item['meta_audit'] = '05_AUDIT/meta.json'
        self.persist()
        meta = dict(schema_version=2, deliverable_id='novel', reviewer_agent_id=reviewer,
                    reviewer_role='A-QAMANAGER',
                    audit_files=[self.file_entry(path) for path in self.item['audits']],
                    checks=[dict(id=key, passed=True, evidence=['audits/novel-1.json#check'])
                            for key in ('independence', 'coverage', 'evidence', 'scoring', 'closure', 'version')],
                    findings=[], verdict='PASS', reviewed_at='2026-09-24T12:00:00Z')
        self.reports['05_AUDIT/meta.json'] = meta
        return meta

    def test_meta_valid_passes_without_adding_literary_score(self):
        self.enable_meta()
        result = self.check()
        self.assertTrue(result['passed'], result)
        self.assertEqual(len(result['weighted_scores']), 2)

    def test_meta_missing_when_required_is_rejected(self):
        self.policy['require_meta_audit'] = True
        self.assertRejected(self.check(), 'requires meta_audit')

    def test_meta_missing_file_is_rejected(self):
        self.enable_meta()
        self.persist()
        (self.root / self.item['meta_audit']).unlink()
        self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'FILE')

    def test_meta_stale_report_hash_is_rejected(self):
        self.enable_meta()
        self.first_report()['limitations'] = ['Synthetic report changed after meta review.']
        self.assertRejected(self.check(), 'HASH')

    def test_self_meta_by_ordinary_auditor_is_rejected(self):
        meta = self.enable_meta()
        meta['reviewer_agent_id'] = self.auditor1
        self.assertRejected(self.check(), 'separate from producers and auditors')

    def test_self_meta_by_producer_is_rejected(self):
        meta = self.enable_meta()
        meta['reviewer_agent_id'] = self.producer
        self.assertRejected(self.check(), 'separate from producers and auditors')

    def test_meta_requires_correct_authorized_role(self):
        self.enable_meta()
        self.agents[-1]['role'] = 'language'
        self.assertRejected(self.check(), 'A-QAMANAGER')

    def test_meta_check_false_or_numeric_boolean_is_rejected(self):
        meta = self.enable_meta()
        for value in (False, 1, 'true', None):
            with self.subTest(value=value):
                meta['checks'][0]['passed'] = value
                self.assertRejected(self.check(), 'must explicitly pass')

    def test_meta_missing_check_is_rejected(self):
        meta = self.enable_meta()
        meta['checks'].pop()
        self.assertRejected(self.check(), 'missing checks')

    def test_meta_duplicate_check_is_rejected(self):
        meta = self.enable_meta()
        meta['checks'].append(copy.deepcopy(meta['checks'][0]))
        self.assertRejected(self.check(), 'DUPLICATE: meta check')

    def test_meta_bundle_must_include_both_reports(self):
        meta = self.enable_meta()
        meta['audit_files'].pop()
        self.assertRejected(self.check(), 'exact current audit report bundle')

    def test_meta_open_finding_is_rejected(self):
        meta = self.enable_meta()
        meta['findings'] = [self.finding()]
        self.assertRejected(self.check(), 'findings must be an empty array')

    def test_meta_return_verdict_is_rejected(self):
        meta = self.enable_meta()
        meta['verdict'] = 'RETURN'
        self.assertRejected(self.check(), 'META: verdict must be PASS')

    def test_meta_evidence_must_point_to_real_file(self):
        meta = self.enable_meta()
        meta['checks'][0]['evidence'] = ['missing.txt#evidence']
        self.assertRejected(self.check(), 'EVIDENCE')

    def test_meta_path_traversal_is_rejected(self):
        self.enable_meta()
        self.item['meta_audit'] = '../outside.json'
        self.assertRejected(self.check(), 'PATH')

    def test_meta_policy_flag_must_be_explicit(self):
        del self.policy['require_meta_audit']
        self.assertRejected(self.check(), 'SCHEMA')

    def test_runtime_lifecycle_does_not_invalidate_authorized_historical_audit(self):
        self.write('06_REGISTRU/lifecycle.json', json.dumps({self.auditor1: 'completed', self.auditor2: 'closed'}))
        self.assertTrue(self.check()['passed'])

    def test_weight_sum_is_exact_beyond_decimal_default_precision(self):
        self.persist()
        path = self.root / '06_REGISTRU/deliverables.json'
        data = path.read_text(encoding='utf-8').replace('"weight": 40', '"weight": 40.000000000000000000000000000001')
        self.write('06_REGISTRU/deliverables.json', data)
        self.assertRejected(gatekeeper.validate(self.root, 'novel'), 'WEIGHTS')


class AdversarialR02Tests(unittest.TestCase):
    """TEST-only reproductions of auditor probes; never emit real editorial reports."""

    def setUp(self):
        self.f = GatekeeperTests(methodName='runTest')
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.f.enable_meta()
        self.approve_fixture()

    def approve_fixture(self):
        """Explicit synthetic re-audit, called only when the test intends new approvals."""
        self.f.persist()
        for item in self.f.items:
            if 'meta_audit' not in item:
                continue
            meta = self.f.reports[item['meta_audit']]
            meta['audit_files'] = [self.f.file_entry(path) for path in item['audits']]
            for check in meta['checks']:
                check['evidence'] = [self.f.proof(item['audits'][0] + '#reviewed')]
        self.f.persist(freeze=False)

    def result(self):
        # Crucially, never refresh a contract, evidence digest or approval implicitly.
        return gatekeeper.validate(self.f.root, 'novel')

    def rejected(self, token):
        result = self.result()
        self.assertFalse(result['passed'], result)
        self.assertIn(token, json.dumps(result), result)
        return result

    def parent_reports(self):
        return {path: (self.f.root / path).read_bytes()
                for path in self.f.item['audits'] + [self.f.item['meta_audit']]}

    def add_source(self, key, text):
        child = self.f.dependency(key)
        self.f.write(f'artifacts/{key}.txt', text)
        child['files'] = [self.f.file_entry(f'artifacts/{key}.txt')]
        child['evidence_files'] = [self.f.file_entry('artifacts/novel.txt')]
        for path in child['audits']:
            self.f.reports[path]['files'] = copy.deepcopy(child['files'])
        child['meta_audit'] = f'audits/{key}-meta.json'
        meta = copy.deepcopy(self.f.reports[self.f.item['meta_audit']])
        meta['deliverable_id'] = key
        self.f.reports[child['meta_audit']] = meta
        return child

    def test_F01_P10_retarget_requires_both_new_parent_audits_and_new_meta(self):
        self.add_source('source-v001', 'The protagonist survives.')
        self.add_source('source-v002', 'The protagonist dies.')
        self.f.item['dependencies'] = ['source-v001']
        self.approve_fixture()
        self.assertTrue(self.result()['passed'])
        old_reports = self.parent_reports()
        self.f.item['dependencies'] = ['source-v002']
        self.f.persist(freeze=False)
        self.assertEqual(self.parent_reports(), old_reports)
        self.assertTrue(gatekeeper.validate(self.f.root, 'source-v002')['passed'])
        self.rejected('CONTRACT')
        # Updating only the manifest/contract does not re-audit the parent.
        self.f.freeze_contracts(update_reports=False)
        self.f.persist(freeze=False)
        self.assertEqual(self.parent_reports(), old_reports)
        self.rejected('CONTRACT')
        self.f.first_report()['contract'] = copy.deepcopy(self.f.item['contract'])
        self.f.persist(freeze=False)
        self.rejected('CONTRACT')
        self.f.reports[self.f.item['audits'][1]]['contract'] = copy.deepcopy(self.f.item['contract'])
        self.f.persist(freeze=False)
        self.rejected('CONTRACT')  # metaaudit still binds the previous contract
        self.approve_fixture()
        self.assertTrue(self.result()['passed'])

    def test_F01_same_dependency_ID_new_version_still_invalidates_parent(self):
        child = self.add_source('source', 'Old source.')
        self.approve_fixture()
        old = self.parent_reports()
        child['version_id'] = 'v002'
        self.f.write('artifacts/source.txt', 'New source.')
        child['files'] = [self.f.file_entry('artifacts/source.txt')]
        self.f.freeze_contracts(update_reports=False)
        for path in child['audits']:
            self.f.reports[path].update(version_id='v002', contract=copy.deepcopy(child['contract']),
                                       files=copy.deepcopy(child['files']))
        meta = self.f.reports[child['meta_audit']]
        meta.update(version_id='v002', contract=copy.deepcopy(child['contract']))
        self.f.persist(freeze=False)
        meta['audit_files'] = [self.f.file_entry(path) for path in child['audits']]
        for check in meta['checks']:
            check['evidence'] = [self.f.proof(child['audits'][0] + '#reviewed')]
        self.f.persist(freeze=False)
        self.assertTrue(gatekeeper.validate(self.f.root, 'source')['passed'])
        self.assertEqual(self.parent_reports(), old)
        self.rejected('CONTRACT')

    def test_F01_requirements_cannot_be_relaxed_after_audit(self):
        self.f.item['requirements'] = dict(min_prose_words=50000, prose_paths=['artifacts/novel.txt'])
        self.f.persist(freeze=False)
        self.rejected('CONTRACT')

    def test_F01_policy_change_invalidates_old_contract(self):
        self.f.policy['require_meta_audit'] = False
        self.f.persist(freeze=False)
        self.rejected('CONTRACT')

    def test_F01_parent_contract_bytes_are_hashed_exactly(self):
        path = self.f.item['contract']['path']
        self.f.write(path, (self.f.root / path).read_bytes() + b' ')
        self.rejected('HASH: contract')

    def test_F01_contract_object_cannot_hide_extra_fields(self):
        path = self.f.item['contract']['path']
        contract = json.loads((self.f.root / path).read_bytes())
        contract['approve_without_dependencies'] = True
        self.f.write(path, json.dumps(contract))
        self.f.item['contract']['sha256'] = self.f.file_entry(path)['sha256']
        self.f.persist(freeze=False)
        self.rejected('CONTRACT')

    def test_F01_operational_status_and_audit_list_are_not_self_hashed(self):
        before = gatekeeper.extract_contract(self.f.root, 'novel')
        self.f.item['status'] = 'RELEASED'
        self.f.item['audits'] = []
        del self.f.item['meta_audit']
        self.f.persist(freeze=False)
        self.assertEqual(gatekeeper.extract_contract(self.f.root, 'novel'), before)
        self.rejected('AUDITS')

    def test_extract_contract_API_and_CLI_return_exact_bytes_without_approval(self):
        expected = (self.f.root / self.f.item['contract']['path']).read_bytes()
        actual = gatekeeper.extract_contract(self.f.root, 'novel')
        self.assertEqual(actual, expected)
        process = subprocess.run([sys.executable, '-B', str(Path(gatekeeper.__file__).resolve()),
                                  '--root', str(self.f.root), '--deliverable', 'novel', '--extract-contract'],
                                 cwd=self.f.sandbox, capture_output=True, check=False)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, expected)
        self.assertEqual(process.stderr, b'')
        self.assertNotIn('passed', json.loads(process.stdout))

    def test_extract_contract_bootstrap_needs_no_own_contract_file_or_audits(self):
        self.f.item['audits'] = []
        del self.f.item['meta_audit']
        path = self.f.item['contract']['path']
        (self.f.root / path).unlink()
        self.f.item['contract']['sha256'] = '0' * 64
        self.f.persist(freeze=False)
        payload = gatekeeper.extract_contract(self.f.root, 'novel')
        self.assertEqual(json.loads(payload)['deliverable_id'], 'novel')
        self.assertFalse((self.f.root / path).exists())

    def test_extract_contract_rejects_changed_input(self):
        self.f.write('artifacts/novel.txt', 'Changed.')
        with self.assertRaisesRegex(gatekeeper.Rejection, 'HASH'):
            gatekeeper.extract_contract(self.f.root, 'novel')

    def test_extract_contract_CLI_error_is_exit_2_without_candidate_on_stdout(self):
        self.f.write('artifacts/novel.txt', 'Changed.')
        process = subprocess.run([sys.executable, '-B', str(Path(gatekeeper.__file__).resolve()),
                                  '--root', str(self.f.root), '--deliverable', 'novel', '--extract-contract'],
                                 cwd=self.f.sandbox, capture_output=True, check=False)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, b'')
        self.assertIn(b'HASH', process.stderr)

    def test_F02_P11_changed_evidence_with_identical_reports_is_rejected(self):
        self.f.write('sources/canon.txt', 'The protagonist survives.')
        self.f.item['evidence_files'] = [self.f.file_entry('sources/canon.txt')]
        for path in self.f.item['audits']:
            for criterion in self.f.reports[path]['criteria']:
                criterion['evidence'] = [self.f.proof('sources/canon.txt:L1-L1')]
        self.approve_fixture()
        self.assertTrue(self.result()['passed'])
        old_reports = self.parent_reports()
        self.f.write('sources/canon.txt', 'The protagonist dies.')
        self.assertEqual(self.parent_reports(), old_reports)
        self.rejected('HASH')

    def test_F02_missing_evidence_digest_is_rejected(self):
        del self.f.first_report()['criteria'][0]['evidence'][0]['sha256']
        self.f.persist(freeze=False)
        self.rejected('SCHEMA')

    def test_F02_wrong_evidence_digest_is_rejected(self):
        self.f.first_report()['criteria'][0]['evidence'][0]['sha256'] = '0' * 64
        self.f.persist(freeze=False)
        self.rejected('HASH: evidence')

    def test_F02_existing_unlisted_evidence_is_rejected(self):
        self.f.write('sources/unlisted.txt', 'Exists but is not frozen.')
        self.f.first_report()['criteria'][0]['evidence'] = [self.f.proof('sources/unlisted.txt')]
        self.f.persist(freeze=False)
        self.rejected('source not frozen')

    def test_F02_even_uncited_frozen_evidence_cannot_drift(self):
        self.f.write('sources/frozen.txt', 'Frozen.')
        self.f.item['evidence_files'] = [self.f.file_entry('sources/frozen.txt')]
        self.approve_fixture()
        self.f.write('sources/frozen.txt', 'Changed without citation.')
        self.rejected('HASH')

    def test_F02_paired_MD_can_be_frozen_before_JSON_without_self_hash(self):
        self.f.write('audits/novel-1.md', '# TEST review\nA stable evidence note; no JSON digest.\n')
        self.f.item['evidence_files'] = [self.f.file_entry('audits/novel-1.md')]
        self.f.first_report()['criteria'][0]['evidence'] = [self.f.proof('audits/novel-1.md#review')]
        self.approve_fixture()
        self.assertTrue(self.result()['passed'])
        self.f.write('audits/novel-1.md', '# TEST review\nChanged after JSON review.')
        self.rejected('HASH')

    def test_F02_contract_rejects_own_audit_as_input_without_hash_cycle(self):
        self.f.item['evidence_files'] = [self.f.file_entry(self.f.item['audits'][0])]
        self.f.persist()  # deliberately invalid test construction
        self.rejected('circular')

    def test_F02_contract_rejects_registry_as_input(self):
        self.f.item['evidence_files'] = [self.f.file_entry('06_REGISTRU/deliverables.json')]
        self.f.persist()
        self.rejected('circular')

    def test_F02_meta_evidence_hash_is_not_optional(self):
        meta = self.f.reports[self.f.item['meta_audit']]
        meta['checks'][0]['evidence'][0]['sha256'] = '0' * 64
        self.f.persist(freeze=False)
        self.rejected('HASH: evidence')

    def test_v1_audit_is_never_silently_accepted(self):
        self.f.first_report()['schema_version'] = 1
        self.f.persist(freeze=False)
        self.rejected('schema_version')

    def test_v1_meta_is_never_silently_accepted(self):
        self.f.reports[self.f.item['meta_audit']]['schema_version'] = 1
        self.f.persist(freeze=False)
        self.rejected('schema_version')

    def test_v1_string_evidence_is_never_silently_migrated(self):
        self.f.first_report()['criteria'][0]['evidence'] = ['artifacts/novel.txt:L1']
        self.f.persist(freeze=False)
        self.rejected('SCHEMA')

    def test_v1_policy_and_registry_are_rejected(self):
        self.f.policy['schema_version'] = 1
        self.f.persist(freeze=False)
        self.rejected('POLICY')
        self.f.policy['schema_version'] = 2
        self.f.persist(freeze=False)
        self.f.write('06_REGISTRU/deliverables.json', json.dumps(dict(deliverables=self.f.items)))
        self.rejected('SCHEMA')

    def test_F04_P21_later_Setext_labels_all_refuse_HUMAN_REVIEW(self):
        for label in ('Sinopsis', 'Synopsis', 'Outline', 'Plan de capitole'):
            for underline in ('========', '--------'):
                with self.subTest(label=label, underline=underline):
                    self.f.prose(50000, f'# Manuscript\n\n{label}\n{underline}\n\n')
                    self.approve_fixture()
                    self.rejected('HUMAN_REVIEW')

    def test_F04_later_ordinary_Setext_keeps_exact_word_boundaries(self):
        for words in (49999, 50000):
            with self.subTest(words=words):
                self.f.prose(words, '# Manuscript\n\nAn ordinary title\n========\n\n')
                self.approve_fixture()
                result = self.result()
                self.assertEqual(result['word_count'], words)
                self.assertEqual(result['passed'], words == 50000, result)

    def test_F04_ATX_Setext_share_labels_and_HTML_comments_are_excluded(self):
        atx = gatekeeper.markdown_parts('# Manuscript\n\n## Sinopsis\nword')
        setext = gatekeeper.markdown_parts('# Manuscript\n\nSinopsis\n===\nword')
        self.assertEqual(atx, setext)
        self.f.prose(50000, '<!-- Sinopsis\n===\n-->\n# Manuscript\n')
        self.approve_fixture()
        self.assertTrue(self.result()['passed'])


class SupplementalEvidenceTests(unittest.TestCase):
    """TEST: auditor-created evidence after production freeze, with no contract refresh."""

    def setUp(self):
        self.a = AdversarialR02Tests(methodName='runTest')
        self.a.setUp()
        self.addCleanup(self.a.doCleanups)
        self.f = self.a.f
        self.primary_path = self.f.item['audits'][0]
        self.meta_path = self.f.item['meta_audit']
        self.frozen_contract = (self.f.root / self.f.item['contract']['path']).read_bytes()
        self.frozen_registry = (self.f.root / '06_REGISTRU/deliverables.json').read_bytes()

    def write_report(self, path):
        self.f.write(path, json.dumps(self.f.reports[path]))

    def refresh_meta(self):
        """Explicit TEST metareview of new primary JSONs; never change production input."""
        meta = self.f.reports[self.meta_path]
        meta['audit_files'] = [self.f.file_entry(p) for p in self.f.item['audits']]
        for check in meta['checks']:
            for ref in check['evidence']:
                if ref['path'] in self.f.item['audits']:
                    ref['sha256'] = self.f.file_entry(ref['path'])['sha256']
        self.write_report(self.meta_path)

    def install_supplement(self, role, entries, cite=None):
        path = self.primary_path if role == 'audit' else self.meta_path
        report = self.f.reports[path]
        report['supplemental_evidence_files'] = copy.deepcopy(entries)
        if cite is not None:
            report['criteria' if role == 'audit' else 'checks'][0]['evidence'] = [self.f.proof(cite)]
        self.write_report(path)
        if role == 'audit':
            self.refresh_meta()

    def create_supplement(self, role, cite=True):
        path = 'audits/primary-review.md' if role == 'audit' else '05_AUDIT/meta-review.md'
        self.f.write(path, '# TEST review\nContract SHA256: ' + self.f.item['contract']['sha256'] + '\n')
        self.install_supplement(role, [self.f.file_entry(path)], path + '#review' if cite else None)
        return path

    def result(self):
        return gatekeeper.validate(self.f.root, 'novel')

    def reject(self, token):
        result = self.result()
        self.assertFalse(result['passed'], result)
        self.assertIn(token, json.dumps(result), result)
        return result

    def normal_workflow(self):
        # Contracts and product are already frozen. No JSON reports exist yet.
        for path in self.f.item['audits'] + [self.meta_path]:
            (self.f.root / path).unlink()
        primary_files = []
        for number, path in enumerate(self.f.item['audits'], 1):
            md, log = f'audits/review-{number}.md', f'audits/tests-{number}.txt'
            self.f.write(md, '# TEST independent review\nContract: ' + self.f.item['contract']['sha256'])
            self.f.write(log, 'TEST synthetic observations, not an editorial approval.')
            report = self.f.reports[path]
            report['supplemental_evidence_files'] = [self.f.file_entry(md), self.f.file_entry(log)]
            report['criteria'][0]['evidence'] = [self.f.proof(md + '#review')]
            self.write_report(path)
            primary_files.extend([md, log])
        # Only now is the metaauditor's MD produced, citing already-fixed inputs.
        meta_md = '05_AUDIT/meta-review.md'
        primary_digest = self.f.file_entry(self.primary_path)['sha256']
        self.f.write(meta_md, '# TEST meta review\nPrimary JSON SHA256: ' + primary_digest +
                     '\nContract SHA256: ' + self.f.item['contract']['sha256'])
        meta = self.f.reports[self.meta_path]
        meta['supplemental_evidence_files'] = [self.f.file_entry(meta_md)]
        meta['checks'][0]['evidence'] = [self.f.proof(meta_md + '#review')]
        self.refresh_meta()
        return primary_files + [meta_md]

    def test_normal_freeze_audit_JSON_MD_then_meta_JSON_MD_keeps_contract_exact(self):
        supplements = self.normal_workflow()
        result = self.result()
        self.assertTrue(result['passed'], result)
        self.assertEqual((self.f.root / self.f.item['contract']['path']).read_bytes(), self.frozen_contract)
        self.assertEqual((self.f.root / '06_REGISTRU/deliverables.json').read_bytes(), self.frozen_registry)
        self.assertEqual(gatekeeper.extract_contract(self.f.root, 'novel'), self.frozen_contract)
        self.assertEqual(self.f.item['evidence_files'], [])
        self.assertEqual(len(result['weighted_scores']), 2)
        self.assertTrue(all(path not in {r['path'] for r in result['checked_files']} for path in supplements))

    def test_valid_audit_supplement_is_allowed_after_contract_freeze(self):
        self.create_supplement('audit')
        self.assertTrue(self.result()['passed'])

    def test_valid_meta_supplement_is_allowed_after_primary_JSONs(self):
        self.create_supplement('meta')
        self.assertTrue(self.result()['passed'])

    def test_omitted_or_empty_supplements_preserve_v2_without_extension(self):
        self.assertTrue(self.result()['passed'])
        for role in ('audit', 'meta'):
            self.install_supplement(role, [])
        self.assertTrue(self.result()['passed'])

    def test_audit_supplement_modified_after_audit_is_rejected(self):
        path = self.create_supplement('audit')
        reports = self.a.parent_reports()
        self.f.write(path, 'TEST changed after primary audit and meta.')
        self.assertEqual(self.a.parent_reports(), reports)
        self.reject('HASH: supplemental evidence changed')

    def test_meta_supplement_modified_after_meta_is_rejected(self):
        path = self.create_supplement('meta')
        reports = self.a.parent_reports()
        self.f.write(path, 'TEST changed after meta.')
        self.assertEqual(self.a.parent_reports(), reports)
        self.reject('HASH: supplemental evidence changed')

    def test_unused_supplement_is_still_hash_checked(self):
        for role in ('audit', 'meta'):
            with self.subTest(role=role):
                path = self.create_supplement(role, cite=False)
                self.assertTrue(self.result()['passed'])
                self.f.write(path, 'TEST unused supplement changed.')
                self.reject('HASH: supplemental evidence changed')
                self.create_supplement(role, cite=False)

    def test_missing_supplement_is_rejected_even_if_not_cited(self):
        path = self.create_supplement('audit', cite=False)
        (self.f.root / path).unlink()
        self.reject('FILE')

    def test_update_primary_supplement_and_its_JSON_requires_new_meta(self):
        path = self.create_supplement('audit')
        old_meta = (self.f.root / self.meta_path).read_bytes()
        self.f.write(path, 'TEST new primary observations.')
        report = self.f.reports[self.primary_path]
        report['supplemental_evidence_files'] = [self.f.file_entry(path)]
        report['criteria'][0]['evidence'] = [self.f.proof(path)]
        self.write_report(self.primary_path)
        self.assertEqual((self.f.root / self.meta_path).read_bytes(), old_meta)
        self.reject('HASH: current hash differs')
        self.refresh_meta()
        self.assertTrue(self.result()['passed'])

    def test_existing_undeclared_source_is_not_an_automatic_supplement(self):
        self.f.write('audits/undeclared.md', 'TEST unlisted auditor evidence.')
        self.f.reports[self.primary_path]['criteria'][0]['evidence'] = [self.f.proof('audits/undeclared.md')]
        self.write_report(self.primary_path)
        self.refresh_meta()
        self.reject('EVIDENCE: source not frozen')

    def test_auditor_cannot_inherit_another_auditors_supplement(self):
        path = self.create_supplement('audit')
        other = self.f.item['audits'][1]
        self.f.reports[other]['criteria'][0]['evidence'] = [self.f.proof(path)]
        self.write_report(other)
        self.refresh_meta()
        self.reject('EVIDENCE: source not frozen')

    def test_meta_cannot_inherit_primary_supplement_without_own_declaration(self):
        path = self.create_supplement('audit')
        meta = self.f.reports[self.meta_path]
        meta['checks'][0]['evidence'] = [self.f.proof(path)]
        self.write_report(self.meta_path)
        self.reject('EVIDENCE: source not frozen')
        self.install_supplement('meta', [self.f.file_entry(path)], path)
        self.assertTrue(self.result()['passed'])

    def test_self_JSON_and_contract_and_manifest_cannot_be_supplements(self):
        for role in ('audit', 'meta'):
            for path in ((self.primary_path if role == 'audit' else self.meta_path),
                         self.f.item['contract']['path'], '06_REGISTRU/deliverables.json'):
                with self.subTest(role=role, path=path):
                    self.install_supplement(role, [self.f.file_entry(path)])
                    self.reject('SUPPLEMENTAL: circular')
                    self.install_supplement(role, [])

    def test_audit_cannot_use_sibling_or_future_meta_JSON_as_supplement(self):
        for path in (self.f.item['audits'][1], self.meta_path):
            with self.subTest(path=path):
                self.install_supplement('audit', [self.f.file_entry(path)])
                self.reject('SUPPLEMENTAL: circular')
                self.install_supplement('audit', [])

    def test_no_override_of_frozen_product_path_even_with_identical_digest(self):
        for role in ('audit', 'meta'):
            for digest in (self.f.item['files'][0]['sha256'], '0' * 64):
                with self.subTest(role=role, digest=digest):
                    self.install_supplement(role, [dict(path='artifacts/novel.txt', sha256=digest)])
                    self.reject('SUPPLEMENTAL: duplicate/override')
                    self.install_supplement(role, [])

    def test_meta_cannot_override_audit_files_via_supplement(self):
        self.install_supplement('meta', [self.f.file_entry(self.primary_path)])
        self.reject('SUPPLEMENTAL: duplicate/override')

    def test_duplicate_supplement_paths_are_rejected(self):
        self.f.write('audits/duplicate.md', 'TEST extra.')
        ref = self.f.file_entry('audits/duplicate.md')
        self.install_supplement('audit', [ref, ref])
        self.reject('DUPLICATE: file')

    def test_symlink_alias_of_product_cannot_override_namespace(self):
        alias = self.f.root / 'audits/product-alias.txt'
        self.f.symlink(alias, self.f.root / 'artifacts/novel.txt')
        self.install_supplement('audit', [self.f.file_entry('audits/product-alias.txt')])
        self.reject('SUPPLEMENTAL: alias/override')

    def test_two_supplement_paths_cannot_alias_same_file(self):
        self.f.write('audits/one.md', 'TEST supplemental file.')
        self.f.symlink(self.f.root / 'audits/two.md', self.f.root / 'audits/one.md')
        self.install_supplement('meta', [self.f.file_entry('audits/one.md'), self.f.file_entry('audits/two.md')])
        self.reject('SUPPLEMENTAL: alias/override')

    def test_hardlink_alias_of_own_JSON_is_rejected(self):
        try:
            os.link(self.f.root / self.primary_path, self.f.root / 'audits/self-alias.json')
        except OSError as exc:
            self.skipTest(f'OS does not permit hard links: {exc}')
        self.install_supplement('audit', [self.f.file_entry('audits/self-alias.json')])
        self.reject('SUPPLEMENTAL: circular')

    def test_symlink_alias_of_contract_is_rejected(self):
        self.f.symlink(self.f.root / 'audits/contract-alias.json', self.f.root / self.f.item['contract']['path'])
        self.install_supplement('meta', [self.f.file_entry('audits/contract-alias.json')])
        self.reject('SUPPLEMENTAL: circular')

    def test_external_supplement_paths_are_rejected_even_when_declared(self):
        outside = self.f.write('outside.md', 'TEST outside ROOT.', outside=True)
        for path in ('../outside.md', str(outside)):
            with self.subTest(path=path):
                self.install_supplement('audit', [dict(path=path, sha256='0' * 64)])
                self.reject('PATH')

    def test_symlink_escape_in_supplement_is_rejected(self):
        outside = self.f.write('outside.md', 'TEST outside ROOT.', outside=True)
        self.f.symlink(self.f.root / 'audits/outside.md', outside)
        self.install_supplement('meta', [dict(path='audits/outside.md', sha256='0' * 64)])
        self.reject('escapes ROOT')

    def test_malformed_supplement_declarations_are_rejected(self):
        for value in (None, True, {}, [dict(path='audits/file.md', sha256=True)],
                      [dict(path='audits/file.md', sha256='not-a-hash')],
                      [dict(path='audits/file.md', sha256='0' * 64, extra=True)]):
            with self.subTest(value=value):
                self.install_supplement('meta', value)
                self.reject('SCHEMA')

    def test_supplement_reference_must_use_same_hash_as_declaration(self):
        self.create_supplement('audit')
        self.f.reports[self.primary_path]['criteria'][0]['evidence'][0]['sha256'] = '0' * 64
        self.write_report(self.primary_path)
        self.refresh_meta()
        self.reject('HASH: evidence declaration differs')

    def test_supplements_do_not_contribute_to_prose_word_count(self):
        # Prepare a different TEST product once, then freeze before adding the log.
        self.f.prose(49999)
        self.a.approve_fixture()
        self.f.write('audits/long-log.txt', ' '.join(['TEST'] * 50000))
        self.install_supplement('audit', [self.f.file_entry('audits/long-log.txt')])
        result = self.reject('WORD_COUNT')
        self.assertEqual(result['word_count'], 49999)


if __name__ == '__main__':
    unittest.main()
