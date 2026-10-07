export const meta = {
  name: 'curricule-cursuri-specializare',
  description: 'Generează programe (80/360/720h) pentru 7 cursuri de specializare IT/AI/robotică, ultra-moderne',
  phases: [
    { title: 'Draft', detail: 'programa inițială per curs (3 trasee)' },
    { title: 'Modernizare', detail: 'îmbunătățire 2025-2026 + QA ore' },
  ],
}

const COURSES = [
  {code:'251202', slug:'programator', title:'Programator',
   domain:'Dezvoltare software modernă, cloud-native și AI-assisted',
   modern:'Python, TypeScript, Rust, Go; programare orientată pe obiecte și funcțională; Git/GitHub; cloud-native, Docker, Kubernetes; CI/CD; API REST/GraphQL; baze de date SQL & NoSQL & vector DBs; testare automată; AI-assisted coding (GitHub Copilot, agentic coding); dezvoltare de aplicații cu LLM, RAG, prompt engineering; WebAssembly; securitate by design (OWASP); DevSecOps'},
  {code:'251203', slug:'inginer-sistem', title:'Inginer de sistem în informatică',
   domain:'Arhitecturi de sistem, DevOps, cloud, cybersecurity',
   modern:'arhitecturi distribuite și microservicii; Linux avansat; virtualizare & containere (Docker, Kubernetes); Infrastructure as Code (Terraform, Ansible); cloud (AWS/Azure/GCP); observability & SRE; zero-trust & cybersecurity; platform engineering; edge computing; AIOps; rețele moderne; automatizare infrastructură'},
  {code:'251401', slug:'cad', title:'Proiectare asistată de calculator (CAD)',
   domain:'CAD/CAE 3D parametric, generative design, digital twin, fabricație aditivă',
   modern:'modelare 3D parametrică (Fusion 360, SolidWorks, Onshape); generative design & topology optimization; simulare FEA/CFD; digital twin; fabricație aditivă / imprimare 3D; PLM; reverse engineering & 3D scanning; proiectare pentru robotică; VR/AR pentru design; automatizare CAD cu scripting/AI'},
  {code:'214959', slug:'robotica', title:'Robotică (Inginer specialist în robotică)',
   domain:'Roboți humanoizi și patrupezi, ROS 2, AI embodied, manipulare',
   modern:'ROS 2; simulare (Gazebo, NVIDIA Isaac Sim); cinematică & dinamică; roboți humanoizi și patrupezi (câini robot); manipulare & grasping; computer vision & percepție; SLAM & navigație; foundation models pentru roboți (Vision-Language-Action); imitation & reinforcement learning; sim-to-real; edge AI; actuatori & senzori; integrare hardware'},
  {code:'215202', slug:'automatizari', title:'Automatizări (Inginer automatist)',
   domain:'PLC/SCADA, IIoT, Industry 4.0, control avansat',
   modern:'PLC (Siemens TIA Portal, Codesys); SCADA/HMI; rețele industriale (Profinet, Modbus, OPC UA, TSN); IIoT & Industry 4.0; digital twin; edge computing; motion control & servo; siguranță funcțională (SIL); mentenanță predictivă cu AI; robotică industrială & cobots; energie & eficiență'},
  {code:'215239', slug:'cercetare-automatica', title:'Cercetare în automatică',
   domain:'Control avansat, reinforcement learning, digital twins, sisteme autonome',
   modern:'teoria sistemelor & control; control optimal, robust și predictiv (MPC); estimare de stare (Kalman/observatoare); identificarea sistemelor; reinforcement learning pentru control; digital twins; sisteme ciber-fizice & autonome; MATLAB/Simulink & Python (control, JAX); metode numerice; publicare & metodologia cercetării'},
  {code:'242401', slug:'formator', title:'Formator',
   domain:'Design instrucțional modern, învățare cu AI, microlearning',
   modern:'design instrucțional (ADDIE, SAM); teoria învățării adulților (andragogie); învățare blended & microlearning; LMS moderne; gamification; AI în educație (tutori AI, învățare adaptivă, generare de conținut); VR/AR pentru training; proiectarea evaluării; learning analytics; accesibilitate & incluziune; facilitare online'},
]

const SCHEMA = {
  type:'object', additionalProperties:false,
  properties:{
    code:{type:'string'}, title:{type:'string'},
    tagline:{type:'string', description:'un slogan scurt, modern, în română'},
    description:{type:'string', description:'2-3 fraze care descriu cursul de specializare'},
    audience:{type:'string', description:'cui i se adresează'},
    prerequisites:{type:'string', description:'condiții de acces / cunoștințe prealabile'},
    outcomes:{type:'array', items:{type:'string'}, description:'ce va putea face absolventul'},
    tracks:{type:'array', description:'exact 3 trasee: 80, 360, 720 ore', items:{
      type:'object', additionalProperties:false,
      properties:{
        hours:{type:'integer', enum:[80,360,720]},
        name:{type:'string'},
        level:{type:'string', description:'ex: Fundamente / Avansat aplicat / Specializare completă'},
        summary:{type:'string'},
        modules:{type:'array', items:{
          type:'object', additionalProperties:false,
          properties:{
            title:{type:'string'},
            hours:{type:'integer'},
            topics:{type:'array', items:{type:'string'}},
            tools:{type:'array', items:{type:'string'}}
          }, required:['title','hours','topics']
        }},
        competencies:{type:'array', items:{type:'string'}},
        project:{type:'string', description:'proiect practic final'},
        evaluation:{type:'string'}
      }, required:['hours','name','level','summary','modules','competencies','project','evaluation']
    }}
  },
  required:['code','title','tagline','description','audience','prerequisites','outcomes','tracks']
}

function draftPrompt(c){
  return `Ești expert în design curricular pentru formarea profesională a adulților în România (cursuri de specializare conform O.G. nr. 129/2000) și practician tehnic senior în domeniul respectiv.

Creează programa completă pentru CURSUL DE SPECIALIZARE „${c.title}" (cod COR ${c.code}).
Domeniu: ${c.domain}.

Cerințe:
- EXACT 3 trasee: 80 ore, 360 ore și 720 ore, cu progresie logică (80 = fundamente; 360 = intermediar–avansat aplicat; 720 = specializare completă, cu proiect amplu).
- Fiecare traseu are module cu: titlu, număr de ore, subiecte concrete (topics) și instrumente/tehnologii reale (tools).
- SUMA orelor modulelor din fiecare traseu TREBUIE să fie EXACT 80, 360, respectiv 720. Verifică aritmetica.
- Pentru fiecare traseu: competențe dobândite, un proiect practic final relevant și modalitatea de evaluare.
- Nr. module orientativ: 80h → 5–7 module; 360h → 10–14 module; 720h → 16–22 module.
- Conținut ULTRA-MODERN, la nivelul anilor 2025–2026, inspirat din cele mai bune cursuri actuale. Include obligatoriu abordări și tehnologii de vârf: ${c.modern}.
- Scrie integral în limba română. Fii concret și bogat (subiecte reale, tool-uri reale, nu generalități).

Returnează structura conform schemei impuse.`
}

function modernizePrompt(draft, c){
  return `Ești reviewer senior de curriculum tech + arhitect de învățare. Primești o programă DRAFT (JSON) pentru cursul de specializare „${c.title}" (cod COR ${c.code}).

Îmbunătățește-o la nivel de EXCELENȚĂ 2025–2026:
1. Adaugă/actualizează cele mai moderne tehnologii, framework-uri și abordări reale din domeniu: ${c.modern}. Elimină orice element învechit.
2. VERIFICĂ ȘI CORECTEAZĂ aritmetica: suma orelor modulelor = EXACT orele traseului (80 / 360 / 720). Ajustează orele modulelor dacă e nevoie, fără a strica progresia.
3. Asigură progresie clară între cele 3 trasee și module bogate, cu subiecte concrete și tool-uri reale.
4. Fiecare traseu: competențe, proiect final ambițios și evaluare clară.
5. Adaugă un tagline modern, descriere, public-țintă, condiții de acces și rezultate ale învățării (outcomes) puternice.
Păstrează limba română. Returnează JSON FINAL complet, conform schemei.

DRAFT:
${JSON.stringify(draft)}`
}

const results = await pipeline(
  COURSES,
  (c) => agent(draftPrompt(c), {schema:SCHEMA, phase:'Draft', label:`draft:${c.slug}`, effort:'high'}),
  (draft, c) => agent(modernizePrompt(draft, c), {schema:SCHEMA, phase:'Modernizare', label:`mod:${c.slug}`, effort:'high'})
)

const out = results.map((r,i)=> r ? ({slug:COURSES[i].slug, icon:'', ...r}) : null).filter(Boolean)
log(`Gata: ${out.length}/7 cursuri cu programe complete`)
return out
