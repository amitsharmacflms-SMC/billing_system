async function login() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    const res = await fetch("/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    console.log("SERVER LOGIN RESPONSE:", data);
    console.log("STATUS:", res.status);

    if (!res.ok) {
        alert(data.error || "Login failed");
        return;
    }

    // SAVE VALUES IN LOCAL STORAGE
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user_role", data.role || "");
    localStorage.setItem("state", data.state || "");
    localStorage.setItem("supplier_id", data.supplier_id || "");

    console.log("LOGIN STORED:", data);

    window.location.href = "/menu";
}
