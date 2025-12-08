function goTo(path) {
    window.location.href = path;
}

function logout() {
    localStorage.clear();
    window.location.href = "/";
}

window.onload = () => {

    const role = localStorage.getItem("user_role");
    const supplier_id = localStorage.getItem("supplier_id");

    console.log("LOGGED USER ROLE =", role, " SUPPLIER_ID =", supplier_id);

    // COMMON USERS (normal staff)
    if (role === "user") {
        document.getElementById("adminSection").style.display = "none";
        document.getElementById("supplierSection").style.display = "none";
    }

    // SUPPLIER ROLE
    if (role === "supplier") {
        document.getElementById("supplierSection").style.display = "block";
        document.getElementById("adminSection").style.display = "none";
    }

    // ADMIN ROLE
    if (role === "admin") {
        document.getElementById("adminSection").style.display = "block";
        document.getElementById("supplierSection").style.display = "block"; // Admins see stock register too
    }
};
