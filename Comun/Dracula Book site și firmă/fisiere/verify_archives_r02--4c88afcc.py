"""Verify real archive copies and recover into an isolated temporary directory."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--round",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--expect-pass",action="store_true")
    args=parser.parse_args()
    if "/" in args.round or "\\" in args.round or args.round in {".",".."}:raise SystemExit("unsafe round")
    result_path=(ROOT/args.output).resolve()
    if not result_path.is_relative_to(ROOT) or result_path.exists():raise SystemExit("unsafe/existing output")
    results=[]
    for identifier in ["SYS-001","SEL-001","RES-001"]:
        snapshot=(ROOT/"08_ARHIVA"/identifier/args.round).resolve(strict=True)
        if not snapshot.is_relative_to((ROOT/"08_ARHIVA").resolve()):raise SystemExit("unsafe snapshot")
        index_data=(snapshot/"index.json").read_bytes()
        index_hash=sha(index_data)
        if index_hash!=(snapshot/"index.sha256").read_text(encoding="ascii").strip():raise SystemExit("index mismatch")
        index=json.loads(index_data);count=0
        for entry in index["entries"]:
            source=(snapshot/entry["path"]).resolve(strict=True)
            if not source.is_relative_to(snapshot):raise SystemExit("unsafe indexed path")
            raw=source.read_bytes()
            if sha(raw)!=entry["sha256"] or len(raw)!=entry["size_bytes"]:raise SystemExit("entry mismatch")
            count+=1
        with tempfile.TemporaryDirectory(prefix="DraculaAudit-") as temporary:
            temp_path=Path(temporary).resolve()
            if not temp_path.is_relative_to(Path(tempfile.gettempdir()).resolve()) or not temp_path.name.startswith("DraculaAudit-"):raise SystemExit("unsafe temporary target")
            restored=temp_path/"restored"
            shutil.copytree(snapshot/"sources",restored)
            process=subprocess.run([sys.executable,"-B",str(restored/"04_INSTRUMENTE/gatekeeper.py"),"--root",str(restored),"--deliverable",identifier,"--json"],capture_output=True,text=True,encoding="utf-8")
            gate=json.loads(process.stdout)
            if gate["passed"]!=args.expect_pass:raise SystemExit("unexpected restored gate verdict")
            if not args.expect_pass:
                def collect(g):return g["errors"]+[e for d in g["dependencies"] for e in collect(d)]
                errors=collect(gate)
                if any(("HASH" in e or "CONTRACT" in e or "PATH" in e or "FILE:" in e) for e in errors):raise SystemExit("restored inputs missing or changed")
            results.append({"deliverable":identifier,"round":args.round,"index_sha256":index_hash,"verified_entries":count,"restored_gate_passed":gate["passed"],"restored_exit_code":process.returncode,"errors":gate["errors"],"expected_pass":args.expect_pass})
    output={"type":"REAL_SNAPSHOT_RECOVERY_CHECK","results":results,"limits":"Checks indexed bytes and the executable gate, not literary quality or external timestamp. Temporary copies removed only inside validated isolated temporary directories."}
    result_path.parent.mkdir(parents=True,exist_ok=True)
    with result_path.open("x",encoding="utf-8") as f:json.dump(output,f,ensure_ascii=False,indent=2)
    print(json.dumps(output,ensure_ascii=False))
if __name__=="__main__":main()

