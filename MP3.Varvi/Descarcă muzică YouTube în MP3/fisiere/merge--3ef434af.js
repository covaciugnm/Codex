(() => {
  const el = id => document.getElementById(id);
  const extensions = /\.(mp4|mkv|mov|avi|webm|m4v|mpeg|mpg|ts)$/i;
  let clips = [], working = false;
  function render() {
    el('merge-list').replaceChildren();
    clips.forEach((clip, index) => {
      const row = document.createElement('tr');
      const name = document.createElement('td');
      name.textContent = `${index + 1}. ${clip.file.webkitRelativePath || clip.file.name}`;
      name.style.overflowWrap = 'anywhere';
      const actions = document.createElement('td');
      for (const [text, label, action, disabled] of [
        ['↑', 'Mută mai sus', () => { [clips[index - 1], clips[index]] = [clips[index], clips[index - 1]]; render(); }, index === 0],
        ['↓', 'Mută mai jos', () => { [clips[index + 1], clips[index]] = [clips[index], clips[index + 1]]; render(); }, index === clips.length - 1],
        ['Elimină', 'Elimină videoclipul', async () => {
          try { await release(clip); clips.splice(index, 1); render(); } catch (e) { el('merge-error').textContent = e.message; }
        }, false]
      ]) {
        const button = document.createElement('button'); button.type = 'button'; button.textContent = text;
        button.title = label; button.setAttribute('aria-label', label + ': ' + clip.file.name);
        button.style.cssText = 'margin:4px;padding:7px 10px'; button.disabled = working || disabled;
        button.onclick = action; actions.append(button);
      }
      row.append(name, actions); el('merge-list').append(row);
    });
    el('merge-count').textContent = `${clips.length} videoclipuri · ordinea din listă este ordinea din filmul final`;
    el('merge-start').disabled = working || clips.length < 2;
    for (const id of ['merge-one','merge-many','merge-folder','merge-clear','merge-name']) el(id).disabled = working;
  }
  async function json(response) {
    const data = await response.json(); if (!response.ok) throw Error(data.error || 'Cererea a eșuat.'); return data;
  }
  async function release(clip) {
    if (clip.id) await json(await fetch(`/api/merge/uploads/${clip.id}/remove`, {method:'POST', headers:{'X-MP3-App':'local'}}));
  }
  function add(input, folder) {
    let files = Array.from(input.files);
    if (folder) files.sort((a,b) => (a.webkitRelativePath || a.name).localeCompare(b.webkitRelativePath || b.name, 'ro', {numeric:true}));
    let skipped = 0;
    for (const file of files) {
      if (!extensions.test(file.name) || !file.size || file.size > 4 * 1024**3 || clips.length >= 100) { skipped++; continue; }
      const key = `${file.webkitRelativePath || file.name}|${file.size}|${file.lastModified}`;
      if (clips.some(c => c.key === key)) { skipped++; continue; }
      clips.push({file, key, id:null});
    }
    el('merge-error').textContent = skipped ? `${skipped} fișiere omise: duplicate, format neacceptat, goale sau limite depășite (100 videoclipuri, 4 GB/fișier).` : '';
    input.value = ''; render();
  }
  for (const id of ['merge-one','merge-many','merge-folder']) el(id).addEventListener('change', () => add(el(id), id==='merge-folder'));
  el('merge-clear').onclick = async () => {
    try { for (const clip of clips) await release(clip); clips=[]; render(); }
    catch (e) { el('merge-error').textContent=e.message; }
  };
  function upload(clip, index) {
    return new Promise((resolve, reject) => {
      const xhr = new XMLHttpRequest(), form = new FormData(); form.append('file',clip.file);
      xhr.open('POST','/api/merge/uploads'); xhr.setRequestHeader('X-MP3-App','local');
      xhr.upload.onprogress = event => {
        const percent = event.lengthComputable ? Math.round(event.loaded/event.total*100) : 0;
        el('merge-message').textContent = `Copiez local videoclipul ${index+1}/${clips.length}: ${clip.file.name} (${percent}%)`;
        el('merge-progress').value = percent;
      };
      xhr.onerror = () => reject(Error('Conexiune întreruptă la încărcare.'));
      xhr.onload = () => { try { const data=JSON.parse(xhr.responseText); if(xhr.status>=400)throw Error(data.error); clip.id=data.id;resolve(); } catch(e){reject(e);} };
      xhr.send(form);
    });
  }
  async function poll(id) {
    try {
      const response = await fetch('/api/merge/jobs/'+id);
      if (response.status===404) { localStorage.removeItem('merge-job'); throw Error('Serverul a fost repornit. Adaugă videoclipurile din nou.'); }
      const data = await json(response);
      el('merge-message').textContent=data.message; el('merge-progress').value=data.percent;
      if (['done','failed'].includes(data.status)) {
        localStorage.removeItem('merge-job'); working=false;
        if(data.status==='done') {
          clips.forEach(c=>c.id=null);
          const link=el('merge-result'); link.href='/files/'+data.file.split(/[\\/]/).map(encodeURIComponent).join('/');
          link.textContent='Descarcă videoclipul unit · MP4';link.hidden=false;
        } else el('merge-error').textContent=data.message;
        render(); return;
      }
      setTimeout(()=>poll(id),1200);
    } catch(e) {
      el('merge-error').textContent=e.message;
      if(localStorage.getItem('merge-job'))setTimeout(()=>poll(id),4000);
      else {working=false;render();}
    }
  }
  el('merge-start').onclick=async()=>{
    working=true;render();el('merge-error').textContent='';el('merge-result').hidden=true;el('merge-status').hidden=false;
    try {
      for(let i=0;i<clips.length;i++)if(!clips[i].id)await upload(clips[i],i);
      const data=await json(await fetch('/api/merge/jobs',{method:'POST',headers:{'Content-Type':'application/json','X-MP3-App':'local'},body:JSON.stringify({ids:clips.map(c=>c.id),name:el('merge-name').value})}));
      localStorage.setItem('merge-job',data.id);poll(data.id);
    }catch(e){el('merge-error').textContent=e.message;working=false;render();}
  };
  render();
  const previous=localStorage.getItem('merge-job');
  if(previous){working=true;render();el('merge-status').hidden=false;poll(previous);}
})();
