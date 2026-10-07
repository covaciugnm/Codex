"""SYS-001 r02 / TEST staging. Snapshots and explicit preservation of rejections."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

# Running the utility must not create an import cache outside 08_ARHIVA.
sys.dont_write_bytecode = True
from gatekeeper import (Gatekeeper, Rejection, array, file_entries, file_reference,
                        evidence_reference, nonempty, relative_path, require, shape,
                        integer, json_bytes, parse_json, hash_string, result_for)


def safe_component(value):
    nonempty(value, 'archive identifier')
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,99}', value)
            and not value.endswith('.'),
            'PATH: archive identifiers require 1..100 ASCII letters/digits/._-, '
            'starting with a letter/digit, without a final dot')
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'CONIN$', 'CONOUT$'}
    reserved.update(f'{prefix}{n}' for prefix in ('COM', 'LPT') for n in range(1, 10))
    require(value.split('.')[0].upper() not in reserved,
            f'PATH: reserved Windows name: {value}')
    return value


def is_link_or_reparse(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0))


def checked_directory(root, path, create=False):
    """Only exact descendants, no symlink/junction destination components."""
    require(path.is_relative_to(root), f'PATH: archive destination escapes ROOT: {path}')
    current = root
    for part in path.relative_to(root).parts:
        current = current / part
        if not os.path.lexists(current):
            require(create, f'PATH: archive directory does not exist: {current}')
            try:
                current.mkdir()
            except FileExistsError:
                pass
        require(not is_link_or_reparse(current), f'PATH: archive destination is a link: {current}')
        require(current.is_dir() and current.resolve(strict=True).is_relative_to(root),
                f'PATH: invalid archive directory: {current}')
    return path


def archive(root, deliverable_id, round_id, result_path=None, extras=(), preserve_rejected=False):
    """Snapshot explicit inputs. Never promote a verdict or modify source files.

    Returns operation metadata; raises Rejection on invalid input. Existing rounds
    are never reused, including incomplete rounds left by interrupted writes.
    """
    safe_component(deliverable_id)
    safe_component(round_id)
    gate = Gatekeeper(root)
    if preserve_rejected:
        return archive_rejected(gate, deliverable_id, round_id, result_path, extras)
    gate.load()
    require(deliverable_id in gate.deliverables, f'ARCHIVE: unknown deliverable {deliverable_id}')
    destination = gate.root / '08_ARHIVA' / deliverable_id / round_id
    require(not os.path.lexists(destination), f'EXISTS: round already exists: {destination}')
    # Preflight existing destination ancestors before collecting any payloads.
    for parent in (gate.root / '08_ARHIVA', destination.parent):
        if os.path.lexists(parent):
            checked_directory(gate.root, parent)

    payloads = {}
    kinds = {}

    def source(rel, kind):
        rel = relative_path(rel, 'archive source')
        resolved = gate.resolve(rel)
        archive_root = gate.root / '08_ARHIVA'
        require(not resolved.is_relative_to(archive_root),
                f'PATH: a snapshot cannot ingest the archive tree: {rel}')
        data = gate.read(rel)
        target = 'sources/' + rel
        require(target not in payloads or payloads[target] == data,
                f'CHANGED: conflicting snapshot source {rel}')
        payloads[target] = data
        kinds.setdefault(target, kind)
        return data

    for rel in ('00_CONDUCERE/policy.json', '06_REGISTRU/agents.json', '06_REGISTRU/deliverables.json'):
        source(rel, 'registry_or_policy')

    visited = set()
    dependency_ids = []

    def collect(identifier):
        if identifier in visited:
            return  # A rejected cyclic graph can still have an archival snapshot.
        require(identifier in gate.deliverables, f'ARCHIVE: missing dependency {identifier}')
        visited.add(identifier)
        item = gate.deliverables[identifier]
        gate.verify_contract(identifier)
        manifest, _ = gate.bundle(item['files'], f'{identifier}/files')
        target = 'manifest.json' if identifier == deliverable_id else (
            'dependency_manifests/' + safe_component(identifier) + '.json')
        payloads[target] = json_bytes(item)
        kinds[target] = 'deliverable_manifest'
        for rel in manifest:
            source(rel, 'artifact')
        source(item['contract']['path'], 'frozen_contract')
        for rel in file_entries(item['evidence_files'], 'evidence_files', 0):
            source(rel, 'evidence_source')
        for original in item['audits']:
            rel = relative_path(original, f'{identifier}/audit')
            report = gate.document(rel)
            require(isinstance(report, dict), f'ARCHIVE: audit must be a JSON object: {rel}')
            require(report.get('deliverable_id') == identifier,
                    f'ARCHIVE: audit deliverable_id mismatch: {rel}')
            integer(report.get('schema_version'), 2, 2, f'{rel}/schema_version')
            gate.report_contract(report, item, rel)
            # Do not require a passing score/verdict or closed findings for preservation.
            # Every claimed artifact digest must nevertheless match the actual bundle.
            audited = file_entries(report.get('files'), f'{rel}/files')
            gate.bundle(report['files'], f'{rel}/files')
            require(audited == manifest, f'BUNDLE: audit must match exact current manifest: {rel}')
            allowed = gate.supplemental_evidence(
                report, item, rel, {**manifest, **file_entries(item['evidence_files'], 'evidence_files', 0)})
            for supplement in file_entries(report.get('supplemental_evidence_files', []),
                                           f'{rel}/supplemental_evidence_files', 0):
                source(supplement, 'supplemental_evidence_source')
            for criterion in array(report.get('criteria'), 'criteria', 1):
                require(isinstance(criterion, dict), 'SCHEMA: criterion must be object')
                for evidence in array(criterion.get('evidence'), 'evidence', 1):
                    gate.evidence(evidence, rel, allowed)
            source(rel, 'audit_report')
        if 'meta_audit' in item:
            rel = relative_path(item['meta_audit'], 'meta_audit')
            meta = gate.document(rel)
            require(isinstance(meta, dict) and meta.get('deliverable_id') == identifier,
                    f'ARCHIVE: meta deliverable_id mismatch: {rel}')
            integer(meta.get('schema_version'), 2, 2, f'{rel}/schema_version')
            gate.report_contract(meta, item, rel)
            actual, _ = gate.bundle(meta.get('audit_files'), f'{rel}/audit_files')
            expected = {relative_path(path, 'audit path'): hashlib.sha256(
                gate.read(relative_path(path, 'audit path'))).hexdigest() for path in item['audits']}
            require(actual == expected, f'HASH: meta must cover exact current reports: {rel}')
            allowed = gate.supplemental_evidence(
                meta, item, rel, {**manifest, **file_entries(item['evidence_files'], 'evidence_files', 0),
                                 **expected})
            for supplement in file_entries(meta.get('supplemental_evidence_files', []),
                                           f'{rel}/supplemental_evidence_files', 0):
                source(supplement, 'supplemental_evidence_source')
            for check in array(meta.get('checks'), 'checks', 1):
                require(isinstance(check, dict), 'SCHEMA: check must be object')
                for evidence in array(check.get('evidence'), 'evidence', 1):
                    gate.evidence(evidence, rel, allowed)
            source(rel, 'meta_audit_report')
        for dependency in item['dependencies']:
            if dependency not in visited:
                dependency_ids.append(dependency)
            collect(dependency)

    collect(deliverable_id)
    extra_paths = set()
    for original in extras:
        rel = relative_path(original, '--extra')
        require(rel not in extra_paths, f'DUPLICATE: --extra {rel}')
        extra_paths.add(rel)
        source(rel, 'extra')
    if result_path is not None:
        rel = relative_path(result_path, '--result')
        result = gate.document(rel)
        shape(result, result_for(deliverable_id), '--result v2')
        integer(result['schema_version'], 2, 2, 'result schema_version')
        require(result['deliverable_id'] == deliverable_id and type(result['passed']) is bool,
                'ARCHIVE: result requires matching deliverable_id and boolean passed')
        gate.report_contract(result, gate.deliverables[deliverable_id], '--result')
        # Preserve caller-supplied bytes, explicitly without certifying the supplied verdict.
        payloads['result.json'] = source(rel, 'supplied_result')
        kinds['result.json'] = 'supplied_result_copy'

    return write_snapshot(gate, deliverable_id, round_id, payloads, kinds,
                          archive_kind='round_snapshot', source_consistency='verified',
                          result_provided=result_path is not None, dependencies=dependency_ids)


def write_snapshot(gate, deliverable_id, round_id, payloads, kinds, **metadata):
    destination = gate.root / '08_ARHIVA' / deliverable_id / round_id
    require(not os.path.lexists(destination), f'EXISTS: round already exists: {destination}')
    for parent in (gate.root / '08_ARHIVA', destination.parent):
        if os.path.lexists(parent):
            checked_directory(gate.root, parent)
    changed = gate.verify_unchanged()
    require(not changed, 'CHANGED: inputs changed before snapshot: ' + '; '.join(changed))
    entries = []
    for rel, data in sorted(payloads.items()):
        entry = dict(path=rel, sha256=hashlib.sha256(data).hexdigest(), size_bytes=len(data), kind=kinds[rel])
        if rel.startswith('sources/'):
            entry['source_path'] = rel[len('sources/'):]
        entries.append(entry)
    index = dict(schema_version=2, deliverable_id=deliverable_id,
                 round_id=round_id, created_at=datetime.now(timezone.utc).isoformat(),
                 editorial_approval_issued=False, supplied_result_is_not_certified=True,
                 **metadata, entries=entries)
    index_data = json_bytes(index)
    index_hash = hashlib.sha256(index_data).hexdigest()

    checked_directory(gate.root, destination.parent, create=True)
    # Exclusive directory creation claims the round; no overwrite or cleanup/reuse.
    try:
        destination.mkdir(exist_ok=False)
    except FileExistsError as exc:
        raise Rejection(f'EXISTS: round already exists: {destination}') from exc

    def write_new(rel, data):
        rel = relative_path(rel, 'snapshot output')
        path = destination / rel
        checked_directory(gate.root, path.parent, create=True)
        require(not os.path.lexists(path), f'EXISTS: snapshot file already exists: {rel}')
        with path.open('xb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        require(not is_link_or_reparse(path), f'PATH: snapshot file replaced by link: {rel}')
        require(hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(data).digest(),
                f'HASH: snapshot write verification failed: {rel}')

    try:
        for rel, data in sorted(payloads.items()):
            write_new(rel, data)
        changed = gate.verify_unchanged()
        require(not changed, 'CHANGED: inputs changed during snapshot: ' + '; '.join(changed))
        # The hash sidecar is the last file: its absence marks an incomplete snapshot.
        write_new('index.json', index_data)
        write_new('index.sha256', (index_hash + '\n').encode('ascii'))
    except (OSError, Rejection) as exc:
        raise Rejection(f'INCOMPLETE: snapshot retained at {destination}; use a new round ID: {exc}') from exc
    return dict(archived=True, deliverable_id=deliverable_id, round_id=round_id,
                snapshot_path=str(destination), index_sha256=index_hash, files_archived=len(entries),
                editorial_approval_issued=False)


def archive_rejected(gate, deliverable_id, round_id, result_path, extras):
    """Preserve statements as statements and observations as observations; never approve.

    Legacy v1 inputs are historical bytes here, not migrated acceptance evidence.
    A parseable, unambiguous deliverables registry and original RETURN result are
    necessary to identify the requested round. Missing/unsafe subordinate inputs
    are recorded without fabrication and without following an unsafe path.
    """
    require(result_path is not None, 'PRESERVE: --result is required with --preserve-rejected')
    payloads, kinds, observations = {}, {}, []

    def observe(original, kind, declared=None, claim='enumerated source'):
        row = dict(source_path=original, claim_source=claim, declared_sha256=declared,
                   observed_sha256=None, copied_path=None, availability='UNAVAILABLE', diagnostics=[])
        observations.append(row)
        try:
            rel = relative_path(original, 'preserved source')
            path = gate.resolve(rel)
            require(not path.is_relative_to(gate.root / '08_ARHIVA'), 'PATH: archive ingestion forbidden')
        except (Rejection, OSError, ValueError) as exc:
            message = str(exc)
            code = 'UNSAFE_PATH' if message.startswith('PATH:') else 'MISSING_OR_UNREADABLE'
            row['diagnostics'].append(dict(code=code, detail=message))
            return None
        try:
            data = gate.read(rel)
        except (Rejection, OSError) as exc:
            require(not str(exc).startswith('CHANGED:'), str(exc))
            row['diagnostics'].append(dict(code='UNREADABLE', detail=str(exc)))
            return None
        target = 'sources/' + rel
        payloads[target] = data
        kinds.setdefault(target, kind)
        digest = hashlib.sha256(data).hexdigest()
        row.update(observed_sha256=digest, copied_path=target, availability='COPIED')
        if declared is not None:
            try:
                expected = hash_string(declared, claim)
                if digest != expected:
                    row['diagnostics'].append(dict(code='HASH_MISMATCH', detail='declared != observed'))
            except Rejection as exc:
                row['diagnostics'].append(dict(code='HASH_INVALID', detail=str(exc)))
        return data

    raw_result = observe(result_path, 'original_rejection_result')
    require(raw_result is not None, 'PRESERVE: original result must be readable inside ROOT')
    try:
        supplied = parse_json(raw_result)
    except (ValueError, UnicodeError) as exc:
        raise Rejection(f'PRESERVE: original result is not valid JSON: {exc}') from exc
    require(isinstance(supplied, dict) and supplied.get('deliverable_id') == deliverable_id
            and supplied.get('passed') is False and isinstance(supplied.get('errors'), list)
            and bool(supplied['errors']) and all(isinstance(e, str) and e.strip() for e in supplied['errors']),
            'PRESERVE: matching original passed=false result with nonempty errors required')
    if 'schema_version' in supplied:
        integer(supplied['schema_version'], 1, 2, 'historical result schema_version')
    payloads['result.json'], kinds['result.json'] = raw_result, 'original_rejection_result'
    for rel in ('00_CONDUCERE/policy.json', '06_REGISTRU/agents.json'):
        observe(rel, 'registry_or_policy')
    raw_registry = observe('06_REGISTRU/deliverables.json', 'declared_registry')
    require(raw_registry is not None, 'PRESERVE: declared registry is required')
    registry = parse_json(raw_registry)
    require(isinstance(registry, dict), 'PRESERVE: registry must be an object')
    items = {}
    for item in array(registry.get('deliverables'), 'historical deliverables', 1):
        require(isinstance(item, dict), 'PRESERVE: deliverable must be an object')
        key = nonempty(item.get('id'), 'historical deliverable id')
        require(key not in items, f'PRESERVE: ambiguous duplicate deliverable {key}')
        items[key] = item
    require(deliverable_id in items, f'PRESERVE: unknown deliverable {deliverable_id}')

    def note(code, source, detail):
        observations.append(dict(source_path=source, claim_source='structure', declared_sha256=None,
                                 observed_sha256=None, copied_path=None, availability='NOT_APPLICABLE',
                                 diagnostics=[dict(code=code, detail=detail)]))

    def entries(values, kind, claim):
        if not isinstance(values, list):
            note('SCHEMA_INVALID', claim, 'expected list; declaration preserved verbatim')
            return
        for entry in values:
            if not isinstance(entry, dict):
                note('SCHEMA_INVALID', claim, 'expected file reference; declaration preserved')
                continue
            if 'sha256' not in entry or entry['sha256'] is None:
                note('HASH_INVALID', claim, 'missing declared digest')
            observe(entry.get('path'), kind, entry.get('sha256'), claim)

    def proof(values, claim):
        if not isinstance(values, list):
            note('SCHEMA_INVALID', claim, 'evidence is not a list')
            return
        for value in values:
            if isinstance(value, dict):
                entries([value], 'evidence_source', claim)
            elif isinstance(value, str):
                # Historical v1 references are copied but explicitly not hash-bound.
                path = value.partition('#')[0]
                path = re.sub(r':L[1-9][0-9]*(?:-L?[1-9][0-9]*)?$', '', path)
                note('UNPINNED_EVIDENCE', path, 'legacy string reference has no reviewed digest')
                observe(path, 'legacy_evidence_source', claim=claim)
            else:
                note('SCHEMA_INVALID', claim, 'invalid evidence reference')

    seen_contracts = set()

    def contract(ref, claim):
        if not isinstance(ref, dict):
            note('CONTRACT_ABSENT_OR_LEGACY', claim, 'no v2 contract reference')
            return
        if 'sha256' not in ref or ref['sha256'] is None:
            note('HASH_INVALID', claim, 'missing contract digest; declaration retained')
        data = observe(ref.get('path'), 'declared_contract', ref.get('sha256'), claim)
        if data is None or not isinstance(ref.get('path'), str) or ref['path'] in seen_contracts:
            return
        seen_contracts.add(ref['path'])
        try:
            doc = parse_json(data)
            require(isinstance(doc, dict), 'contract must be object')
            entries(doc.get('files', []), 'declared_artifact', ref['path'])
            entries(doc.get('evidence_files', []), 'evidence_source', ref['path'])
            if isinstance(doc.get('policy'), dict):
                entries([doc['policy']], 'declared_policy', ref['path'])
            for dependency in array(doc.get('dependencies', []), 'contract dependencies'):
                require(isinstance(dependency, dict), 'invalid contract dependency')
                contract(dependency.get('contract'), ref['path'])
        except (Rejection, ValueError, UnicodeError) as exc:
            note('SCHEMA_INVALID', ref['path'], str(exc))

    def report(path, meta=False):
        data = observe(path, 'meta_audit_report' if meta else 'audit_report')
        if data is None:
            return
        try:
            doc = parse_json(data)
            require(isinstance(doc, dict), 'report must be object')
            entries(doc.get('audit_files' if meta else 'files', []), 'report_claimed_file', str(path))
            entries(doc.get('supplemental_evidence_files', []), 'supplemental_evidence_source', str(path))
            if 'contract' in doc:
                contract(doc['contract'], str(path))
            for row in array(doc.get('checks' if meta else 'criteria', []), 'report checks/criteria'):
                require(isinstance(row, dict), 'invalid report check/criterion')
                proof(row.get('evidence', []), str(path))
        except (Rejection, ValueError, UnicodeError) as exc:
            note('SCHEMA_INVALID', path, str(exc))

    visited, dependency_ids = set(), []

    def collect(identifier):
        if identifier in visited:
            return
        visited.add(identifier)
        if identifier not in items:
            note('MISSING_DEPENDENCY', identifier, 'not in declared registry')
            return
        item = items[identifier]
        target = 'manifest.json' if identifier == deliverable_id else (
            'dependency_manifests/' + hashlib.sha256(identifier.encode('utf-8')).hexdigest() + '.json')
        payloads[target], kinds[target] = json_bytes(item), 'declared_manifest'
        entries(item.get('files'), 'artifact', identifier)
        entries(item.get('evidence_files', []), 'evidence_source', identifier)
        contract(item.get('contract'), identifier)
        for path in array(item.get('audits', []), 'historical audits'):
            report(path)
        if 'meta_audit' in item:
            report(item['meta_audit'], meta=True)
        for child in array(item.get('dependencies', []), 'historical dependencies'):
            if not isinstance(child, str):
                note('SCHEMA_INVALID', identifier, 'invalid dependency ID')
                continue
            if child not in visited:
                dependency_ids.append(child)
            collect(child)

    collect(deliverable_id)
    seen_extras = set()
    for original in extras:
        require(isinstance(original, str) and original not in seen_extras, 'DUPLICATE: --extra')
        seen_extras.add(original)
        observe(original, 'extra', claim='--extra')
    incomplete = any(row['availability'] == 'UNAVAILABLE' for row in observations)
    traversal_complete = not any(any(d['code'] in ('SCHEMA_INVALID', 'MISSING_DEPENDENCY')
                                     for d in row['diagnostics']) for row in observations)
    return write_snapshot(gate, deliverable_id, round_id, payloads, kinds,
                          archive_kind='rejected_evidence_snapshot', source_consistency='NOT_CERTIFIED',
                          supplied_result_verdict='RETURN', result_provided=True,
                          observed_availability='PARTIAL' if incomplete else 'AVAILABLE',
                          declaration_traversal_complete=traversal_complete,
                          dependencies=dependency_ids, observations=observations)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--deliverable', required=True)
    parser.add_argument('--round', required=True, dest='round_id')
    parser.add_argument('--result', help='ROOT-relative path to an existing gatekeeper JSON result')
    parser.add_argument('--extra', action='append', default=[], metavar='RELPATH',
                        help='Additional ROOT-relative file to preserve; repeat as needed')
    parser.add_argument('--preserve-rejected', action='store_true',
                        help='Preserve original RETURN and observed bytes despite declared hash errors')
    args = parser.parse_args(argv)
    try:
        result = archive(args.root, args.deliverable, args.round_id, args.result, args.extra,
                         args.preserve_rejected)
    except (Rejection, OSError, ValueError, RuntimeError) as exc:
        print(json.dumps(dict(archived=False, deliverable_id=args.deliverable,
                              round_id=args.round_id, errors=[str(exc)]), ensure_ascii=True))
        return 2
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
