const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){
  window.location.href = "/menu";
}

function popup(msg){
  alert(msg);
}

async function loadSuppliersDropdown(){
  const res = await fetch(`${API_BASE}/suppliers/`, {
    headers:{ Authorization:`Bearer ${token}` }
  });
  const list = await res.json();
  const ddl = document.getElementById("d_supplier_id");
  ddl.innerHTML = `<option value="">-- Select Supplier --</option>`;
  list.forEach(s=>{
    ddl.innerHTML += `<option value="${s.id}">${s.name}</option>`;
  });
}

async function loadDists(){
  const res = await fetch(`${API_BASE}/distributors/`, {
    headers:{ Authorization:`Bearer ${token}` }
  });
  const list = await res.json();
  const t = document.getElementById("distBody");
  t.innerHTML = "";
  list.forEach(d=>{
    t.innerHTML += `
      <tr>
        <td>${d.id}</td>
        <td>${d.unique_key}</td>
        <td>${d.name}</td>
        <td>${d.city||''}</td>
        <td>${d.state||''}</td>
        <td>${d.gstin}</td>
        <td>
          <button onclick="deleteDist(${d.id})">Delete</button>
        </td>
      </tr>`;
  });
}

document.getElementById("addDist").onclick = async ()=>{
  const payload = {
    unique_key: d_unique_key.value,
    name: d_name.value,
    gstin: d_gstin.value,
    city: d_city.value,
    state: d_state.value,
    supplier_id: d_supplier_id.value || null
  };

  const res = await fetch(`${API_BASE}/distributors/add`, {
    method:"POST",
    headers:{ "Content-Type":"application/json", Authorization:`Bearer ${token}` },
    body:JSON.stringify(payload)
  });

  const data = await res.json();
  popup(data.message || data.error);
  loadDists();
};

async function deleteDist(id){
  if(!confirm("Delete distributor?")) return;

  const res = await fetch(`${API_BASE}/distributors/delete/${id}`, {
    method:"DELETE",
    headers:{ Authorization:`Bearer ${token}` }
  });

  const data = await res.json();
  popup(data.message || data.error);
  loadDists();
}

window.onload = ()=>{
  loadSuppliersDropdown();
  loadDists();
};
