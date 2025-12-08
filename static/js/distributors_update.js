const API_BASE = "https://billingsystem-production.up.railway.app"; const token = localStorage.getItem("token");
function goMenu(){ window.location.href = "/menu"; }

async function loadDists(){
  const res = await fetch(`${API_BASE}/distributors/`, { headers:{ Authorization:`Bearer ${token}` }});
  const list = await res.json();
  const t = document.getElementById('distBody'); t.innerHTML='';
  list.forEach(d=>{
    t.insertAdjacentHTML('beforeend', `<tr>
      <td>${d.id}</td><td><input data-id="${d.id}" class="name" value="${d.name}"/></td>
      <td><input data-id="${d.id}" class="city" value="${d.city||''}"/></td>
      <td><input data-id="${d.id}" class="state" value="${d.state||''}"/></td>
      <td><button onclick="updateDist(${d.id})">Save</button><button onclick="deleteDist(${d.id})">Delete</button></td>
    </tr>`);
  });
}

document.getElementById('addDist').onclick = async ()=>{
  const payload = { name: document.getElementById('d_name').value, city: document.getElementById('d_city').value, state: document.getElementById('d_state').value };
  const res = await fetch(`${API_BASE}/distributors/add`, { method:'POST', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload) });
  if(!res.ok){ alert('Add failed'); return; }
  await loadDists();
};

async function updateDist(id){
  const payload = { name: document.querySelector(`.name[data-id="${id}"]`).value, city: document.querySelector(`.city[data-id="${id}"]`).value, state: document.querySelector(`.state[data-id="${id}"]`).value };
  const res = await fetch(`${API_BASE}/update/${id}`, { method:'PUT', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload) });
  // Note: your distributor update route is /update/<int:dist_id> so the correct endpoint is /distributors/update/<id>
  const res2 = await fetch(`${API_BASE}/distributors/update/${id}`, { method:'PUT', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload) });
  if(!res2.ok){ alert('Update failed'); }
  await loadDists();
}

async function deleteDist(id){
  if(!confirm('Delete distributor?')) return;
  const res = await fetch(`${API_BASE}/distributors/delete/${id}`, { method:'DELETE', headers:{ Authorization:`Bearer ${token}` }});
  if(!res.ok){ alert('Delete failed'); }
  await loadDists();
}

window.onload = loadDists;
