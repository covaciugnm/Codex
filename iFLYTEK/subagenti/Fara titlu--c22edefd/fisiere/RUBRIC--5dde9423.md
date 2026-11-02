# Independent audit rubric

One point per criterion, awarded only when evidence is present. A 10/10 measures completeness and reproducibility of the static analysis activity within the inventoried inputs, not recovery of unavailable original source or absence of decompiler limitations.

1. **Complete container inventory.** Every unique APK/XAPK in the original manifest, current collection, and local task inputs is accounted for, with duplicate source paths mapped to the same SHA-256; missing/download failures are resolved or explicitly reflected in the score.
2. **Identity and splits.** Package name, versionName, versionCode, channel/variant, ABI and XAPK split inventory are obtained from actual package metadata; every split APK is accounted for.
3. **Input integrity and provenance.** SHA-256, byte sizes, source paths/URLs and Git/Release provenance are recorded and verified against the available manifests.
4. **Version isolation.** Each app/version has a separate logical directory and each distinct channel/hash variant is distinguished; no output mixing or overwrite between versions.
5. **Static extraction coverage.** APK manifests, resources/assets, DEX and native libraries are inventoried; extracted content is accessible, with every ZIP entry accounted for or an explicit error record.
6. **Decompiler outcomes.** Applicable DEX/resource decoding is attempted with pinned tool versions and per-input logs, commands, exit codes and output counts; failures and fallback output are preserved. Native Flutter AOT is identified and its limitations recorded.
7. **Comparison with existing archive.** File hashes/content inventories identify exact matches, new/changed/removed paths and existing reconstructed/decompiled material; existing artifacts are reused by reference rather than blindly duplicated.
8. **Source availability and claims.** A bounded public-source search is documented; official source, generic SDK, extracted bytecode, decompiled Java/Smali and Flutter AOT are clearly distinguished, without claims of recovering original source.
9. **Reproducibility and integrity.** Scripts and tool acquisition metadata allow rerunning the process; inventories validate output hashes/sizes and counts. No APK or collected payload is executed, and no private account/service access is required.
10. **Delivery and independent closure.** A navigable per-version index plus limitations, restore instructions where required, and final independent audit evidence are present. Auditor verifies representative outputs and complete machine-checkable invariants; all material issues are fixed or explicitly prevent 10/10.

Audits are iterative. Intermediate scores cannot be raised simply by relabelling missing work as a limitation. An unavailable original source can remain a documented finding if static extraction/decompilation was the authorized alternative and all applicable work was performed.
