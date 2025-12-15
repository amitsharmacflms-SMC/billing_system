async function loadProducts() {
    const res = await fetch("/stock/all-products", {
        headers: { Authorization: "Bearer " + localStorage.getItem("token") }
    });
    const products = await res.json();

    const sel = document.getElementById("product");
    sel.innerHTML = "";

    products.forEach(p => {
        sel.innerHTML += `<option value="${p.id}">${p.name}</option>`;
    });
}

async function loadRegister() {
    const product = document.getElementById("product").value;
    const month = document.getElementById("month").value;
    const year = document.getElementById("year").value;

    const res = await fetch(
        `/stock-register/monthly?product_id=${product}&month=${month}&year=${year}`,
        { headers: { Authorization: "Bearer " + localStorage.getItem("token") } }
    );

    const data = await res.json();

    document.getElementById("registerBody").innerHTML = `
      <tr>
        <td>${data.month}</td>
        <td>${data.opening_qty}</td>
        <td>${data.received_qty}</td>
        <td>${data.out_qty}</td>
        <td>${data.balance_qty}</td>
      </tr>`;
}

document.addEventListener("DOMContentLoaded", loadProducts);
