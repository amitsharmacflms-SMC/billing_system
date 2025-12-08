const API_BASE = "https://billingsystem-production.up.railway.app"; const token = localStorage.getItem("token");
function goMenu(){ window.location.href = "/menu"; }

async function loadSuppliers(){
  const res = await fetch(`${API_BASE}/suppliers/`, { headers:{ Authorization:`Bearer ${token}` }});
  const list = await res.json();
  const t = document.getElementById('supBody'); t.innerHTML='';
  list.forEach(s=>{
    t.insertAdjacentHTML('beforeend', `<tr>
      <td>${s.id}</td><td><input data-id="${s.id}" class="name" value="${s.name}"/></td>
      <td><input data-id="${s.id}" class="city" value="${s.city||''}"/></td>
      <td><input data-id="${s.id}" class="state" value="${s.state||''}"/></td>
      <td><input data-id="${s.id}" class="gstin" value="${s.gstin||''}"/></td>
      <td><button onclick="updateSupplier(${s.id})">Save</button>
          <button onclick="deleteSupplier(${s.id})">Delete</button></td>
    </tr>`);
  });
}

document.getElementById('addSupplier').onclick = async ()=>{
  const payload = { name: document.getElementById('s_name').value, city: document.getElementById('s_city').value, state: document.getElementById('s_state').value, gstin: document.getElementById('s_gstin').value };
  const res = await fetch(`${API_BASE}/suppliers/add`, { method:'POST', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload) });
  if(!res.ok){ alert('Add failed'); return; }
  await loadSuppliers();
};

async function updateSupplier(id){
  const payload = {
    name: document.querySelector(`.name[data-id="${id}"]`).value,
    city: document.querySelector(`.city[data-id="${id}"]`).value,
    state: document.querySelector(`.state[data-id="${id}"]`).value,
    gstin: document.querySelector(`.gstin[data-id="${id}"]`).value
  };
  const res = await fetch(`${API_BASE}/suppliers/update/${id}`, { method:'PUT', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload) });
  if(!res.ok){ alert('Update failed'); }
  await loadSuppliers();
}

async function deleteSupplier(id){
  if(!confirm('Delete supplier?')) return;
  const res = await fetch(`${API_BASE}/suppliers/delete/${id}`, { method:'DELETE', headers:{ Authorization:`Bearer ${token}` }});
  if(!res.ok){ alert('Delete failed'); }
  await loadSuppliers();
}

window.onload = loadSuppliers;
