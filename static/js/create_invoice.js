const API_CREATE = "/api/invoices/create";
const token = localStorage.getItem("token");

const authHeaders = {
  "Content-Type": "application/json",
  "Authorization": `Bearer ${token}`
};

let products = [];

/* ---------------- INIT ---------------- */
window.onload = async () => {
  await loadDistributors();
  await loadProducts();
  addItemRow();
};

/* ---------------- LOAD DISTRIBUTORS ---------------- */
async function loadDistributors(){
  const res = await fetch("/distributors/", { headers: authHeaders });
  const data = await res.json();

  const ddl = document.getElementById("buyerSelect");
  ddl.innerHTML = `<option value="">-- Select Distributor --</option>`;
  data.forEach(d=>{
    ddl.innerHTML += `<option value="${d.id}">${d.name}</option>`;
  });
}

/* ---------------- LOAD PRODUCTS ---------------- */
async function loadProducts(){
  const res = await fetch("/products/", { headers: authHeaders });
  products = await res.json();
}

/* ---------------- ADD ITEM ROW ---------------- */
function addItemRow(){
  const tr = document.createElement("tr");

  tr.innerHTML = `
    <td>
      <select class="product">
        <option value="">Select</option>
        ${products.map(p => `<option value="${p.id}">${p.name}</option>`).join("")}
      </select>
    </td>
    <td class="stock">-</td>
    <td><input type="number" class="pcs" value="0"></td>
    <td><input type="number" class="cs" value="0"></td>
    <td><input type="number" class="rate" value="0"></td>
    <td><input type="number" class="disc" value="0"></td>
    <td><input type="number" class="gst" value="5"></td>
    <td><button onclick="this.closest('tr').remove(); recalcTotals()">❌</button></td>
  `;

  const productSelect = tr.querySelector(".product");
  const csInput = tr.querySelector(".cs");
  const rateInput = tr.querySelector(".rate");
  const stockCell = tr.querySelector(".stock");

  productSelect.addEventListener("change", async ()=>{
    const pid = productSelect.value;
    if(!pid) return;

    const prod = products.find(p => p.id == pid);
    rateInput.value = prod.rate || 0;

    const res = await fetch(`/stock/available/${pid}`, { headers: authHeaders });
    const data = await res.json();

    stockCell.innerText = data.available_cs;

    if(data.available_cs <= 0){
      csInput.value = 0;
      csInput.disabled = true;
    } else {
      csInput.disabled = false;
    }
  });

  csInput.addEventListener("input", ()=>{
    const max = Number(stockCell.innerText || 0);
    if(Number(csInput.value) > max){
      csInput.value = max;
      alert("Insufficient stock");
    }
    recalcTotals();
  });

  tr.querySelectorAll("input").forEach(i =>
    i.addEventListener("input", recalcTotals)
  );

  document.getElementById("itemsBody").appendChild(tr);
}

/* ---------------- TOTALS ---------------- */
function recalcTotals(){
  let taxable = 0, gst = 0;

  document.querySelectorAll("#itemsBody tr").forEach(tr=>{
    const pcs = Number(tr.querySelector(".pcs").value || 0);
    const rate = Number(tr.querySelector(".rate").value || 0);
    const disc = Number(tr.querySelector(".disc").value || 0);
    const gstp = Number(tr.querySelector(".gst").value || 0);

    const t = rate * pcs * (1 - disc / 100);
    const g = t * gstp / 100;

    taxable += t;
    gst += g;
  });

  document.getElementById("taxableTotal").innerText = taxable.toFixed(2);
  document.getElementById("gstTotal").innerText = gst.toFixed(2);
  document.getElementById("grandTotal").innerText = (taxable + gst).toFixed(2);
}

/* ---------------- SAVE INVOICE ---------------- */
async function saveInvoice(){
  const invoiceNoInput = document.getElementById("invoice_no");
  const buyerSelectEl = document.getElementById("buyerSelect");

  const invoice_no = invoiceNoInput.value.trim();
  const buyer_id = buyerSelectEl.value;

  if(!invoice_no || !buyer_id){
    alert("Invoice number and distributor are required");
    return;
  }

  const items = [];
  document.querySelectorAll("#itemsBody tr").forEach(tr=>{
    const pid = tr.querySelector(".product").value;
    if(!pid) return;

    items.push({
      product_id: Number(pid),
      pcs: Number(tr.querySelector(".pcs").value || 0),
      cs: Number(tr.querySelector(".cs").value || 0),
      rate: Number(tr.querySelector(".rate").value || 0),
      disc_percent: Number(tr.querySelector(".disc").value || 0),
      gst_percent: Number(tr.querySelector(".gst").value || 0)
    });
  });

  if(items.length === 0){
    alert("Add at least one item");
    return;
  }

  const res = await fetch("/api/invoices/create", {
    method: "POST",
    headers: authHeaders,
    body: JSON.stringify({ invoice_no, buyer_id, items })
  });

  const data = await res.json();
  if(!res.ok){
    alert(data.error || "Invoice creation failed");
    return;
  }

  alert("Invoice created successfully");
  window.location.href = `/invoice/${data.invoice_id}`;
}
