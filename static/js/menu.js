function goTo(path) {
    window.location.href = path;
}

function logout() {
    localStorage.clear();
    window.location.href = "/";
}

window.onload = () => {
    const role = localStorage.getItem("user_role");

    if (role === "admin") {
        document.getElementById("adminOptions").innerHTML = `
            <div class="menu-item" onclick="goTo('/product-update')">Product Update</div>
            <div class="menu-item" onclick="goTo('/suppliers-update')">Suppliers Update</div>
            <div class="menu-item" onclick="goTo('/distributors-update')">Distributors Update</div>
        `;
    }
};
