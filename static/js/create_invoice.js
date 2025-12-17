const API_CREATE = "/api/invoices/create";
const token = localStorage.getItem("token");

const authHeaders = {
  "Content-Type": "application/json",
  "Authorization": `Bearer ${token}`
};

let products = [];
let distributors = [];

/* ---------------- INIT ---------------- */
window.onload = async () => {
  await loadDistributors();
  await loadProducts();
  addItemRow(); // initial row
};

/* ---------------- LOAD DISTRIBUTORS ---------------- */
async function loadDistributors(){
  const res = await fetch("/distributors/", {
    headers: authHeaders
  });

  if(!res.ok){
    alert("Failed to load distributors (login expired?)");
    return;
  }

  distributors = await res.json();

  const ddl = document.getElementById("buyerSelect");
  ddl.innerHTML = `<option value="">-- Select Distributor --</option>`;

  distributors.forEach(d=>{
    ddl.innerHTML += `<option value="${d.id}">${d.name}</option>`;
  });
}

/* ---------------- LOAD PRODUCTS ---------------- */
async function loadProducts(){
  const res = await fetch("/products/", {
    headers: authHeaders
  });

  if(!res.ok){
    alert("Failed to load products (login expired?)");
    products = [];
    return;
  }

  const data = await res.json();

  // SAFETY: ensure array
  if(!Array.isArray(data)){
    console.error("Products API did not return array", data);
    products = [];
    return;
  }

  products = data;
}

/* ---------------- ADD ITEM ROW ---------------- */
function addItemRow(){
  if(!Array.isArray(products) || products.length === 0){
    alert("Products not loaded yet");
    return;
  }

  const tr = document.createElement("tr");

  tr.innerHTML = `
    <td>
      <select class="product">
        <option value="">Select</option>
        ${products.map(p =>
          `<option value="${p.id}">${p.name}</option>`
        ).join("")}
      </select>
    </td>
    <td><input type="number" class="pcs" value="0" min="0"></td>
    <td><input type="number" class="cs" value="0" min="0"></td>
    <td><input type="number" class="rate" value="${products[0]?.rate || 0}" min="0"></td>
    <td><input type="number" class="disc" value="0" min="0"></td>
    <td><input type="number" class="gst" value="5" min="0"></td>
    <td><button type="button" onclick="this.closest('tr').remove()">❌</button></td>
  `;

  document.getElementById("itemsBody").appendChild(tr);
}

/* ---------------- SAVE INVOICE ---------------- */
async function saveInvoice(){
  const invoice_no = document.getElementById("invoice_no").value.trim();
  const buyer_id = document.getElementById("buyerSelect").value;

  if(!invoice_no || !buyer_id){
    alert("Invoice number and distributor are required");
    return;
  }

  const items = [];

  document.querySelectorAll("#itemsBody tr").forEach(tr=>{
    const product_id = tr.querySelector(".product").value;
    if(!product_id) return;

    items.push({
      product_id: Number(product_id),
      pcs: Number(tr.querySelector(".pcs").value || 0),
      cs: Number(tr.querySelector(".cs").value || 0),
      rate: Number(tr.querySelector(".rate").value || 0),
      disc_percent: Number(tr.querySelector(".disc").value || 0),
      gst_percent: Number(tr.querySelector(".gst").value || 0)
    });
  });

  if(items.length === 0){
    alert("Add at least one product");
    return;
  }

  const res = await fetch(API_CREATE, {
    method: "POST",
    headers: authHeaders,
    body: JSON.stringify({
      invoice_no,
      buyer_id,
      items
    })
  });

  const data = await res.json();

  if(!res.ok){
    alert(data.error || "Invoice creation failed");
    return;
  }

  alert("Invoice created successfully");

  // Redirect to PRINT / VIEW invoice
  window.location.href = `/invoice/${data.invoice_id}`;
}
