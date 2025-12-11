document.addEventListener("DOMContentLoaded", loadProducts);

async function loadProducts() {
    const token = localStorage.getItem("token");

    let res = await fetch("/stock/products", {
        headers: { "Authorization": "Bearer " + token }
    });

    let data = await res.json();

    let select = document.getElementById("product");
    select.innerHTML = data.map(p =>
        `<option value="${p.id}">${p.name}</option>`
    ).join("");
}


async function saveStock() {
    const token = localStorage.getItem("token");

    const payload = {
        product_id: document.getElementById("product").value,
        bill_no: document.getElementById("bill_no").value,
        bill_date: document.getElementById("bill_date").value,
        received_cs: document.getElementById("received_cs").value,
        remarks: document.getElementById("remarks").value
    };

    let res = await fetch("/stock/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(payload)
    });

    let data = await res.json();

    if (res.ok) {
        alert("Stock added successfully!");
        location.reload();
    } else {
        alert("Error: " + data.error);
    }
}
