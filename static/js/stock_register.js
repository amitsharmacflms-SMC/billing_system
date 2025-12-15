async function loadStockRegister() {
    const month = document.getElementById("monthFilter").value;
    const date = document.getElementById("dateFilter").value;

    if (!month && !date) {
        alert("Select Month or Date");
        return;
    }

    const params = new URLSearchParams();
    if (month) params.append("month", month);
    if (date) params.append("date", date);

    const res = await fetch(`/stock-register?${params.toString()}`, {
        headers: {
            Authorization: "Bearer " + localStorage.getItem("token")
        }
    });

    const data = await res.json();
    const tbody = document.getElementById("stockBody");
    tbody.innerHTML = "";

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6">No records</td></tr>`;
        return;
    }

    data.forEach(r => {
        tbody.innerHTML += `
            <tr>
                <td>${r.month}</td>
                <td>${r.date}</td>
                <td>${r.opening_qty}</td>
                <td>${r.received_qty}</td>
                <td>${r.out_qty}</td>
                <td>${r.balance_qty}</td>
            </tr>
        `;
    });
}

function exportExcel() {
    const month = document.getElementById("monthFilter").value;
    const date = document.getElementById("dateFilter").value;

    const params = new URLSearchParams();
    if (month) params.append("month", month);
    if (date) params.append("date", date);

    fetch(`/stock/stock-register?${params.toString()}`, {
    headers: {
        Authorization: "Bearer " + localStorage.getItem("token")
    }
});

    .then(res => res.blob())
    .then(blob => {
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "Stock_Register.xlsx";
        a.click();
    });
}
