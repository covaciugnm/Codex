"""Execute the actual patched ARM64 instructions in Unicorn, without networking."""
import argparse
import json
import struct
from pathlib import Path

from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm64_const import *

H = 0x200000000
STACK = 0x300000000
POOL = H + 0x80000
THREAD = H + 0xF0000
NULL = H + 0x101
STOP = 0x1900000


def fixture(binary):
    u = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
    u.mem_map(0, 0x2000000)
    u.mem_write(0, binary)
    u.mem_map(H, 0x100000)
    u.mem_map(STACK, 0x10000)
    u.reg_write(UC_ARM64_REG_X15, STACK + 0x8000)
    u.reg_write(UC_ARM64_REG_X29, STACK + 0x80D0)
    u.reg_write(UC_ARM64_REG_X22, NULL)
    u.reg_write(UC_ARM64_REG_X26, THREAD)
    u.reg_write(UC_ARM64_REG_X27, POOL)
    u.reg_write(UC_ARM64_REG_X28, H >> 32)
    u.reg_write(UC_ARM64_REG_X30, STOP)
    u.mem_write(THREAD + 0x60, struct.pack("<QQ", H + 0x60000, H + 0x70000))
    return u


def put_string(u, address, value):
    data = value.encode("ascii")
    u.mem_write(address - 1, struct.pack("<QII", 0x5E25C, len(data) * 2, 0) + data + b"\0" * 16)
    return address


def ptr(u, address, value, size=4):
    u.mem_write(address, value.to_bytes(8, "little")[:size])


def read_ptr(u, address):
    return H + int.from_bytes(u.mem_read(address, 4), "little")


def read_string(u, address):
    size = int.from_bytes(u.mem_read(address + 7, 4), "little") >> 1
    return bytes(u.mem_read(address + 15, size)).decode("ascii")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("library", type=Path)
    p.add_argument("report", type=Path)
    a = p.parse_args()
    b = a.library.read_bytes()
    metadata = json.loads((a.report.parent / "native-patch.json").read_text())
    sy = metadata["symbols"]
    cases = []
    for phone, expected in [("712345678", True), ("700000000", True), ("799999999", True),
                            ("0712345678", False), ("40712345678", False), ("612345678", False),
                            ("71234567", False), ("7123456789", False), ("71234a678", False),
                            ("71234 678", False), ("", False)]:
        u = fixture(b)
        u.reg_write(UC_ARM64_REG_X1, put_string(u, H + 0x1001, phone))
        u.reg_write(UC_ARM64_REG_X2, put_string(u, H + 0x1101, "+40"))
        u.emu_start(0xFA92D0, STOP, count=500)
        assert u.reg_read(UC_ARM64_REG_PC) == STOP
        actual = u.reg_read(UC_ARM64_REG_X0) == NULL + 0x20
        assert actual == expected, (phone, actual)
        cases.append({"case": "Romanian format: " + (phone or "empty"), "passed": True})
    for prefix in ["+86", "+852", "+853"]:
        u = fixture(b)
        u.reg_write(UC_ARM64_REG_X2, put_string(u, H + 0x1101, prefix))
        u.emu_start(0xFA92D0, 0xFA92D4, count=100)
        assert u.reg_read(UC_ARM64_REG_PC) == 0xFA92D4
        assert u.reg_read(UC_ARM64_REG_X15) == STACK + 0x8000 - 16
        cases.append({"case": "Original validator retained: " + prefix, "passed": True})
    for prefix in ["+40", "+86", "+852", "+853", "+401"]:
        u = fixture(b)
        u.reg_write(UC_ARM64_REG_X2, put_string(u, H + 0x1101, prefix))
        u.emu_start(sy["country_length"], STOP if prefix == "+40" else 0x179F91C, count=100)
        if prefix == "+40":
            assert u.reg_read(UC_ARM64_REG_X0) == 18
        else:
            assert u.reg_read(UC_ARM64_REG_PC) == 0x179F91C
        cases.append({"case": "Length dispatch: " + prefix, "passed": True})
    for helper, value, slot, end in [("init_prefix", "+40", 0x27, 0x156CF4C),
                                     ("init_label", "Romania", 0x2B, 0x156CFB8)]:
        u = fixture(b)
        string, array, empty = H + 0x1001, H + 0x2001, H + 0x3001
        put_string(u, string, " " * len(value))
        ptr(u, array - 1, 0x5A31C, 8)
        ptr(u, STACK + 0x80D0 - 16, array, 8)
        ptr(u, THREAD + 0xA0, empty, 8)
        u.reg_write(UC_ARM64_REG_X0, string)
        u.emu_start(sy[helper], end, count=100)
        assert read_string(u, string) == value
        assert read_ptr(u, array + slot) == string
        assert u.reg_read(UC_ARM64_REG_X3) == empty
        cases.append({"case": "Initialize " + value + " and preserve Intl arguments", "passed": True})

    # Execute the real dropdown patch and real Dart AllocateArray fast path.
    # Mock only unrelated framework methods; examine their actual ABI arguments.
    u = fixture(b)
    outer, state, mapping, backing = [H + n for n in (0x1001, 0x2001, 0x3001, 0x4001)]
    closure, mapped, result = [H + n for n in (0x8001, 0x9001, 0xA001)]
    strings = []
    for i, prefix in enumerate(["+86", "+852", "+853", "+40"]):
        strings.append(put_string(u, H + 0x5001 + i * 0x100, prefix))
    ptr(u, STACK + 0x80D0 - 8, outer, 8)
    ptr(u, outer + 0xF, state)
    ptr(u, state + 0x17, mapping)
    ptr(u, mapping + 0xF, backing)
    ptr(u, backing + 0x27, strings[3])
    for offset, value in [(0x3BA10, strings[0]), (0x3BA20, strings[1]),
                          (0x507C0, strings[2]), (0x5C8, H + 0xB001), (0x5DDC8, H + 0xC001)]:
        ptr(u, POOL + offset, value, 8)
    ptr(u, mapped + 7, H + 0xB001)
    u.reg_write(UC_ARM64_REG_X0, closure)
    seen = []

    def hook(uc, address, size, _):
        if address == 0x9EEA60:
            assert uc.reg_read(UC_ARM64_REG_X1) == 20
            assert uc.reg_read(UC_ARM64_REG_X30) == 0x128315C
            uc.reg_write(UC_ARM64_REG_D0, int.from_bytes(struct.pack("<d", 17.25), "little"))
            uc.reg_write(UC_ARM64_REG_PC, uc.reg_read(UC_ARM64_REG_X30))
            seen.append("original screen scaling")
        elif address == 0x18A3084:
            assert uc.reg_read(UC_ARM64_REG_X30) == 0x128315C
            assert int.from_bytes(uc.mem_read(STACK + 0x80D0 - 0x20, 8), "little") == closure
            seen.append("allocation at existing GC call site with rooted closure")
        elif address == 0xDCB314:
            sp = uc.reg_read(UC_ARM64_REG_X15)
            assert int.from_bytes(uc.mem_read(sp, 8), "little") == closure
            arr = int.from_bytes(uc.mem_read(sp + 8, 8), "little")
            assert int.from_bytes(uc.mem_read(arr + 0xB, 4), "little") == 8
            values = [read_string(uc, read_ptr(uc, arr + 0xF + i * 4)) for i in range(4)]
            assert values == ["+86", "+852", "+853", "+40"], values
            uc.reg_write(UC_ARM64_REG_X0, mapped)
            uc.reg_write(UC_ARM64_REG_PC, uc.reg_read(UC_ARM64_REG_X30))
            seen.append("four distinct countries passed to original widget mapping")
        elif address == 0x956C78:
            assert uc.reg_read(UC_ARM64_REG_X2) == mapped
            uc.reg_write(UC_ARM64_REG_X0, result)
            uc.reg_write(UC_ARM64_REG_PC, uc.reg_read(UC_ARM64_REG_X30))
    u.hook_add(UC_HOOK_CODE, hook)
    u.emu_start(0x1283120, 0x1283164, count=1000)
    assert u.reg_read(UC_ARM64_REG_PC) == 0x1283164
    assert struct.unpack("<d", u.mem_read(STACK + 0x80D0 - 0xA8, 8))[0] == -17.25
    assert int.from_bytes(u.mem_read(STACK + 0x80D0 - 0x20, 8), "little") == result
    assert len(seen) == 3
    cases.append({"case": "Complete dropdown path and original scale preserved", "passed": True, "checks": seen})
    result = {"schemaVersion": 1, "engine": "Unicorn ARM64", "networkRequests": 0,
              "patchedSha256": metadata["patchedSha256"], "passed": len(cases), "failed": 0,
              "cases": cases, "limits": ["GC slow paths and Flutter rendering require device tests.",
                                           "No server request or account login is simulated as successful."]}
    a.report.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"passed": len(cases), "failed": 0}))


if __name__ == "__main__":
    main()
