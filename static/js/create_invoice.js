const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");
const user_role = localStorage.getItem("user_role");
const supplier_id_local = localStorage.getItem("supplier_id");

async function loadDistributorsForInvoice(){
  let url;
  if(user_role === "supplier" && supplier_id_local){
    url = `${API_BASE}/distributors/by-supplier/${supplier_id_local}`;
  } else {
    url = `${API_BASE}/distributors/`;
  }
  const res = await fetch(url, { headers:{ Authorization:`Bearer ${token}` }});
  const list = await res.json();
  const buy = document.getElementById("buyerSelect");
  buy.innerHTML = '';
  list.forEach(d => buy.insertAdjacentHTML('beforeend', `<option value="${d.id}">${d.name} - ${d.city||''}</option>`));
}
