const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu() { window.location.href = "/menu"; }

// ------------------------------------------------------------------
// LOAD PRODUCTS INTO DROPDOWN FOR FILTERING
// ------------------------------------------------------------------
async function loadProducts() {
    const res = await fetch(`${API_BASE}/products/`, {
        headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();

    const select = document.getElementById("productFilter");
    data.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = p.name;
        select.appendChild(opt);
    });
}

// ------------------------------------------------------------------
// LOAD STOCK ENTRIES (LEDGER)
// ------------------------------------------------------------------
async function loadStockEntries() {
    let url = `${API_BASE}/stock/entries`;

    const product_id = document.getElementById("productFilter").value;
    const fromDate = document.getElementById("fromDate").value;
    const toDate = document.getElementById("toDate").value;

    if (product_id) url += `?product_id=${product_id}`;

    const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` }
    });

    let data = await res.json();

    // FILTER BY DATE RANGE (client side)
    if (fromDate) {
        data = data.filter(x => x.date >= fromDate);
    }
    if (toDate) {
        data = data.filter(x => x.date <= toDate);
    }

    const tbody = document.getElementById("stockRegisterBody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='5' style='text-align:center;'>No Records Found</td></tr>";
        return;
    }

    data.forEach(r => {
        tbody.innerHTML += `
            <tr>
                <td>${r.date}</td>
                <td>${r.product_name}</td>
                <td>${r.received_cs}</td>
                <td>${r.invoice_no || '-'}</td>
                <td>${r.remarks || ''}</td>
            </tr>
        `;
    });
}

// ------------------------------------------------------------------
// APPLY FILTER BUTTON
// ------------------------------------------------------------------
function applyFilter() {
    loadStockEntries();
}

// ------------------------------------------------------------------
window.onload = async function () {
    await loadProducts();
    await loadStockEntries();
};
