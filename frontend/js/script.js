const queryEl = document.getElementById('query');
const resultEl = document.getElementById('result');
const askBtn = document.getElementById('ask');
const clearBtn = document.getElementById('clear');
const historyEl = document.getElementById('history');
const conditionEl = document.getElementById('condition');
const summaryEl = document.getElementById('summary');
const disclaimerEl = document.getElementById('disclaimer');
const symptomsEl = document.getElementById('symptoms');
const precautionsEl = document.getElementById('precautions');
const whenEl = document.getElementById('when_to_seek_care');
const sourcesEl = document.getElementById('sources');
const followupsEl = document.getElementById('followups');
const placeholderEl = document.getElementById('placeholder');

const historyCardEl = document.getElementById('history-card');
const clearHistoryBtn = document.getElementById('clear-history');
const viewRedflagsBtn = document.getElementById('view-redflags-btn');

const confidenceBadgeEl = document.getElementById('confidence-badge');
const toggleSymptomsBtn = document.getElementById('toggle-symptoms');
const togglePrecautionsBtn = document.getElementById('toggle-precautions');
const safetyTriggerEl = document.getElementById('safety-trigger');
const safetyModalOverlayEl = document.getElementById('safety-modal');
const safetyModalCloseBtn = document.getElementById('safety-modal-close');
const safetyModalDisclaimerEl = document.getElementById('safety-modal-disclaimer');
const safetyModalRedflagsEl = document.getElementById('safety-modal-redflags');

let history = JSON.parse(localStorage.getItem('sha_history') || '[]');
renderHistory();

function showHistoryPanel(show){
  if(historyCardEl) historyCardEl.style.display = show ? 'block' : 'none';
  if(resultEl) resultEl.style.display = show ? 'none' : 'block';
}

// Default view: show result panel, keep history hidden until user clicks History.
showHistoryPanel(false);

const SYMPTOMS_LIMIT = 10;
const PRECAUTIONS_LIMIT = 10;

let symptomsExpanded = false;
let precautionsExpanded = false;
let lastSymptoms = [];
let lastPrecautions = [];
let lastWhenToSeekCare = [];
let lastDisclaimer = '';

const DEFAULT_DISCLAIMER = "I am not a medical professional. This tool provides general information only; seek a qualified provider for personal medical advice.";

function renderChips(listEl, items, expanded, limit){
  if(!listEl) return;
  listEl.innerHTML = '';
  const shown = expanded ? (items || []) : (items || []).slice(0, limit);
  (shown || []).forEach(t=>{ const li = document.createElement('li'); li.textContent = t; listEl.appendChild(li); });
}

function setSafetyModalOpen(open){
  if(!safetyModalOverlayEl) return;
  safetyModalOverlayEl.classList.toggle('open', !!open);
  safetyModalOverlayEl.setAttribute('aria-hidden', String(!open));
}

function fillSafetyModal(){
  if(!safetyModalDisclaimerEl || !safetyModalRedflagsEl) return;
  safetyModalDisclaimerEl.textContent = lastDisclaimer || (disclaimerEl && disclaimerEl.textContent) || DEFAULT_DISCLAIMER;
  const items = (lastWhenToSeekCare || []).filter(Boolean);
  safetyModalRedflagsEl.innerHTML = '';
  const shown = items.length ? items : ["If symptoms are severe, worsening, or you are worried, seek medical care."];
  shown.forEach(s=>{
    const li = document.createElement('li');
    li.textContent = s;
    safetyModalRedflagsEl.appendChild(li);
  });
}

function openSafetyModal(){
  fillSafetyModal();
  setSafetyModalOpen(true);
}

function closeSafetyModal(){
  setSafetyModalOpen(false);
}

function updateToggleButtons(){
  if(toggleSymptomsBtn){
    const tooMany = (lastSymptoms || []).length > SYMPTOMS_LIMIT;
    toggleSymptomsBtn.style.display = tooMany ? 'inline-flex' : 'none';
    toggleSymptomsBtn.textContent = symptomsExpanded ? 'Show less' : 'Show more';
  }
  if(togglePrecautionsBtn){
    const tooMany = (lastPrecautions || []).length > PRECAUTIONS_LIMIT;
    togglePrecautionsBtn.style.display = tooMany ? 'inline-flex' : 'none';
    togglePrecautionsBtn.textContent = precautionsExpanded ? 'Show less' : 'Show more';
  }
}

function setLoading(loading){
  askBtn.disabled = loading;
  clearBtn.disabled = loading;
  askBtn.textContent = loading ? 'Thinking…' : 'Ask';
}

function renderResult(content){
  // If string, show simple preformatted; if object, render structured view
  if(typeof content === 'string'){
    const structured = resultEl.querySelector('#result-structured');
    if(structured) structured.style.display = 'none';
    if(placeholderEl) placeholderEl.style.display = 'none';

    // Don't wipe the whole DOM subtree. Clearing `resultEl.innerHTML`
    // removes `#result-structured` and list elements, so later renders
    // can't update symptoms/precautions.
    const oldPre = resultEl.querySelector('#result-text');
    if(oldPre) oldPre.remove();

    const pre = document.createElement('pre');
    pre.id = 'result-text';
    pre.textContent = content;
    resultEl.appendChild(pre);
    return;
  }
  // object: populate structured elements
  const oldPre = resultEl.querySelector('#result-text');
  if(oldPre) oldPre.remove();

  if(placeholderEl) placeholderEl.style.display = 'none';
  const structured = resultEl.querySelector('#result-structured');
  if(structured) structured.style.display = 'block';

  // reset expansion state for a new answer
  symptomsExpanded = false;
  precautionsExpanded = false;
  lastSymptoms = content.symptoms || [];
  lastPrecautions = content.precautions || [];
  lastWhenToSeekCare = content.when_to_seek_care || [];
  lastDisclaimer = content.disclaimer || lastDisclaimer || DEFAULT_DISCLAIMER;

  // disclaimer
  if(disclaimerEl) disclaimerEl.textContent = content.disclaimer || '';
  if(conditionEl) conditionEl.textContent = content.condition || '';
  if(summaryEl) summaryEl.textContent = content.summary || '';

  if(confidenceBadgeEl){
    const conf = (content.confidence || '').toString();
    confidenceBadgeEl.textContent = conf ? `Confidence: ${conf}` : '';
    confidenceBadgeEl.style.display = conf ? 'inline-flex' : 'none';
  }
  // lists
  renderChips(symptomsEl, lastSymptoms, symptomsExpanded, SYMPTOMS_LIMIT);
  renderChips(precautionsEl, lastPrecautions, precautionsExpanded, PRECAUTIONS_LIMIT);
  updateToggleButtons();

  if(whenEl){
    whenEl.innerHTML='';
    (content.when_to_seek_care || []).forEach(s=>{ const li=document.createElement('li'); li.textContent=s; whenEl.appendChild(li); });
  }
  if(sourcesEl){
    sourcesEl.innerHTML='';
    (content.sources || []).forEach(src=>{ const li=document.createElement('li'); if(typeof src === 'string'){ li.textContent = src; } else { const a = document.createElement('a'); a.href = src.url || '#'; a.target='_blank'; a.rel='noopener'; a.textContent = src.title || src.url || src; li.appendChild(a); } sourcesEl.appendChild(li); });
  }
  // followups
  if(followupsEl){
    followupsEl.innerHTML='';
    (content.follow_up_questions || []).forEach(q=>{ const btn = document.createElement('button'); btn.className='btn-ghost'; btn.style.padding='6px 10px'; btn.textContent=q; btn.addEventListener('click', ()=>{ queryEl.value = q; ask(); }); followupsEl.appendChild(btn); });
  }

  // keep modal content in sync with the latest answer
  fillSafetyModal();
}

function addToHistory(q, summary){
  const item = {q, summary, t: Date.now()};
  history.unshift(item);
  if(history.length>10) history.pop();
  localStorage.setItem('sha_history', JSON.stringify(history));
  renderHistory();
}

function renderHistory(){
  historyEl.innerHTML = '';
  if(history.length===0){
    historyEl.innerHTML = '<li style="color:var(--muted)">No history yet</li>';
    return;
  }
  history.forEach(h => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${escapeHtml(h.q)}</strong><small>${new Date(h.t).toLocaleString()}</small>`;
    li.addEventListener('click', ()=>{
      showHistoryPanel(false);
      queryEl.value = h.q;
      ask();
    });
    historyEl.appendChild(li);
  });
}

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"})[c]);
}

async function ask(){
  const q = queryEl.value.trim();
  if(!q){
    renderResult('Please enter a question or describe symptoms.');
    return;
  }
  setLoading(true);
  renderResult('Thinking…');
  try{
    const r = await fetch('/ask',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({query:q})
    });
    const data = await r.json();
    setLoading(false);
    if(!r.ok){
      // show refusal using structured view when possible
      renderResult({disclaimer:data.disclaimer||'Request was refused. ', summary:data.reason||JSON.stringify(data), symptoms:[], precautions:['See a healthcare provider if needed'], when_to_seek_care:[], sources:[]});
      return;
    }
    // If response looks like structured schema, render structured; otherwise attempt to pretty-print
    if(data.condition || data.summary || data.symptoms){
      renderResult(data);
      addToHistory(q, (data.summary || '').slice(0,200));
    } else {
      const text = data.answer || data.message || JSON.stringify(data, null, 2);
      renderResult(text);
      addToHistory(q, (typeof text==='string' ? text.slice(0,200) : 'result'));
    }
  }catch(e){
    setLoading(false);
    renderResult('Error: '+e.message+'. Please check your connection and try again.');
  }
}

clearBtn.addEventListener('click', ()=>{ queryEl.value=''; queryEl.focus(); });
askBtn.addEventListener('click', ask);

if(clearHistoryBtn){
  clearHistoryBtn.addEventListener('click', ()=>{
    const ok = confirm('Delete all history?');
    if(!ok) return;
    history = [];
    localStorage.setItem('sha_history', JSON.stringify([]));
    renderHistory();
    showHistoryPanel(false);
    queryEl.focus();
  });
}

if(toggleSymptomsBtn){
  toggleSymptomsBtn.addEventListener('click', ()=>{
    symptomsExpanded = !symptomsExpanded;
    renderChips(symptomsEl, lastSymptoms, symptomsExpanded, SYMPTOMS_LIMIT);
    updateToggleButtons();
  });
}

if(togglePrecautionsBtn){
  togglePrecautionsBtn.addEventListener('click', ()=>{
    precautionsExpanded = !precautionsExpanded;
    renderChips(precautionsEl, lastPrecautions, precautionsExpanded, PRECAUTIONS_LIMIT);
    updateToggleButtons();
  });
}

if(safetyTriggerEl){
  const openHandler = ()=>openSafetyModal();
  safetyTriggerEl.addEventListener('click', openHandler);
  safetyTriggerEl.addEventListener('keydown', (e)=>{ if(e.key === 'Enter' || e.key === ' '){ e.preventDefault(); openHandler(); } });
}
if(safetyModalCloseBtn){
  safetyModalCloseBtn.addEventListener('click', closeSafetyModal);
}
if(safetyModalOverlayEl){
  safetyModalOverlayEl.addEventListener('click', (e)=>{ if(e.target === safetyModalOverlayEl) closeSafetyModal(); });
}
window.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closeSafetyModal(); });

if(viewRedflagsBtn){
  viewRedflagsBtn.addEventListener('click', openSafetyModal);
}

// allow Ctrl+Enter to send
queryEl.addEventListener('keydown', (e)=>{ if(e.key==='Enter' && (e.ctrlKey||e.metaKey)){ ask(); } });

// Navigation: make sidebar links functional (Ask / History / Awareness)
document.querySelectorAll('.nav a').forEach(a=>{
  a.addEventListener('click', (ev)=>{
    document.querySelectorAll('.nav a').forEach(x=>x.classList.remove('active'));
    a.classList.add('active');
    const txt = a.textContent.trim().toLowerCase();
    if(txt==='history'){
      showHistoryPanel(true);
      if(history.length===0 && historyEl){
        historyEl.scrollTop = 0;
      }
    } else if(txt==='awareness'){
      showHistoryPanel(false);
      // fetch FAQ from backend and populate the FAQ card
      fetch('/faq').then(r=>r.json()).then(list=>{
        const faqList = document.querySelector('.faq-list');
        faqList.innerHTML='';
        (list||[]).forEach(it=>{ const li = document.createElement('li'); const ael = document.createElement('a'); ael.href = it.url || '#'; ael.target='_blank'; ael.rel='noopener'; ael.textContent = it.title || it; li.appendChild(ael); faqList.appendChild(li); });
      }).catch(()=>{});
    } else {
      showHistoryPanel(false);
      // Ask selected: focus input
      queryEl.focus();
    }
  });
});
