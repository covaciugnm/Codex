from pathlib import Path
p=Path(__file__).parent/'a12_r5_make_matches.py';s=p.read_text(encoding='utf8').replace("rs2=roots2.get('runs')or roots2.get('results')or [];","rs2=(roots2.get('runs')or roots2.get('results')or [])+(rd(pc/'JVM/Calibrare_JVM_R5_3.json').get('results')or []);").replace("x.get('run_rc',x.get('run')),'JVM_calibrated_root'","x.get('rc',x.get('run_rc',x.get('run'))),'JVM_calibrated_root'");p.write_text(s,encoding='utf8')

