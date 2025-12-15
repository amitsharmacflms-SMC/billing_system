// -------------------------------------
// LOAD STOCK REGISTER DATA
// -------------------------------------
async function loadStockRegister() {

    const monthEl = document.getElementById("monthFilter");
    const dateEl = document.getElementById("dateFilter");

    const month = monthEl ? monthEl.value : "";
    const date = dateEl ? dateEl.value : "";

    if (!month && !date) {
        alert("Please select Month or Date");
        return;
    }

    const params = new URLSearchParams();
    if (month) params.append("month", month);
    if (date) params.append("date", date);

    const res = await fetch(
        "/stock/stock-register?" + params.toString(),
        {
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("token")
            }
        }
    );

    if (!res.ok) {
        alert("Failed to load stock register");
        return;
    }

    const data = await res.json();
    const tbody = document.getElementById("stockBody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = "<tr><td colspan='6'>No records found</td></tr>";
        return;
    }

    data.forEach(row => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${row.month}</td>
            <td>${row.date}</td>
            <td>${row.opening_qty}</td>
            <td>${row.received_qty}</td>
            <td>${row.out_qty}</td>
            <td>${row.balance_qty}</td>
        `;

        tbody.appendChild(tr);
    });
}

// -------------------------------------
// EXPORT TO EXCEL
// -------------------------------------
function exportExcel() {

    const month = document.getElementById("monthFilter").value;
    const date = document.getElementById("dateFilter").value;

    if (!month && !date) {
        alert("Please select Month or Date");
        return;
    }

    const params = new URLSearchParams();
    if (month) params.append("month", month);
    if (date) params.append("date", date);

    fetch(
        "/stock/stock-register/export?" + params.toString(),
        {
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("token")
            }
        }
    )
    .then(res => res.blob())
    .then(blob => {
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "Stock_Register.xlsx";
        link.click();
    });
}
