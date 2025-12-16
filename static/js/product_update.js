const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){
  window.location.href = "/menu";
}

// -----------------------------
// LOAD PRODUCTS
// -----------------------------
async function loadProducts(){
  const res = await fetch(`${API_BASE}/products/`, {
    headers:{ Authorization:`Bearer ${token}` }
  });

  const list = await res.json();
  const t = document.getElementById('prodBody');
  t.innerHTML = '';

  list.forEach(p=>{
    t.insertAdjacentHTML('beforeend', `
      <tr>
        <td>${p.id}</td>
        <td><input class="edit_name" data-id="${p.id}" value="${p.name || ''}"></td>
        <td><input class="edit_hsn" data-id="${p.id}" value="${p.hsn || ''}"></td>
        <td><input class="edit_rate" data-id="${p.id}" value="${p.rate || 0}"></td>
        <td><input class="edit_pack" data-id="${p.id}" value="${p.pack || ''}"></td>
        <td>
          <button onclick="updateProduct(${p.id})">Save</button>
          <button onclick="deleteProduct(${p.id})">Delete</button>
        </td>
      </tr>
    `);
  });
}

// -----------------------------
// ADD PRODUCT
// -----------------------------
document.getElementById('addProd').onclick = async ()=>{
  const payload = {
    sku: document.getElementById('p_sku').value.trim(),
    name: document.getElementById('p_name').value.trim(),
    hsn: document.getElementById('p_hsn').value.trim(),
    mrp: parseFloat(document.getElementById('p_mrp').value || 0),
    rate: parseFloat(document.getElementById('p_rate').value || 0),
    pack: document.getElementById('p_pack').value.trim()
  };

  const res = await fetch(`${API_BASE}/products/add`, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(!res.ok){
    alert(await res.text());
    return;
  }

  loadProducts();
};

// -----------------------------
// UPDATE PRODUCT
// -----------------------------
async function updateProduct(id){
  const payload = {
    name: document.querySelector(`.edit_name[data-id="${id}"]`).value,
    hsn: document.querySelector(`.edit_hsn[data-id="${id}"]`).value,
    rate: parseFloat(document.querySelector(`.edit_rate[data-id="${id}"]`).value || 0),
    pack: document.querySelector(`.edit_pack[data-id="${id}"]`).value
  };

  const res = await fetch(`${API_BASE}/products/update/${id}`, {
    method:'PUT',
    headers:{
      'Content-Type':'application/json',
      Authorization:`Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });

  if(!res.ok){
    alert("Update failed");
    return;
  }

  loadProducts();
}

// -----------------------------
// DELETE PRODUCT
// -----------------------------
async function deleteProduct(id){
  if(!confirm("Delete product?")) return;

  const res = await fetch(`${API_BASE}/products/delete/${id}`, {
    method:'DELETE',
    headers:{ Authorization:`Bearer ${token}` }
  });

  if(!res.ok){
    alert("Delete failed");
    return;
  }

  loadProducts();
}

window.onload = loadProducts;
