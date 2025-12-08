document.addEventListener("DOMContentLoaded", () => {
    const role = localStorage.getItem("role");
    const supplierId = localStorage.getItem("supplier_id");
    const name = localStorage.getItem("full_name") || "";

    console.log("ROLE =", role, "SUPPLIER =", supplierId);

    document.getElementById("welcomeUser").innerText = `Welcome, ${name}`;

    // Show / hide buttons based on role
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
