const API_BASE = "https://billingsystem-production.up.railway.app";

function togglePassword() {
    const pass = document.getElementById("password");
    const btn = document.querySelector(".showpass");
    
    if (pass.type === "password") {
        pass.type = "text";
        btn.textContent = "Hide";
    } else {
        pass.type = "password";
        btn.textContent = "Show";
    }
}

async function login() {
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    const response = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
        document.getElementById("error").innerText = "Invalid email or password";
        return;
    }

    // Save JWT + role
    localStorage.setItem("token", data.access_token);

    const me = await fetch(`${API_BASE}/auth/me`, {
        headers: { Authorization: `Bearer ${data.access_token}` }
    }).then(r => r.json());

    localStorage.setItem("user_role", me.role);

    // Redirect to menu
    window.location.href = "/menu";
}
