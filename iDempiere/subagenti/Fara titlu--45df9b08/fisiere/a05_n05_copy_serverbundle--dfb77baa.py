from pathlib import Path
s=Path('D:/CodexWork/a05_n05_copy_uibundle.py').read_text().replace('org.adempiere.ui.zk_13.0.0.202603090043','org.adempiere.server_13.0.0.202603090043').replace('Native_UI_bundle_readonly','Native_Server_bundle_readonly').replace('UI not started','server not started')
s=s[:s.index('\neva=')]+'\nprint({"entries":len(rows),"bytes":target.stat().st_size,"runtime_started":False})\n'
exec(compile(s,'copy_server_readonly','exec'))
