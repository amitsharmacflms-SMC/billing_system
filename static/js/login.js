document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("loginForm");
    if (!form) {
        console.warn("loginForm not found on page.");
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value.trim();

        try {
            const res = await fetch("/auth/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();

            if (!res.ok) {
                alert(data.error || "Invalid login");
                return;
            }

            // Save session values
            localStorage.setItem("token", data.token);
            localStorage.setItem("role", data.role);
            localStorage.setItem("supplier_id", data.supplier_id);
            localStorage.setItem("state", data.state);
            localStorage.setItem("full_name", data.full_name);

            window.location.href = "/menu";

        } catch (err) {
            console.error("Login error:", err);
            alert("Network error");
        }
    });
});
