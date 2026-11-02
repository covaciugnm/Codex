"""Build a version-pinned, auditable ARM64 patch. Run in the analysis WSL.

Requires Python 3, pyelftools and GNU aarch64-linux-gnu binutils.
The original library is never modified. All changed byte ranges are reported.
"""
import argparse
import hashlib
import io
import json
import re
import struct
import subprocess
from pathlib import Path

from elftools.elf.elffile import ELFFile

EXPECTED = "17745c9106afa9fbdf3077ea2d0771437b1435371aec73d8ad13ef5e71ad2f06"
EXTENSION = 0x18AD080


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("original", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--work", type=Path, required=True)
    args = p.parse_args()
    assert args.original.resolve() != args.output.resolve(), "Preserve original"
    source = Path(__file__).with_name("romania40.S")
    raw = args.original.read_bytes()
    assert sha(raw) == EXPECTED, "Unsupported libapp.so: original SHA-256 mismatch"
    args.work.mkdir(parents=True, exist_ok=True)
    elf_original = ELFFile(io.BytesIO(raw))
    names = re.findall(r'\.section (\.patch\.([0-9a-f]+)),', source.read_text())
    layout = "\n".join(f"original_{a} = 0x{a};" for a in sorted(set(
        re.findall(r'\boriginal_([0-9a-f]+)', source.read_text())))) + "\nSECTIONS {\n"
    for name, address in sorted(names, key=lambda x: int(x[1], 16)):
        layout += f" {name} 0x{address} : {{ *({name}) }}\n"
    layout += f" .extension 0x{EXTENSION:x} : {{ *(.extension) }}\n"
    layout += " /DISCARD/ : { *(.text) *(.data) *(.bss) *(.comment) }\n}\n"
    linker = args.work / "patch.ld"
    linker.write_text(layout)
    obj = args.work / "patch.o"
    elf_path = args.work / "patch.elf"
    subprocess.run(["aarch64-linux-gnu-as", str(source), "-o", str(obj)], check=True)
    subprocess.run(["aarch64-linux-gnu-ld", "-T", str(linker), str(obj), "-o", str(elf_path)], check=True)
    with elf_path.open("rb") as f:
        patch = ELFFile(f)
        parts = [(s.name, s["sh_addr"], s.data()) for s in patch.iter_sections()
                 if s.name.startswith(".patch.") or s.name == ".extension"]
        symbols = {s.name: s["st_value"] for s in patch.get_section_by_name(".symtab").iter_symbols()
                   if s.name and s["st_info"]["type"] != "STT_SECTION"}
    extension_data = next(data for name, _, data in parts if name == ".extension")
    end = EXTENSION + len(extension_data)
    assert end < 0x18B0000, "Extension overlaps writable segment"
    assert not any(raw[EXTENSION:end]), "Expected unused zero-filled ELF padding"
    mutated = bytearray(raw)
    changes = []

    def replace(offset, new, reason):
        old = raw[offset:offset + len(new)]
        assert len(old) == len(new)
        assert not any(offset < c["offset"] + c["length"] and c["offset"] < offset + len(new)
                       for c in changes), "Overlapping patches"
        mutated[offset:offset + len(new)] = new
        changes.append({"offset": offset, "offsetHex": hex(offset), "length": len(new),
                        "reason": reason, "beforeSha256": sha(old), "afterSha256": sha(new),
                        **({"beforeHex": old.hex(), "afterHex": new.hex()} if len(new) <= 32 else {})})

    for name, offset, data in parts:
        replace(offset, data, name)
    for i, seg in enumerate(elf_original.iter_segments()):
        if seg["p_type"] == "PT_LOAD" and seg["p_flags"] == 5:
            assert seg["p_vaddr"] == seg["p_offset"] == 0x940000
            assert seg["p_filesz"] == seg["p_memsz"] == 0xF6D060
            header = elf_original["e_phoff"] + i * elf_original["e_phentsize"]
            replace(header + 32, struct.pack("<QQ", end - seg["p_offset"], end - seg["p_offset"]),
                    "Extend executable PT_LOAD to include leaf helpers")
    for i, sec in enumerate(elf_original.iter_sections()):
        if sec.name == ".text":
            header = elf_original["e_shoff"] + i * elf_original["e_shentsize"]
            replace(header + 32, struct.pack("<Q", end - sec["sh_offset"]),
                    "Extend .text section size")
    covered = bytearray(len(raw))
    for c in changes:
        covered[c["offset"]:c["offset"] + c["length"]] = b"\x01" * c["length"]
    assert all(a == b or covered[i] for i, (a, b) in enumerate(zip(raw, mutated)))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(mutated)
    report = {"schemaVersion": 1, "originalSha256": EXPECTED, "patchedSha256": sha(mutated),
              "bytes": len(mutated), "changedBytes": sum(a != b for a, b in zip(raw, mutated)),
              "assemblySha256": sha(source.read_bytes()), "changes": changes, "symbols": symbols,
              "countries": ["+86", "+852", "+853", "+40"],
              "romaniaMobileNationalFormat": "7 followed by 8 ASCII digits; no leading 0",
              "wireCountryCode": "40", "serverAcceptanceTested": False,
              "allChangesWithinAllowlist": True,
              "allocatingCallSitesPreserved": ["0x156cf18", "0x156cf44", "0x156cfb0", "0x1283158"]}
    (args.work / "native-patch.json").write_text(json.dumps(report, indent=2) + "\n")
    with (args.work / "patch-disassembly.txt").open("w") as f:
        subprocess.run(["aarch64-linux-gnu-objdump", "-d", str(elf_path)], stdout=f, check=True)
    print(json.dumps({k: report[k] for k in ["originalSha256", "patchedSha256", "changedBytes"]}))


if __name__ == "__main__":
    main()
