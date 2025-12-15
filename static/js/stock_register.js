async function loadProducts() {
    const res = await fetch("/stock/all-products", {
        headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
        }
    });

    const products = await res.json();
    const sel = document.getElementById("product");
    sel.innerHTML = "";

    products.forEach(p => {
        sel.innerHTML += `<option value="${p.id}">${p.name}</option>`;
    });
}


async function loadYearlyRegister() {
    const productId = document.getElementById("product").value;
    const year = document.getElementById("year").value;

    if (!productId || !year) {
        alert("Select product and year");
        return;
    }

    const res = await fetch(
        `/stock-register/yearly?product_id=${productId}&year=${year}`,
        {
            headers: {
                Authorization: "Bearer " + localStorage.getItem("token")
            }
        }
    );

    const data = await res.json();
    const tbody = document.getElementById("registerBody");
    tbody.innerHTML = "";

    data.forEach(row => {
        tbody.innerHTML += `
            <tr>
                <td>${row.month}</td>
                <td>${row.opening_qty}</td>
                <td>${row.received_qty}</td>
                <td>${row.out_qty}</td>
                <td>${row.balance_qty}</td>
            </tr>
        `;
    });
}


function exportExcel() {
    const productId = document.getElementById("product").value;
    const year = document.getElementById("year").value;

    if (!productId || !year) {
        alert("Select product and year");
        return;
    }

    const token = localStorage.getItem("token");

    const url = `/stock-register/yearly-export?product_id=${productId}&year=${year}`;

    fetch(url, {
        headers: {
            Authorization: "Bearer " + token
        }
    })
    .then(res => res.blob())
    .then(blob => {
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = `Stock_Register_${year}.xlsx`;
        link.click();
    });
}


document.addEventListener("DOMContentLoaded", loadProducts);
