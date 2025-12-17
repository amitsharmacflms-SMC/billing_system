const API = "/api/invoices/create";

let products = [];
let distributors = [];

/* ---------------- INIT ---------------- */
window.onload = async () => {
  await loadDistributors();
  await loadProducts();
  addItemRow(); // start with one row
};

/* ---------------- LOAD DATA ---------------- */
async function loadDistributors(){
  const res = await fetch("/distributors/");
  distributors = await res.json();

  const ddl = document.getElementById("buyerSelect");
  ddl.innerHTML = `<option value="">-- Select Distributor --</option>`;
  distributors.forEach(d=>{
    ddl.innerHTML += `<option value="${d.id}">${d.name}</option>`;
  });
}

async function loadProducts(){
  const res = await fetch("/products/");
  products = await res.json();
}

/* ---------------- ADD ROW (FIXES YOUR ERROR) ---------------- */
function addItemRow(){
  const tr = document.createElement("tr");

  tr.innerHTML = `
    <td>
      <select class="product">
        <option value="">Select</option>
        ${products.map(p => `<option value="${p.id}">${p.name}</option>`).join("")}
      </select>
    </td>
    <td><input type="number" class="pcs" value="0"></td>
    <td><input type="number" class="cs" value="0"></td>
    <td><input type="number" class="rate" value="0"></td>
    <td><input type="number" class="disc" value="0"></td>
    <td><input type="number" class="gst" value="5"></td>
    <td><button onclick="this.closest('tr').remove()">❌</button></td>
  `;

  document.getElementById("itemsBody").appendChild(tr);
}

/* ---------------- SAVE INVOICE ---------------- */
async function saveInvoice(){
  const invoice_no = document.getElementById("invoice_no").value;
  const buyer_id = document.getElementById("buyerSelect").value;

  if(!invoice_no || !buyer_id){
    alert("Invoice number and distributor required");
    return;
  }

  const items = [];
  document.querySelectorAll("#itemsBody tr").forEach(tr=>{
    const product_id = tr.querySelector(".product").value;
    if(!product_id) return;

    items.push({
      product_id: product_id,
      pcs: tr.querySelector(".pcs").value,
      cs: tr.querySelector(".cs").value,
      rate: tr.querySelector(".rate").value,
      disc_percent: tr.querySelector(".disc").value,
      gst_percent: tr.querySelector(".gst").value
    });
  });

  if(items.length === 0){
    alert("Add at least one product");
    return;
  }

  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      invoice_no,
      buyer_id,
      items
    })
  });

  const data = await res.json();

  if(!res.ok){
    alert(data.error);
    return;
  }

  alert("Invoice created successfully");

  // redirect to print/view invoice
  window.location.href = `/invoice/${data.invoice_id}`;
}
