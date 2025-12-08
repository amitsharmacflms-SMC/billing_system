const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){ window.location.href = "/menu"; }

document.getElementById('run').onclick = async ()=>{
  const from = document.getElementById('from').value;
  const to = document.getElementById('to').value;
  if(!from || !to){ alert('Select dates'); return; }
  // No dedicated report endpoint exists yet — we will fetch invoices and filter client-side
  const res = await fetch(`${API_BASE}/api/invoices`, { headers:{ Authorization:`Bearer ${token}` } });
  if(!res.ok){ document.getElementById('reportResults').innerText = 'Unable to fetch'; return; }
  const list = await res.json();
  const filtered = list.filter(inv=>{
    const d = new Date(inv.date || inv.created_at || Date.now());
    return d >= new Date(from) && d <= new Date(to);
  });
  const html = `<div>Found ${filtered.length} invoices</div>` + filtered.map(i=>`<div>Invoice ${i.invoice_no || i.id} - <button onclick="openInv(${i.id})">Open</button></div>`).join('');
  document.getElementById('reportResults').innerHTML = html;
};

function openInv(id){ window.open(`${API_BASE}/invoice/${id}`,'_blank'); }
