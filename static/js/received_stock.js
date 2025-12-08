const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){ window.location.href = "/menu"; }

async function loadStock(){
  const res = await fetch(`${API_BASE}/products/`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if(!res.ok){ console.error("Products fetch failed"); return; }
  const products = await res.json();
  const t = document.getElementById("stockBody");
  t.innerHTML = "";
  products.forEach(p=>{
    const row = `<tr>
      <td>${p.id}</td>
      <td>${p.name}</td>
      <td>${p.pack ?? ''}</td>
      <td>${p.rate ?? ''}</td>
      <td>${p.mrp ?? ''}</td>
      <td>${p.stock ?? '0'}</td>
    </tr>`;
    t.insertAdjacentHTML('beforeend', row);
  });
}
window.onload = loadStock;
