document.addEventListener("DOMContentLoaded", loadStockSummary);

function loadStockSummary() {

    fetch("/stock/stock-summary", {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
        }
    })
    .then(res => {
        if (!res.ok) throw new Error("Failed to load");
        return res.json();
    })
    .then(data => {
        const tbody = document.getElementById("stockBody");
        tbody.innerHTML = "";

        if (data.length === 0) {
            tbody.innerHTML = "<tr><td colspan='5'>No stock data</td></tr>";
            return;
        }

        data.forEach(row => {
            tbody.innerHTML += `
                <tr>
                    <td>${row.product}</td>
                    <td>${row.opening_qty}</td>
                    <td>${row.received_qty}</td>
                    <td>${row.out_qty}</td>
                    <td><b>${row.balance_qty}</b></td>
                </tr>
            `;
        });
    })
    .catch(err => {
        console.error(err);
        alert("Unable to load stock summary");
    });
}
