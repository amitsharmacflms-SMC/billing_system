// -------------------------------------
// LOAD STOCK REGISTER DATA
// -------------------------------------
function loadStockRegister() {

    const month = document.getElementById("month").value;
    const date = document.getElementById("date").value;

    let url = "/stock/stock-register?";

    if (month) {
        url += "month=" + month;
    } else if (date) {
        url += "date=" + date;
    } else {
        alert("Select Month or Date");
        return;
    }

    fetch(url, {
        headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
        }
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Server error");
        }
        return res.json();
    })
    .then(data => renderTable(data))
    .catch(err => {
        console.error(err);
        alert("Failed to load stock register");
    });
}


// -------------------------------------
// RENDER TABLE
// -------------------------------------
function renderTable(data) {

    const tbody = document.getElementById("stockBody");
    tbody.innerHTML = "";

    if (!data || data.length === 0) {
        tbody.innerHTML =
            "<tr><td colspan='5'>No records found</td></tr>";
        return;
    }

    data.forEach(row => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${row.product}</td>
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

    const month = document.getElementById("month").value;
    const date = document.getElementById("date").value;

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
                Authorization: "Bearer " + localStorage.getItem("token")
            }
        }
    )
    .then(res => res.blob())
    .then(blob => {
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = "Stock_Register.xlsx";
        link.click();
    })
    .catch(err => {
        console.error(err);
        alert("Export failed");
    });
}
