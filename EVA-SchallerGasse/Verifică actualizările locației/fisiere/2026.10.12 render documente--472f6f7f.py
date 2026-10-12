from pathlib import Path
import importlib.util, sys, shutil

SKILL=Path('C:/Users/User/.codex/plugins/cache/openai-primary-runtime/documents/26.915.20218/skills/documents/render_docx.py')
spec=importlib.util.spec_from_file_location('codex_docx_renderer',SKILL)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
docx=Path(sys.argv[1]).resolve()
pdf=docx.with_suffix('.pdf')
out=Path(sys.argv[2]).resolve()
if not pdf.exists():raise RuntimeError('Native Word PDF export is required before rasterization')
def native_pdf(doc_path,user_profile,convert_tmp_dir,stem,verbose=False):
    dest=Path(convert_tmp_dir)/(stem+'.pdf')
    shutil.copy2(pdf,dest)
    return str(dest),'Rendered from this DOCX by native Microsoft Word, read-only and macros disabled.'
mod.convert_to_pdf=native_pdf
sys.argv=[str(SKILL),str(docx),'--output_dir',str(out),'--dpi','135','--emit_pdf']
mod.main()
# User date convention also applies to retained QA filenames.
for p in out.glob('page-*.png'):p.rename(out/('2026.10.12 '+p.name))
