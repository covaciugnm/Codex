const $ = id => document.getElementById(id);
let timer, importId = null, importCount = 0, busy = false;
const fileUrl = name => '/files/' + name.split(/[\\/]/).map(encodeURIComponent).join('/');
function setBusy(value) {
  busy = value;
  $('start').disabled = value;
  $('excel-start').disabled = value || !importId || !importCount;
}
async function responseJSON(response) {
  const data = await response.json();
  if (!response.ok) throw Error(data.error || 'Cererea a eșuat.');
  return data;
}
function beginJob(id) {
  clearTimeout(timer);
  localStorage.setItem('mp3-job', id);
  $('job').hidden = false;
  $('error').textContent = '';
  setBusy(true);
  poll(id);
}
async function poll(id) {
  try {
    const response = await fetch('/api/jobs/' + id);
    if (response.status === 404) {
      localStorage.removeItem('mp3-job');
      setBusy(false);
      $('message').textContent = 'Sesiunea anterioară s-a încheiat. Poți începe o descărcare nouă.';
      return;
    }
    const job = await responseJSON(response);
    $('message').textContent = job.message;
    const batch = job.batch_total ? `LINK ${job.batch_current} / ${job.batch_total} · ${job.source_label} · ` : '';
    $('count').textContent = `${batch}PIESA ${job.current} / ${job.total} · ${job.files.length} SALVATE`;
    $('progress').value = job.percent;
    $('folder').textContent = job.folder || '';
    $('results').replaceChildren();
    for (const file of job.files) {
      const row = document.createElement('tr');
      for (const value of [file.artist + ' — ' + file.title, file.album || '—']) {
        const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
      }
      const cell = document.createElement('td'), link = document.createElement('a');
      link.href = fileUrl(file.file); link.textContent = 'MP3 ↓'; cell.append(link); row.append(cell);
      $('results').append(row);
    }
    const logs = [...job.errors.map(e => `${e.source || ''} Piesa ${e.index}: ${e.title}\n${e.error}`), ...job.warnings];
    $('details').hidden = !logs.length; $('logs').textContent = logs.join('\n\n');
    if (['done', 'partial', 'failed'].includes(job.status)) {
      localStorage.removeItem('mp3-job'); setBusy(false);
      if (job.status === 'failed') $('error').textContent = job.message;
      return;
    }
    timer = setTimeout(() => poll(id), 1200);
  } catch (error) {
    $('error').textContent = 'Conexiune întreruptă; reîncerc automat. ' + error.message;
    timer = setTimeout(() => poll(id), 5000);
  }
}
$('form').addEventListener('submit', async event => {
  event.preventDefault(); $('error').textContent = ''; setBusy(true);
  try {
    const data = await responseJSON(await fetch('/api/jobs', {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-MP3-App': 'local'},
      body: JSON.stringify({url: $('url').value, quality: $('quality').value})
    }));
    beginJob(data.id);
  } catch (error) { $('error').textContent = error.message; setBusy(false); }
});
function resetImport() {
  importId = null; importCount = 0; $('excel-summary').hidden = true;
  $('excel-error').textContent = ''; setBusy(busy);
}
$('excel-file').addEventListener('change', resetImport);
$('excel-form').addEventListener('submit', async event => {
  event.preventDefault(); resetImport();
  const file = $('excel-file').files[0];
  if (!file) return;
  if (file.size > 10 * 1024 * 1024) { $('excel-error').textContent = 'Maximum 10 MB.'; return; }
  $('excel-preview').disabled = true; $('excel-file').disabled = true;
  try {
    const form = new FormData(); form.append('file', file);
    const data = await responseJSON(await fetch('/api/imports', {method: 'POST', headers: {'X-MP3-App': 'local'}, body: form}));
    importId = data.id; importCount = data.entries.length;
    $('excel-summary').hidden = false;
    $('excel-count').textContent = `${data.filename}: ${importCount} linkuri valide, ${data.issues.length} rânduri omise cu probleme sau duplicate.` +
      (!importCount ? ' Completează coloana Link YouTube din Excel, salvează și importă din nou.' : ' Verifică lista, apoi pornește descărcarea.');
    $('excel-sheets').textContent = data.sheets.map(s => `${s.name}: ${s.skipped ? 'fără coloană de linkuri' : s.count + ' linkuri'}`).join(' · ');
    $('excel-links').replaceChildren();
    for (const entry of data.entries) {
      const row = document.createElement('tr'), location = document.createElement('td'), cell = document.createElement('td');
      location.textContent = `${entry.sheet} / ${entry.row}`;
      location.title = data.folders[entry.sheet] || '';
      const link = document.createElement('a'); link.href = entry.url; link.textContent = entry.url;
      link.target = '_blank'; link.rel = 'noopener noreferrer'; cell.append(link); row.append(location, cell); $('excel-links').append(row);
    }
    $('excel-issues').hidden = !data.issues.length;
    $('excel-issue-list').textContent = data.issues.map(i => `${i.sheet}, rând ${i.row}: ${i.reason}`).join('\n');
  } catch (error) { $('excel-error').textContent = error.message; }
  finally { $('excel-preview').disabled = false; $('excel-file').disabled = false; setBusy(busy); }
});
$('excel-start').addEventListener('click', async () => {
  if (!importId || busy) return;
  setBusy(true); $('excel-error').textContent = '';
  try {
    const data = await responseJSON(await fetch(`/api/imports/${importId}/start`, {
      method: 'POST', headers: {'Content-Type': 'application/json', 'X-MP3-App': 'local'},
      body: JSON.stringify({quality: $('quality').value})
    }));
    importId = null; beginJob(data.id);
    $('job').scrollIntoView({behavior: 'smooth'});
  } catch (error) { $('excel-error').textContent = error.message; setBusy(false); }
});
fetch('/api/status').then(responseJSON).then(s => { $('destination').textContent = s.output; })
  .catch(() => { $('destination').textContent = 'Server indisponibil'; });
const previous = localStorage.getItem('mp3-job');
if (previous) beginJob(previous);
