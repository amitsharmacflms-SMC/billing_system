const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){
  window.location.href = "/menu";
}

// ----------------------------------
// LOAD PRODUCTS
// ----------------------------------
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
        <td><input data-id="${p.id}" class="edit_name" value="${p.name || ''}"/></td>
        <td><input data-id="${p.id}" class="edit_hsn" value="${p.hsn || ''}"/></td>
        <td><input data-id="${p.id}" class="edit_rate" value="${p.rate || 0}"/></td>
        <td><input data-id="${p.id}" class="edit_pack" value="${p.pack || ''}"/></td>
        <td>
          <button onclick="updateProduct(${p.id})">Save</button>
          <button onclick="deleteProduct(${p.id})">Delete</button>
        </td>
      </tr>
    `);
  });
}

// ----------------------------------
// ADD PRODUCT  ✅ FIXED
// ----------------------------------
document.getElementById('addProd').onclick = async () => {
  const sku = document.getElementById('p_sku').value.trim();
  const name = document.getElementById('p_name').value.trim();

  if (!sku || !name) {
    alert("SKU and Product name required");
    return;
  }

  const payload = {
    sku: sku,
    name: name,
    hsn: document.getElementById('p_hsn').value.trim(),
    mrp: parseFloat(document.getElementById('p_mrp').value || 0),
    rate: parseFloat(document.getElementById('p_rate').value || 0),
    pack: document.getElementById('p_pack').value.trim()
  };

  const res = await fetch("/products/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    alert(await res.text());
    return;
  }

  await loadProducts();
};

// ----------------------------------
// UPDATE PRODUCT
// ----------------------------------
async function updateProduct(id){
  const payload = {
    name: document.querySelector(`.edit_name[data-id="${id}"]`).value.trim(),
    hsn: document.querySelector(`.edit_hsn[data-id="${id}"]`).value.trim(),
    rate: parseFloat(document.querySelector(`.edit_rate[data-id="${id}"]`).value || 0),
    pack: document.querySelector(`.edit_pack[data-id="${id}"]`).value.trim()
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
    alert('Update failed');
    return;
  }

  await loadProducts();
}

// ----------------------------------
// DELETE PRODUCT
// ----------------------------------
async function deleteProduct(id){
  if(!confirm('Delete product?')) return;

  const res = await fetch(`${API_BASE}/products/delete/${id}`, {
    method:'DELETE',
    headers:{ Authorization:`Bearer ${token}` }
  });

  if(!res.ok){
    alert('Delete failed');
    return;
  }

  await loadProducts();
}

window.onload = loadProducts;
