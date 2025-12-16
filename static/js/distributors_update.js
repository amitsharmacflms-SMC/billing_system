const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){
  window.location.href = "/menu";
}

// ---------------- LOAD SUPPLIERS DROPDOWN ----------------
async function loadSuppliersDropdown(){
  const res = await fetch(`${API_BASE}/suppliers/`, {
    headers:{ Authorization:`Bearer ${token}` }
  });
  const list = await res.json();
  const ddl = document.getElementById("d_supplier_id");

  ddl.innerHTML = `<option value="">-- Select Supplier --</option>`;
  list.forEach(s=>{
    ddl.insertAdjacentHTML(
      "beforeend",
      `<option value="${s.id}">${s.name}</option>`
    );
  });
}

// ---------------- LOAD DISTRIBUTORS ----------------
async function loadDists(){
  const res = await fetch(`${API_BASE}/distributors/`, {
    headers:{ Authorization:`Bearer ${token}` }
  });
  const list = await res.json();
  const t = document.getElementById("distBody");
  t.innerHTML = "";

  list.forEach(d=>{
    t.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${d.id}</td>
        <td><input class="name" data-id="${d.id}" value="${d.name||''}"></td>
        <td><input class="city" data-id="${d.id}" value="${d.city||''}"></td>
        <td><input class="state" data-id="${d.id}" value="${d.state||''}"></td>
        <td><input class="gstin" data-id="${d.id}" value="${d.gstin||''}"></td>
        <td>
          <button onclick="updateDist(${d.id})">Save</button>
          <button onclick="deleteDist(${d.id})">Delete</button>
        </td>
      </tr>
    `);
  });
}

// ---------------- ADD DISTRIBUTOR ----------------
document.getElementById("addDist").onclick = async ()=>{
  const payload = {
    unique_key: d_unique_key.value,
    name: d_name.value,
    contact_person: d_contact_person.value,
    phone: d_phone.value,
    email: d_email.value,
    address: d_address.value,
    city: d_city.value,
    state: d_state.value,
    pincode: d_pincode.value,
    gstin: d_gstin.value,
    supplier_id: d_supplier_id.value || null
  };

  const res = await fetch(`${API_BASE}/distributors/add`, {
    method:"POST",
    headers:{ "Content-Type":"application/json", Authorization:`Bearer ${token}` },
    body:JSON.stringify(payload)
  });

  if(!res.ok){
    alert("Add failed");
    return;
  }
  loadDists();
};

// ---------------- UPDATE ----------------
async function updateDist(id){
  const payload = {
    name: document.querySelector(`.name[data-id="${id}"]`).value,
    city: document.querySelector(`.city[data-id="${id}"]`).value,
    state: document.querySelector(`.state[data-id="${id}"]`).value,
    gstin: document.querySelector(`.gstin[data-id="${id}"]`).value
  };

  await fetch(`${API_BASE}/distributors/update/${id}`, {
    method:"PUT",
    headers:{ "Content-Type":"application/json", Authorization:`Bearer ${token}` },
    body:JSON.stringify(payload)
  });

  loadDists();
}

// ---------------- DELETE ----------------
async function deleteDist(id){
  if(!confirm("Delete distributor?")) return;

  const res = await fetch(`${API_BASE}/distributors/delete/${id}`, {
    method:"DELETE",
    headers:{ Authorization:`Bearer ${token}` }
  });

  if(!res.ok){
    const err = await res.json();
    alert(err.error || "Delete failed");
    return;
  }
  loadDists();
}

window.onload = () => {
  loadSuppliersDropdown();
  loadDists();
};
