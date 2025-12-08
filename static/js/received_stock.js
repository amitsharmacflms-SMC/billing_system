const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu() { window.location.href = "/menu"; }


// ----------------------------------------
// LOAD STOCK SUMMARY
// ----------------------------------------
async function loadStock(){
    const res = await fetch(`${API_BASE}/stock/summary`, {
        headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();
    const tbody = document.getElementById("stockBody");
    tbody.innerHTML = "";

    data.forEach(row => {
        tbody.innerHTML += `
            <tr>
                <td>${row.product_name}</td>
                <td>${row.received_cs}</td>
                <td>${row.sold_cs}</td>
                <td><b>${row.current_stock_cs}</b></td>
                <td><button onclick="openAddStock(${row.product_id}, '${row.product_name}')">Add</button></td>
            </tr>
        `;
    });
}


// ----------------------------------------
// ADD STOCK POPUP
// ----------------------------------------
function openAddStock(id, name){
    const received_cs = prompt(`Enter cases to add for ${name}:`);
    if (!received_cs) return;

    const invoice_no = prompt("Enter Invoice No (optional):");
    const remarks = prompt("Remarks:");

    const payload = {
        product_id: id,
        date: new Date().toISOString().split("T")[0],
        received_cs: received_cs,
        invoice_no: invoice_no,
        remarks: remarks
    };

    submitStock(payload);
}


// ----------------------------------------
// SUBMIT STOCK TO BACKEND
// ----------------------------------------
async function submitStock(payload){
    const res = await fetch(`${API_BASE}/stock/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });

    const data = await res.json();

    if(res.ok){
        alert("Stock Added Successfully!");
        loadStock();
    } else {
        alert("Error: " + data.error);
    }
}


window.onload = loadStock;
