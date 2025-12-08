const API_BASE = "https://billingsystem-production.up.railway.app";  // your backend URL
const token = localStorage.getItem("token");

// Default headers
const authHeaders = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`
};


// ---------------------------
// LOAD PRODUCTS
// ---------------------------
async function loadProducts() {
    const res = await fetch(`${API_BASE}/products/`, {
        method: "GET",
        headers: authHeaders
    });

    if (!res.ok) {
        console.error("Failed to load products");
        return;
    }

    const data = await res.json();

    const container = document.getElementById("productsTableBody");
    container.innerHTML = "";

    data.forEach(p => {
        container.innerHTML += `
            <tr>
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.hsn}</td>
                <td>${p.mrp}</td>
                <td>${p.rate}</td>
                <td>${p.pack}</td>
            </tr>
        `;
    });
}


// ---------------------------
// LOAD DISTRIBUTORS
// ---------------------------
async function loadDistributors() {
    const res = await fetch(`${API_BASE}/distributors/`, {
        method: "GET",
        headers: authHeaders
    });

    if (!res.ok) {
        console.error("Distributor API Error");
        return;
    }

    const data = await res.json();
    const container = document.getElementById("distributorsTableBody");
    container.innerHTML = "";

    data.forEach(d => {
        container.innerHTML += `
            <tr>
                <td>${d.id}</td>
                <td>${d.name}</td>
                <td>${d.state}</td>
                <td>${d.city}</td>
                <td>${d.gstin}</td>
            </tr>
        `;
    });
}


// ---------------------------
// LOAD SUPPLIERS
// ---------------------------
async function loadSuppliers() {
    const res = await fetch(`${API_BASE}/suppliers/`, {
        method: "GET",
        headers: authHeaders
    });

    if (!res.ok) {
        console.error("Supplier API Error");
        return;
    }

    const data = await res.json();
    const container = document.getElementById("suppliersTableBody");
    container.innerHTML = "";

    data.forEach(s => {
        container.innerHTML += `
            <tr>
                <td>${s.id}</td>
                <td>${s.name}</td>
                <td>${s.state}</td>
                <td>${s.city}</td>
                <td>${s.gstin}</td>
            </tr>
        `;
    });
}


// ---------------------------
// CREATE INVOICE
// ---------------------------
async function createInvoice(invoiceData) {
    const res = await fetch(`${API_BASE}/api/invoices/create`, {
        method: "POST",
        headers: authHeaders,
        body: JSON.stringify(invoiceData)
    });

    const data = await res.json();
    if (!res.ok) {
        alert("Invoice creation failed: " + data.error);
        return null;
    }

    alert("Invoice Created: ID = " + data.invoice_id);
    return data.invoice_id;
}


// ---------------------------
// VIEW INVOICE HTML
// ---------------------------
function viewInvoice(invoiceID) {
    window.open(`${API_BASE}/invoice/${invoiceID}`, "_blank");
}
