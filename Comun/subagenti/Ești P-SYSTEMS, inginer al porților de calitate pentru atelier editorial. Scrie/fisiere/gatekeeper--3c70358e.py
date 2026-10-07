"""SYS-001 r02 / schema 2. TEST staging; read-only editorial gate."""

from __future__ import annotations

import argparse
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re
import sys
import uuid

SCHEMA_VERSION = 2
CONTRACT_FIELDS = ('version_id', 'stage', 'files', 'producer_agent_ids',
                   'required_audit_roles', 'requirements', 'criteria', 'evidence_files')


def json_bytes(value):
    """Deterministic UTF-8 JSON, exact Decimal values, one final LF; no float coercion."""
    def encode(item):
        if isinstance(item, Decimal):
            require(item.is_finite(), 'NUMBER: nonfinite decimal')
            return str(item)
        if isinstance(item, dict):
            return '{' + ','.join(json.dumps(k) + ':' + encode(item[k]) for k in sorted(item)) + '}'
        if isinstance(item, list):
            return '[' + ','.join(encode(v) for v in item) + ']'
        return json.dumps(item, ensure_ascii=True, allow_nan=False)
    return (encode(value) + '\n').encode('utf-8')


def parse_json(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=no_duplicate_keys,
                      parse_float=Decimal, parse_constant=invalid_constant)


def file_reference(value, label):
    shape(value, ('path', 'sha256'), label)
    return dict(path=relative_path(value['path'], label), sha256=hash_string(value['sha256'], label))


def evidence_reference(value, label):
    shape(value, ('path', 'sha256', 'anchor'), label)
    ref = file_reference({k: value[k] for k in ('path', 'sha256')}, label)
    anchor = value['anchor']
    require(isinstance(anchor, str), f'EVIDENCE: anchor must be a string in {label}')
    if anchor.startswith('#'):
        require(bool(anchor[1:].strip()), f'EVIDENCE: empty anchor in {label}')
    elif anchor:
        match = re.fullmatch(r':L([1-9][0-9]*)(?:-L?([1-9][0-9]*))?', anchor)
        require(match is not None, f'EVIDENCE: invalid anchor in {label}')
        require(match.group(2) is None or int(match.group(2)) >= int(match.group(1)),
                f'EVIDENCE: reversed line range in {label}')
    return {**ref, 'anchor': anchor}


def contract_document(item, deliverables, policy_hash):
    """Projection only; excludes own contract reference, status, audits and meta_audit."""
    dependencies = []
    for key in item['dependencies']:
        require(key in deliverables, f'DEPENDENCY: unknown deliverable {key}')
        child = deliverables[key]
        dependencies.append(dict(deliverable_id=key, version_id=child['version_id'],
                                 contract=file_reference(child['contract'], f'{key}/contract')))
    return dict(schema_version=2, deliverable_id=item['id'],
                **{key: item[key] for key in CONTRACT_FIELDS}, dependencies=dependencies,
                policy=dict(path='00_CONDUCERE/policy.json', sha256=policy_hash))


def markdown_parts(content):
    """One bounded Markdown rule for both labels and counting, including later Setext."""
    content = re.sub(r'<!--[\s\S]*?(?:-->|\Z)', '', content.lstrip('\ufeff'))
    lines = content.splitlines()
    labels = [next((line.strip() for line in lines if line.strip()), '')]
    kept, index = [], 0
    while index < len(lines):
        line = lines[index]
        atx = re.match(r'^ {0,3}#{1,6}(?:\s+(.*)|$)', line)
        if atx:
            labels.append((atx.group(1) or '').strip())
            index += 1
        elif (line.strip() and index + 1 < len(lines)
              and re.fullmatch(r' {0,3}(?:=+|-+)\s*', lines[index + 1])):
            labels.append(line.strip())
            index += 2
        else:
            kept.append(line)
            index += 1
    return labels, '\n'.join(kept)


class Rejection(ValueError):
    """An input cannot establish a passing gate."""


def require(condition, message):
    if not condition:
        raise Rejection(message)


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()),
            f"SCHEMA: {label} must be a nonempty string")
    return value


def shape(value, required, label, optional=()):
    require(isinstance(value, dict), f"SCHEMA: {label} must be an object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    require(not missing and not extra,
            f"SCHEMA: {label}: missing={sorted(missing)}, extra={sorted(extra)}")


def array(value, label, minimum=0):
    require(isinstance(value, list) and len(value) >= minimum,
            f"SCHEMA: {label} must be an array with at least {minimum} entries")
    return value


def integer(value, low, high, label):
    require(type(value) is int and low <= value <= high,
            f"NUMBER: {label} must be an integer in {low}..{high}; booleans invalid")
    return value


def weight(value, label):
    require(type(value) in (int, Decimal), f"NUMBER: {label} must be numeric")
    result = Decimal(value)
    require(result.is_finite() and 0 < result <= 100,
            f"NUMBER: {label} must be finite and in (0,100]")
    return result


def agent_uuid(value, label):
    nonempty(value, label)
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise Rejection(f"UUID: {label} must be a registered runtime UUID") from exc
    require(str(parsed) == value and parsed.int != 0,
            f"UUID: {label} must be a canonical non-nil UUID")
    return value


def unique_strings(value, label, minimum=0):
    result = array(value, label, minimum)
    for item in result:
        nonempty(item, label)
    require(len(set(result)) == len(result), f"DUPLICATE: {label}")
    return result


def relative_path(value, label):
    nonempty(value, label)
    win = PureWindowsPath(value)
    require(not win.drive and not win.root and not value.startswith('/'),
            f"PATH: {label} must be relative to ROOT")
    parts = value.replace('\\', '/').split('/')
    require(all(part and part not in ('.', '..') and ':' not in part
                and part == part.strip() and not part.endswith('.')
                and not any(ord(c) < 32 for c in part) for part in parts),
            f"PATH: unsafe path in {label}: {value!r}")
    return '/'.join(parts)


def hash_string(value, label):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-fA-F]{64}', value),
            f"SCHEMA: {label} must be a SHA-256 hexadecimal digest")
    return value.lower()


def file_entries(value, label, minimum=1):
    result = {}
    for entry in array(value, label, minimum):
        shape(entry, ('path', 'sha256'), label)
        path = relative_path(entry['path'], label)
        require(path not in result, f"DUPLICATE: file {path} in {label}")
        result[path] = hash_string(entry['sha256'], label)
    return result


def criterion_entries(value, label, audit=False):
    result = {}
    for entry in array(value, label, 1):
        fields = ('id', 'weight', 'score', 'evidence') if audit else ('id', 'weight')
        shape(entry, fields, label)
        key = nonempty(entry['id'], label)
        require(key not in result, f"DUPLICATE: criterion {key} in {label}")
        weight(entry['weight'], f'{label}/{key}/weight')
        if audit:
            integer(entry['score'], 0, 1000, f'{label}/{key}/score')
            for evidence in array(entry['evidence'], f'{label}/{key}/evidence', 1):
                evidence_reference(evidence, f'{label}/{key}/evidence')
        result[key] = entry
    require(sum((Fraction(x['weight']) for x in result.values()), Fraction(0)) == 100,
            f"WEIGHTS: {label} weights must sum exactly to 100")
    return result


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"DUPLICATE: JSON object key {key}")
        result[key] = value
    return result


def invalid_constant(value):
    raise Rejection(f'NUMBER: invalid JSON constant {value}')


def timestamp(value, label):
    nonempty(value, label)
    require(re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
                         r'(?:\.\d+)?(?:Z|[+-](?:[01]\d|2[0-3]):[0-5]\d)', value),
            f'SCHEMA: {label} requires ISO8601 datetime with timezone')
    try:
        datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError as exc:
        raise Rejection(f'SCHEMA: invalid {label}') from exc


def result_for(deliverable_id):
    return dict(schema_version=2, deliverable_id=deliverable_id, version_id=None, contract=None,
                passed=False, errors=[],
                weighted_scores=[], word_count=None, checked_files=[], dependencies=[])


class Gatekeeper:
    """A fresh instance must be used for each validation; nothing is persisted."""

    def __init__(self, root):
        self.root = Path(root).resolve(strict=True)
        require(self.root.is_dir(), 'ROOT: expected an existing directory')
        self.snapshots = {}
        self.deliverables = {}
        self.agents = {}
        self.producers = set()
        self.audit_ids = {}
        self.results = {}
        self.require_meta_audit = True
        self.verified_contracts = set()

    def resolve(self, rel):
        rel = relative_path(rel, 'file')
        try:
            path = (self.root / rel).resolve(strict=True)
        except (OSError, RuntimeError, ValueError) as exc:
            raise Rejection(f'FILE: cannot resolve {rel}: {exc}') from exc
        require(path.is_relative_to(self.root), f'PATH: {rel} escapes ROOT')
        require(path.is_file(), f'FILE: {rel} is not a regular file')
        return path

    def read(self, rel):
        path = self.resolve(rel)
        try:
            data = path.read_bytes()
        except OSError as exc:
            raise Rejection(f'FILE: cannot read {rel}: {exc}') from exc
        digest = hashlib.sha256(data).hexdigest()
        previous = self.snapshots.get(rel)
        require(previous is None or previous == (path, digest),
                f'CHANGED: {rel} changed during validation')
        self.snapshots[rel] = (path, digest)
        return data

    def document(self, rel):
        try:
            return parse_json(self.read(rel))
        except (UnicodeError, ValueError) as exc:
            raise Rejection(f'JSON: {rel}: {exc}') from exc

    def load(self):
        policy = self.document('00_CONDUCERE/policy.json')
        expected = dict(schema_version=2, threshold_exclusive=950, score_scale=1000,
                        min_independent_auditors=2, require_all_criteria_above_threshold=True)
        shape(policy, (*expected, 'require_meta_audit'), 'policy')
        for key, value in expected.items():
            require(type(policy[key]) is type(value) and policy[key] == value,
                    f'POLICY: {key} must be exactly {value!r}')
        require(type(policy['require_meta_audit']) is bool,
                'POLICY: require_meta_audit must be an explicit boolean')
        self.require_meta_audit = policy['require_meta_audit']

        registry = self.document('06_REGISTRU/agents.json')
        shape(registry, ('agents',), 'agents registry')
        for agent in array(registry['agents'], 'agents', 1):
            shape(agent, ('agent_id', 'role', 'kind', 'active'), 'agent')
            key = agent_uuid(agent['agent_id'], 'agent_id')
            require(key not in self.agents, f'DUPLICATE: agent_id {key}')
            nonempty(agent['role'], 'agent role')
            require(agent['kind'] in ('producer', 'auditor'), 'SCHEMA: invalid agent kind')
            require(type(agent['active']) is bool, 'SCHEMA: active must be boolean')
            self.agents[key] = agent
            if agent['kind'] == 'producer':
                self.producers.add(key)

        registry = self.document('06_REGISTRU/deliverables.json')
        shape(registry, ('schema_version', 'deliverables'), 'deliverables registry v2')
        integer(registry['schema_version'], 2, 2, 'registry schema_version; v1 requires migration')
        for item in array(registry['deliverables'], 'deliverables', 1):
            shape(item, ('id', 'stage', 'status', 'files', 'producer_agent_ids',
                         'required_audit_roles', 'dependencies', 'requirements',
                         'criteria', 'audits', 'version_id', 'contract', 'evidence_files'),
                  'deliverable v2', ('meta_audit',))
            key = nonempty(item['id'], 'deliverable id')
            require(key not in self.deliverables, f'DUPLICATE: deliverable id {key}')
            nonempty(item['stage'], f'{key}/stage')
            nonempty(item['status'], f'{key}/status')
            nonempty(item['version_id'], f'{key}/version_id')
            file_reference(item['contract'], f'{key}/contract')
            file_entries(item['files'], f'{key}/files')
            file_entries(item['evidence_files'], f'{key}/evidence_files', minimum=0)
            criterion_entries(item['criteria'], f'{key}/criteria')
            for producer in unique_strings(item['producer_agent_ids'], f'{key}/producers', 1):
                agent_uuid(producer, 'producer_agent_id')
                require(producer in self.agents, f'AGENT: unknown producer {producer}')
                agent = self.agents[producer]
                require(agent['kind'] == 'producer' and agent['active'],
                        f'AGENT: producer {producer} must be active and registered as producer')
                self.producers.add(producer)
            unique_strings(item['required_audit_roles'], f'{key}/required_audit_roles', 2)
            unique_strings(item['dependencies'], f'{key}/dependencies')
            audit_paths = [relative_path(p, f'{key}/audits')
                           for p in unique_strings(item['audits'], f'{key}/audits')]
            require(len(set(audit_paths)) == len(audit_paths), f'DUPLICATE: {key}/audit paths')
            if 'meta_audit' in item:
                relative_path(item['meta_audit'], f'{key}/meta_audit')
            req = item['requirements']
            shape(req, (), f'{key}/requirements', ('min_prose_words', 'prose_paths'))
            if 'min_prose_words' in req:
                minimum = req['min_prose_words']
                require(type(minimum) is int and minimum >= 50000,
                        f'NUMBER: {key}/min_prose_words must be an integer >= 50000')
                require('prose_paths' in req, f'PROSE: {key} requires explicit prose_paths')
            if 'prose_paths' in req:
                paths = [relative_path(p, f'{key}/prose_paths')
                         for p in unique_strings(req['prose_paths'], f'{key}/prose_paths', 1)]
                require(len(paths) == len(set(paths)), f'DUPLICATE: {key}/prose_paths')
            self.deliverables[key] = item

    def inputs(self, item):
        """Verify all frozen evidence, including uncited files, and reject hash cycles."""
        protected = ['06_REGISTRU/deliverables.json', item['contract']['path'],
                     *item['audits']]
        if 'meta_audit' in item:
            protected.append(item['meta_audit'])
        forbidden = {(self.root / relative_path(p, 'protected path')).resolve() for p in protected}
        for path in forbidden:
            require(path.is_relative_to(self.root), 'PATH: protected report/contract path escapes ROOT')
        for entry in item['files'] + item['evidence_files']:
            resolved = self.resolve(entry['path'])
            require(resolved not in forbidden, f'CONTRACT: circular input/report reference {entry["path"]}')
            for path in forbidden:
                if path.is_file():
                    require(not resolved.samefile(path), f'CONTRACT: circular file alias {entry["path"]}')
        return self.bundle(item['files'] + item['evidence_files'], f'{item["id"]}/frozen inputs')

    def expected_contract(self, item):
        return contract_document(item, self.deliverables,
                                 self.snapshots['00_CONDUCERE/policy.json'][1])

    def verify_contract(self, key, stack=()):
        require(key not in stack, f'CYCLE: contract dependency {stack + (key,)}')
        if key in self.verified_contracts:
            return
        require(key in self.deliverables, f'DEPENDENCY: unknown deliverable {key}')
        item = self.deliverables[key]
        ref = file_reference(item['contract'], f'{key}/contract')
        actual = self.document(ref['path'])
        require(self.snapshots[ref['path']][1] == ref['sha256'], f'HASH: contract changed for {key}')
        require(json_bytes(actual) == json_bytes(self.expected_contract(item)),
                f'CONTRACT: current inputs/dependencies differ from frozen contract for {key}')
        self.inputs(item)
        for child in item['dependencies']:
            self.verify_contract(child, stack + (key,))
        self.verified_contracts.add(key)

    def report_contract(self, report, item, label):
        require(report.get('version_id') == item['version_id'], f'CONTRACT: wrong version in {label}')
        require(file_reference(report.get('contract'), label) == file_reference(item['contract'], label),
                f'CONTRACT: old or different audited contract in {label}')
        self.verify_contract(item['id'])

    def bundle(self, entries, label, result=None):
        manifest = file_entries(entries, label)
        physical = set()
        payloads = {}
        for rel, expected in manifest.items():
            data = self.read(rel)
            path, actual = self.snapshots[rel]
            identity = path.stat()
            # Detect aliases including hard links, case aliases and internal symlinks.
            identity = (identity.st_dev, identity.st_ino)
            require(identity not in physical, f'DUPLICATE: physical file in {label}: {rel}')
            physical.add(identity)
            if result is not None:
                result['checked_files'].append(dict(path=rel, sha256=actual))
            require(expected == actual, f'HASH: current hash differs for {rel} in {label}')
            payloads[rel] = data
        return manifest, payloads

    def evidence(self, reference, label, allowed):
        ref = evidence_reference(reference, label)
        rel = ref['path']
        require(rel in allowed, f'EVIDENCE: source not frozen in contract or declared by this report: {rel}')
        require(ref['sha256'] == allowed[rel], f'HASH: evidence declaration differs for {rel}')
        data = self.read(rel)
        require(hashlib.sha256(data).hexdigest() == ref['sha256'], f'HASH: evidence changed: {rel}')

    def supplemental_evidence(self, report, item, report_path, base):
        """Extend only this report's evidence namespace, without changing its contract.

        All supplements are verified, including uncited ones. Redundant declarations
        are rejected, even with the same digest; no lexical or physical override.
        Report JSONs, own contract and operational manifest cannot become supplements.
        """
        label = f'{report_path}/supplemental_evidence_files'
        supplements = file_entries(report.get('supplemental_evidence_files', []), label, 0)
        allowed = dict(base)
        if not supplements:
            return allowed
        protected_names = [report_path, item['contract']['path'],
                           '06_REGISTRU/deliverables.json', *item['audits']]
        if 'meta_audit' in item:
            protected_names.append(item['meta_audit'])
        protected = {(self.root / relative_path(name, label)).resolve() for name in protected_names}
        protected_identities = set()
        for path in protected:
            require(path.is_relative_to(self.root), f'PATH: protected supplemental target escapes ROOT: {path}')
            if path.is_file():
                info = path.stat()
                protected_identities.add((info.st_dev, info.st_ino))
        identities = {}
        for rel in base:
            info = self.resolve(rel).stat()
            identities[(info.st_dev, info.st_ino)] = rel
        for rel, expected in supplements.items():
            require(rel not in allowed, f'SUPPLEMENTAL: duplicate/override of declared path: {rel}')
            path = self.resolve(rel)
            info = path.stat()
            identity = (info.st_dev, info.st_ino)
            require(path not in protected and identity not in protected_identities,
                    f'SUPPLEMENTAL: circular report/contract/manifest reference: {rel}')
            require(identity not in identities,
                    f'SUPPLEMENTAL: alias/override of {identities.get(identity)}: {rel}')
            data = self.read(rel)
            require(hashlib.sha256(data).hexdigest() == expected,
                    f'HASH: supplemental evidence changed: {rel}')
            identities[identity] = rel
            allowed[rel] = expected
        return allowed

    def audit(self, rel, item, manifest, seen_reviewers, seen_roles, result):
        audit = self.document(rel)
        shape(audit, ('schema_version', 'audit_id', 'deliverable_id', 'reviewer_agent_id',
                      'reviewer_role', 'files', 'criteria', 'findings', 'verdict',
                      'limitations', 'reviewed_at', 'version_id', 'contract'), f'audit v2 {rel}',
              ('supplemental_evidence_files',))
        integer(audit['schema_version'], 2, 2, 'audit schema_version; v1 requires re-audit')
        audit_id = nonempty(audit['audit_id'], 'audit_id')
        require(audit_id not in self.audit_ids, f'DUPLICATE: audit_id {audit_id}')
        self.audit_ids[audit_id] = rel
        require(audit['deliverable_id'] == item['id'], f'AUDIT: wrong deliverable in {rel}')
        reviewer = agent_uuid(audit['reviewer_agent_id'], 'reviewer_agent_id')
        require(reviewer not in self.producers, f'INDEPENDENCE: producer cannot audit: {reviewer}')
        require(reviewer in self.agents, f'AGENT: unregistered auditor {reviewer}')
        agent = self.agents[reviewer]
        require(agent['active'] and agent['kind'] == 'auditor',
                f'AGENT: {reviewer} must be an active auditor')
        role = nonempty(audit['reviewer_role'], 'reviewer_role')
        require(role == agent['role'], f'ROLE: reviewer role differs from registry in {rel}')
        require(reviewer not in seen_reviewers, f'DUPLICATE: auditor {reviewer}')
        seen_reviewers.add(reviewer)
        self.report_contract(audit, item, rel)

        audit_manifest, _ = self.bundle(audit['files'], f'audit {rel}/files')
        require(audit_manifest == manifest, f'BUNDLE: {rel} must cover the exact complete manifest')
        allowed = self.supplemental_evidence(
            audit, item, rel, {**manifest, **file_entries(item['evidence_files'], 'evidence_files', 0)})
        expected = criterion_entries(item['criteria'], 'manifest criteria')
        actual = criterion_entries(audit['criteria'], f'audit {rel}/criteria', audit=True)
        require(actual.keys() == expected.keys(), f'CRITERIA: IDs must exactly match in {rel}')
        for key, entry in actual.items():
            require(Decimal(entry['weight']) == Decimal(expected[key]['weight']),
                    f'WEIGHTS: criterion {key} differs from manifest in {rel}')
            for reference in entry['evidence']:
                self.evidence(reference, f'{rel}/{key}', allowed)

        finding_ids = set()
        for finding in array(audit['findings'], f'{rel}/findings'):
            shape(finding, ('id', 'severity', 'status', 'location', 'description', 'remediation'),
                  f'{rel}/finding')
            for key, value in finding.items():
                nonempty(value, f'{rel}/finding/{key}')
            require(finding['id'] not in finding_ids, f'DUPLICATE: finding ID in {rel}')
            finding_ids.add(finding['id'])
            require(finding['status'].casefold() in ('closed', 'resolved'),
                    f'FINDING: unresolved {finding["severity"]} finding {finding["id"]} in {rel}')
        for limitation in array(audit['limitations'], f'{rel}/limitations'):
            nonempty(limitation, f'{rel}/limitation')
        timestamp(audit['reviewed_at'], f'{rel}/reviewed_at')
        require(audit['verdict'] in ('PASS', 'RETURN'), f'SCHEMA: invalid verdict in {rel}')

        # Descriptive arithmetic over supplied scores, never a generated editorial rating.
        score = sum((Fraction(x['score']) * Fraction(x['weight']) for x in actual.values()),
                    Fraction(0)) / 100
        result['weighted_scores'].append(dict(audit_id=audit_id, reviewer_agent_id=reviewer,
                                             reviewer_role=role, score=float(score)))
        failed = [key for key, entry in actual.items() if entry['score'] <= 950]
        require(not failed, f'THRESHOLD: every criterion must be >950 in {rel}; rejected={failed}')
        require(audit['verdict'] == 'PASS', f'VERDICT: {rel} returned the deliverable')
        seen_roles.add(role)

    def meta_audit(self, item, reviewers):
        if 'meta_audit' not in item:
            require(not self.require_meta_audit, f'META: {item["id"]} requires meta_audit')
            return
        rel = relative_path(item['meta_audit'], 'meta_audit')
        meta = self.document(rel)
        shape(meta, ('schema_version', 'deliverable_id', 'reviewer_agent_id', 'reviewer_role',
                     'audit_files', 'checks', 'findings', 'verdict', 'reviewed_at', 'version_id',
                     'contract'), f'meta v2 {rel}', ('supplemental_evidence_files',))
        integer(meta['schema_version'], 2, 2, 'meta schema_version; v1 requires re-audit')
        require(meta['deliverable_id'] == item['id'], f'META: wrong deliverable in {rel}')
        reviewer = agent_uuid(meta['reviewer_agent_id'], 'meta reviewer_agent_id')
        require(reviewer not in self.producers and reviewer not in reviewers,
                f'META: metaauditor must be separate from producers and auditors: {reviewer}')
        require(reviewer in self.agents, f'META: unregistered metaauditor {reviewer}')
        agent = self.agents[reviewer]
        require(agent['kind'] == 'auditor' and agent['active']
                and agent['role'] == 'A-QAMANAGER' and meta['reviewer_role'] == 'A-QAMANAGER',
                'META: an authorized registered A-QAMANAGER auditor is required')
        self.report_contract(meta, item, rel)
        expected = {}
        for original in item['audits']:
            path = relative_path(original, 'meta audit_files')
            expected[path] = hashlib.sha256(self.read(path)).hexdigest()
        actual, _ = self.bundle(meta['audit_files'], f'{rel}/audit_files')
        require(actual == expected, f'META: exact current audit report bundle required in {rel}')
        allowed = self.supplemental_evidence(
            meta, item, rel, {**file_entries(item['files'], 'files'),
                             **file_entries(item['evidence_files'], 'evidence_files', 0), **expected})
        checks = set()
        for check in array(meta['checks'], 'meta checks', 1):
            shape(check, ('id', 'passed', 'evidence'), 'meta check')
            key = nonempty(check['id'], 'meta check id')
            require(key not in checks, f'DUPLICATE: meta check {key}')
            checks.add(key)
            require(check['passed'] is True, f'META: check {key} must explicitly pass')
            for evidence in array(check['evidence'], f'meta/{key}/evidence', 1):
                self.evidence(evidence, f'meta/{key}', allowed)
        missing = {'independence', 'coverage', 'evidence', 'scoring', 'closure', 'version'} - checks
        require(not missing, f'META: missing checks {sorted(missing)}')
        require(isinstance(meta['findings'], list) and not meta['findings'],
                'META: findings must be an empty array')
        require(meta['verdict'] == 'PASS', 'META: verdict must be PASS')
        timestamp(meta['reviewed_at'], 'meta reviewed_at')

    def prose(self, item, manifest, payloads, result):
        req = item['requirements']
        if 'prose_paths' not in req:
            return
        total = 0
        # Only explicit labels are detectable; editorial genre/content requires human review.
        plan_label = re.compile(
            r'^(?:synopsis|sinopsis|outline|chapter[ _-]*plans?|'
            r'plan(?:uri)?[ _-]+(?:(?:de|pe)[ _-]+)?capitol(?:e|elor)?)(?:$|[ _:\-])',
            re.IGNORECASE)
        for original in req['prose_paths']:
            rel = relative_path(original, 'prose_paths')
            require(rel in manifest, f'PROSE: {rel} is absent from the manifest')
            require(Path(rel).suffix.lower() in ('.md', '.txt'),
                    f'PROSE: {rel} must be UTF-8 .md or .txt')
            try:
                content = payloads[rel].decode('utf-8')
            except UnicodeError as exc:
                raise Rejection(f'PROSE: invalid UTF-8 in {rel}') from exc
            require('\x00' not in content, f'PROSE: binary NUL in {rel}')
            require(not any(plan_label.match(Path(part).stem) for part in rel.split('/')),
                    f'HUMAN_REVIEW: plan/synopsis marked as prose: {rel}')
            labels, narrative = markdown_parts(content)
            require(not any(plan_label.match(label) for label in labels),
                    f'HUMAN_REVIEW: plan/synopsis label in {rel}')
            total += len(narrative.split())
        result['word_count'] = total
        minimum = req.get('min_prose_words', 50000)
        require(total >= minimum, f'WORD_COUNT: {total} < required {minimum}')

    def visit(self, key, stack):
        if key in stack:
            result = result_for(key)
            result['errors'].append('CYCLE: ' + ' -> '.join(stack + [key]))
            return result
        if key in self.results:
            return self.results[key]
        result = result_for(key)
        self.results[key] = result
        if key not in self.deliverables:
            result['errors'].append(f'DEPENDENCY: unknown deliverable {key}')
            return result
        item = self.deliverables[key]
        result['version_id'] = item['version_id']
        result['contract'] = file_reference(item['contract'], 'contract')
        for dependency in item['dependencies']:
            child = self.visit(dependency, stack + [key])
            result['dependencies'].append(child)
            if not child['passed']:
                result['errors'].append(f'DEPENDENCY: {dependency} did not pass')

        try:
            manifest, payloads = self.bundle(item['files'], f'{key}/files', result)
            self.verify_contract(key)
        except (Rejection, OSError) as exc:
            result['errors'].append(str(exc))
            return result
        try:
            self.prose(item, manifest, payloads, result)
        except Rejection as exc:
            result['errors'].append(str(exc))

        reviewers, roles, physical_audits = set(), set(), set()
        if not item['audits']:
            result['errors'].append(f'AUDITS: missing audit reports for {key}')
        for original in item['audits']:
            rel = relative_path(original, f'{key}/audit path')
            try:
                stat = self.resolve(rel).stat()
                identity = (stat.st_dev, stat.st_ino)
                require(identity not in physical_audits, f'DUPLICATE: physical audit report {rel}')
                physical_audits.add(identity)
                self.audit(rel, item, manifest, reviewers, roles, result)
            except (Rejection, OSError) as exc:
                result['errors'].append(f'{rel}: {exc}')
        if len(reviewers) < 2:
            result['errors'].append('INDEPENDENCE: at least two distinct registered auditors required')
        missing = set(item['required_audit_roles']) - roles
        if missing:
            result['errors'].append(f'ROLES: missing passing audits for {sorted(missing)}')
        try:
            self.meta_audit(item, reviewers)
        except (Rejection, OSError) as exc:
            result['errors'].append(str(exc))
        result['passed'] = not result['errors']
        return result

    def verify_unchanged(self):
        errors = []
        for rel, (expected_path, expected_hash) in self.snapshots.items():
            try:
                path = self.resolve(rel)
                actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
                require(path == expected_path and actual_hash == expected_hash,
                        f'CHANGED: {rel} changed during validation')
            except (Rejection, OSError) as exc:
                errors.append(str(exc))
        return errors


def validate(root, deliverable_id):
    """Return the public result contract. Do not write files or change states."""
    result = result_for(deliverable_id)
    try:
        nonempty(deliverable_id, 'deliverable_id')
        gate = Gatekeeper(root)
        gate.load()
        result = gate.visit(deliverable_id, [])
        changed = gate.verify_unchanged()
        if changed:
            # Any concurrent change invalidates the entire checked dependency graph.
            for checked in gate.results.values():
                checked['passed'] = False
                checked['errors'].extend(changed)
        result['passed'] = not result['errors']
    except (Rejection, OSError, ValueError, RuntimeError, RecursionError) as exc:
        result['errors'].append(f'REJECT: {exc}')
        result['passed'] = False
    return result


def extract_contract(root, deliverable_id):
    """Return exact candidate contract bytes; no audits/scores/writes. Not an approval.

    The item's own contract reference may be a syntactically valid placeholder.
    Dependencies must already have frozen, consistent contracts (but need no audits).
    """
    gate = Gatekeeper(root)
    gate.load()
    require(deliverable_id in gate.deliverables, f'CONTRACT: unknown deliverable {deliverable_id}')
    item = gate.deliverables[deliverable_id]
    gate.inputs(item)
    for child in item['dependencies']:
        gate.verify_contract(child, (deliverable_id,))
    data = json_bytes(gate.expected_contract(item))
    changed = gate.verify_unchanged()
    require(not changed, 'CHANGED: ' + '; '.join(changed))
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, help='Editorial workspace ROOT')
    parser.add_argument('--deliverable', required=True, help='Registered deliverable ID')
    parser.add_argument('--json', action='store_true', help='Emit only the JSON result')
    parser.add_argument('--extract-contract', action='store_true',
                        help='Emit exact contract UTF-8 bytes to stdout, not an approval')
    args = parser.parse_args(argv)
    if args.extract_contract:
        try:
            data = extract_contract(args.root, args.deliverable)
            sys.stdout.buffer.write(data)
            return 0
        except (Rejection, OSError, ValueError, RuntimeError) as exc:
            print(f'RETURN: {exc}', file=sys.stderr)
            return 2
    result = validate(args.root, args.deliverable)
    if args.json:
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    else:
        print(f'{"PASS" if result["passed"] else "RETURN"}: {result["deliverable_id"]}')
        def show_errors(node, prefix=''):
            for error in node['errors']:
                print(f'{prefix}- {error}')
            for child in node['dependencies']:
                print(f'{prefix}Dependency {child["deliverable_id"]}:')
                show_errors(child, prefix + '  ')
        show_errors(result)
        if result['word_count'] is not None:
            print(f'Word count: {result["word_count"]}')
    return 0 if result['passed'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
