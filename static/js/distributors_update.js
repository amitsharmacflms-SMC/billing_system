const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){
  window.location.href = "/menu";
}

function popup(msg){
  alert(msg);
}

/* ---------------- LOAD SUPPLIERS ---------------- */
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

/* ---------------- LOAD DISTRIBUTORS LIST ---------------- */
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
        <td>${d.city || ""}</td>
        <td>${d.state || ""}</td>
        <td>${d.gstin}</td>
        <td>
          <button onclick="editDist(${d.id})">Edit</button>
          <button onclick="deleteDist(${d.id})">Delete</button>
        </td>
      </tr>
    `;
  });
}

/* ---------------- ADD / UPDATE ---------------- */
document.getElementById("addDist").onclick = async ()=>{
  const editId = addDist.dataset.editId;

  const payload = {
    unique_key: d_unique_key.value.trim(),
    name: d_name.value.trim(),
    gstin: d_gstin.value.trim(),
    contact_person: d_contact_person.value,
    phone: d_phone.value,
    email: d_email.value,
    address: d_address.value,
    city: d_city.value,
    state: d_state.value,
    pincode: d_pincode.value,
    supplier_id: d_supplier_id.value || null
  };

  if(!payload.unique_key || !payload.name || !payload.gstin){
    popup("Distributor Code, Name and GSTIN are mandatory");
    return;
  }

  let url = `${API_BASE}/distributors/add`;
  let method = "POST";

  if(editId){
    url = `${API_BASE}/distributors/update/${editId}`;
    method = "PUT";
  }

  const res = await fetch(url, {
    method,
    headers:{
      "Content-Type":"application/json",
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  popup(data.message || data.error);

  if(res.ok){
    clearForm();
    loadDists();
  }
};

/* ---------------- EDIT ---------------- */
async function editDist(id){
  const res = await fetch(`${API_BASE}/distributors/${id}`, {
    headers:{ Authorization:`Bearer ${token}` }
  });
  const d = await res.json();

  d_unique_key.value = d.unique_key || "";
  d_name.value = d.name || "";
  d_gstin.value = d.gstin || "";
  d_contact_person.value = d.contact_person || "";
  d_phone.value = d.phone || "";
  d_email.value = d.email || "";
  d_address.value = d.address || "";
  d_city.value = d.city || "";
  d_state.value = d.state || "";
  d_pincode.value = d.pincode || "";
  d_supplier_id.value = d.supplier_id || "";

  addDist.innerText = "Save Changes";
  addDist.dataset.editId = id;
}

/* ---------------- DELETE ---------------- */
async function deleteDist(id){
  if(!confirm("Delete distributor?")) return;

  const res = await fetch(`${API_BASE}/distributors/delete/${id}`, {
    method:"DELETE",
    headers:{ Authorization:`Bearer ${token}` }
  });

  const data = await res.json();
  popup(data.message || data.error);

  if(res.ok){
    loadDists();
  }
}

/* ---------------- HELPERS ---------------- */
function clearForm(){
  document.querySelectorAll(".form-row input").forEach(i => i.value = "");
  d_supplier_id.value = "";
  addDist.innerText = "Add Distributor";
  delete addDist.dataset.editId;
}

window.onload = ()=>{
  loadSuppliersDropdown();
  loadDists();
};
