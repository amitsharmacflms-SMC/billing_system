const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){ window.location.href = "/menu"; }

async function loadSuppliers(){
  const res = await fetch(`${API_BASE}/suppliers/`, { headers:{ Authorization:`Bearer ${token}` }});
  const list = await res.json();
  const sel = document.getElementById('supplierSelect');
  sel.innerHTML = '<option value="">Select Supplier</option>';
  list.forEach(s => sel.insertAdjacentHTML('beforeend', `<option value="${s.id}">${s.name}</option>`));
}

async function loadDistributors(){
  const res = await fetch(`${API_BASE}/distributors/`, { headers:{ Authorization:`Bearer ${token}` }});
  const list = await res.json();
  const mult = document.getElementById('distributorsSelect');
  mult.innerHTML = '';
  list.forEach(d => mult.insertAdjacentHTML('beforeend', `<option value="${d.id}">${d.name} (${d.city||''})</option>`));
}

async function assign(){
  const supplier_id = document.getElementById('supplierSelect').value;
  if(!supplier_id){ alert('Choose supplier'); return; }
  const selected = Array.from(document.getElementById('distributorsSelect').selectedOptions).map(o=>parseInt(o.value));
  if(selected.length===0){ alert('Select distributors'); return; }
  const res = await fetch(`${API_BASE}/mapping/assign`, {
    method:'POST', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`},
    body: JSON.stringify({ supplier_id: supplier_id, distributor_ids: selected })
  });
  if(res.ok){ alert('Assigned'); loadDistributors(); }
  else { alert('Failed'); }
}

async function unassign(){
  // unassign selected distributors -> set supplier_id = null
  const selected = Array.from(document.getElementById('distributorsSelect').selectedOptions).map(o=>parseInt(o.value));
  if(selected.length===0){ alert('Select distributors'); return; }
  for(const did of selected){
    await fetch(`${API_BASE}/distributors/update/${did}`, {
      method:'PUT', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`},
      body: JSON.stringify({ supplier_id: null })
    });
  }
  alert('Unassigned');
  loadDistributors();
}

window.onload = async ()=>{
  await loadSuppliers();
  await loadDistributors();
};
