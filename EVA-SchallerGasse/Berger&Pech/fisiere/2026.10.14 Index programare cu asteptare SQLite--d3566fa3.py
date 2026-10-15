import sqlite3,runpy
from pathlib import Path
original_connect=sqlite3.connect
def connect_with_wait(*args,**kwargs):
    kwargs.setdefault('timeout',60)
    return original_connect(*args,**kwargs)
sqlite3.connect=connect_with_wait
runpy.run_path(str(Path.cwd()/'folder map/actualizeaza_index.py'),run_name='__main__')
