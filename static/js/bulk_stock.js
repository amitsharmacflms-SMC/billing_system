document.addEventListener("DOMContentLoaded", loadProducts);

async function loadProducts() {
    const token = localStorage.getItem("token");

    let res = await fetch("/stock/all-products", {
        headers: { "Authorization": "Bearer " + token }
    });

    let products = await res.json();

    let tbody = document.getElementById("productTable");
    tbody.innerHTML = products.map(p => `
        <tr>
            <td>${p.name}</td>
            <td>
                <input type="number" 
                       id="qty_${p.id}" 
                       step="0.01" 
                       placeholder="0">
            </td>
        </tr>
    `).join("");
}

async function submitStock() {
    const token = localStorage.getItem("token");

    const bill_no = document.getElementById("bill_no").value;
    const bill_date = document.getElementById("bill_date").value;

    if (!bill_no || !bill_date) {
        alert("Enter bill number and date");
        return;
    }

    // Collect all qty > 0
    let rows = document.querySelectorAll("input[id^='qty_']");
    let entries = [];

    rows.forEach(row => {
        let qty = parseFloat(row.value);
        if (qty > 0) {
            let product_id = row.id.replace("qty_", "");
            entries.push({ product_id, qty });
        }
    });

    if (entries.length === 0) {
        alert("Enter at least one quantity");
        return;
    }

    let payload = {
        bill_no,
        bill_date,
        entries
    };

    let res = await fetch("/stock/bulk-add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(payload)
    });

    let data = await res.json();

    if (res.ok) {
        alert(data.message);
        location.reload();
    } else {
        alert("Error: " + data.error);
    }
}
