// -------------------------------------
// AUTO CLEAR MONTH / DATE (UX FIX)
// -------------------------------------
document.addEventListener("DOMContentLoaded", () => {

    const monthEl = document.getElementById("month");
    const dateEl  = document.getElementById("date");

    // Clear date when month selected
    monthEl.addEventListener("change", () => {
        dateEl.value = "";
    });

    // Clear month when date selected
    dateEl.addEventListener("change", () => {
        monthEl.value = "";
    });
});


// -------------------------------------
// LOAD STOCK REGISTER DATA
// -------------------------------------
function loadStockRegister() {

    const month = document.getElementById("month").value;
    const date  = document.getElementById("date").value;

    if (!month && !date) {
        alert("Select Month or Date");
        return;
    }

    let url = "/stock/stock-register?";

    if (month) {
        url += "month=" + month;
    } else {
        url += "date=" + date;
    }

    fetch(url, {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token")
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
            "<tr><td colspan='6'>No records found</td></tr>";
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
