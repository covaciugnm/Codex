from pathlib import Path
import json
B=Path(__file__).parent
R=B/'CRM_iDempiere_EVA_2026-10-08'
pages=[]
def page(title,paragraphs,headers=None,rows=None):
    pages.append(dict(title=title,paragraphs=paragraphs,headers=headers,rows=rows))
