// ----------------------------
// GLOBAL NAVIGATION FUNCTIONS
// ----------------------------
function goStockRegister() {
    window.location.href = "/stock-register-page";
}

function goReceivedStock() {
    window.location.href = "/received-stock";
}

function goCreateInvoice() {
    window.location.href = "/invoice/create";
}

function goSearchInvoice() {
    window.location.href = "/invoice/search";
}

function goReports() {
    window.location.href = "/reports";
}

// ----------------------------
// DOM READY
// ----------------------------
document.addEventListener("DOMContentLoaded", () => {
    const role = localStorage.getItem("role");
    const supplierId = localStorage.getItem("supplier_id");
    const name = localStorage.getItem("full_name") || "";

    console.log("ROLE =", role, "SUPPLIER =", supplierId);

    document.getElementById("welcomeUser").innerText = `Welcome, ${name}`;

    // Role-based visibility
    if (role === "admin") {
        document.getElementById("btnUserMgmt").style.display = "block";
        document.getElementById("btnProductUpdate").style.display = "block";
        document.getElementById("btnSupplierUpdate").style.display = "block";
        document.getElementById("btnDistributorUpdate").style.display = "block";
    }

    if (role === "supplier") {
        document.getElementById("btnProductUpdate").style.display = "none";
        document.getElementById("btnUserMgmt").style.display = "none";
    }

    // Logout
    document.getElementById("logoutBtn").onclick = () => {
        localStorage.clear();
        window.location.href = "/";
    };
});
