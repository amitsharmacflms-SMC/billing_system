const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");
function goMenu(){ window.location.href = "/menu"; }

async function loadProducts(){
  const res = await fetch(`${API_BASE}/products/`, { headers:{ Authorization:`Bearer ${token}` }});
  const list = await res.json();
  const t = document.getElementById('prodBody'); t.innerHTML='';
  list.forEach(p=>{
    t.insertAdjacentHTML('beforeend', `<tr>
      <td>${p.id}</td><td><input data-id="${p.id}" class="edit_name" value="${p.name}"/></td>
      <td><input data-id="${p.id}" class="edit_hsn" value="${p.hsn||''}"/></td>
      <td><input data-id="${p.id}" class="edit_rate" value="${p.rate||0}"/></td>
      <td><input data-id="${p.id}" class="edit_pack" value="${p.pack||''}"/></td>
      <td>
        <button onclick="updateProduct(${p.id})">Save</button>
        <button onclick="deleteProduct(${p.id})">Delete</button>
      </td>
    </tr>`);
  });
}

document.getElementById('addProd').onclick = async ()=>{
  const payload = {
    name: document.getElementById('p_name').value,
    hsn: document.getElementById('p_hsn').value,
    rate: parseFloat(document.getElementById('p_rate').value||0),
    pack: document.getElementById('p_pack').value
  };
  const res = await fetch(`${API_BASE}/products/add`, {
    method:'POST', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload)
  });
  if(!res.ok){ alert('Add failed'); return; }
  await loadProducts();
};

async function updateProduct(id){
  const payload = {
    name: document.querySelector(`.edit_name[data-id="${id}"]`).value,
    hsn: document.querySelector(`.edit_hsn[data-id="${id}"]`).value,
    rate: parseFloat(document.querySelector(`.edit_rate[data-id="${id}"]`).value||0),
    pack: document.querySelector(`.edit_pack[data-id="${id}"]`).value
  };
  const res = await fetch(`${API_BASE}/products/update/${id}`, {
    method:'PUT', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload)
  });
  if(!res.ok){ alert('Update failed'); }
  await loadProducts();
}

async function deleteProduct(id){
  if(!confirm('Delete product?')) return;
  const res = await fetch(`${API_BASE}/products/delete/${id}`, {
    method:'DELETE', headers:{ Authorization:`Bearer ${token}` }
  });
  if(!res.ok){ alert('Delete failed'); }
  await loadProducts();
}

window.onload = loadProducts;
