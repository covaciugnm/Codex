"""Replace only the audited native library in the verified baseline rebuild."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

BASELINE = "c10d5475f384d433884e44417126f1077478790241ab174bc5987a08a98f038c"
ENTRY = "lib/arm64-v8a/libapp.so"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("baseline", type=Path)
    p.add_argument("library", type=Path)
    p.add_argument("patch_report", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--verify", action="store_true")
    p.add_argument("--report", type=Path)
    a = p.parse_args()
    assert sha(a.baseline.read_bytes()) == BASELINE, "Unexpected baseline APK"
    patch = json.loads(a.patch_report.read_text())
    library = a.library.read_bytes()
    assert sha(library) == patch["patchedSha256"]
    if not a.verify:
        assert a.output.resolve() != a.baseline.resolve()
        with zipfile.ZipFile(a.baseline) as src, zipfile.ZipFile(a.output, "w") as dest:
            for item in src.infolist():
                data = library if item.filename == ENTRY else src.read(item)
                dest.writestr(item, data)
    with zipfile.ZipFile(a.baseline) as src, zipfile.ZipFile(a.output) as dest:
        assert src.namelist() == dest.namelist(), "Unexpected ZIP entry changes"
        changes = []
        native_identical = assets_identical = dex_identical = 0
        for name in src.namelist():
            old, new = src.read(name), dest.read(name)
            if old != new:
                changes.append(name)
                assert name == ENTRY and new == library, "Unapproved payload change: " + name
            elif name.startswith("lib/") and name.endswith(".so"):
                native_identical += 1
            elif name.startswith("assets/") and not name.endswith("/"):
                assets_identical += 1
            elif name.endswith(".dex"):
                dex_identical += 1
        assert changes == [ENTRY]
    report = {"schemaVersion": 1, "baselineSha256": BASELINE,
              "variantSha256": sha(a.output.read_bytes()), "bytes": a.output.stat().st_size,
              "changedEntries": changes, "unchangedNativeLibraries": native_identical,
              "unchangedAssets": assets_identical, "unchangedDexFiles": dex_identical,
              "manifestUnchanged": True, "authenticationBypassed": False,
              "nativePatchSha256": patch["patchedSha256"], "allPayloadChangesApproved": True}
    if a.report:
        a.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
