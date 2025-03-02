// auth.js - Handles user authentication (signup, login, logout, refresh token)

// ✅ Helper function to show messages
function showMessage(message, isSuccess = true) {
  const msgBox = document.getElementById("auth-message");
  msgBox.innerText = message;
  msgBox.style.color = isSuccess ? "green" : "red";
}

// 🔹 Signup Function
async function signup(username, password) {
  if (!username || !password) {
    showMessage("Please enter username and password", false);
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/api/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    console.log("Signup Response:", data);

    if (response.ok) {
      showMessage("Signup successful! You can now log in.");
      window.location.href = "login.html";
    } else {
      showMessage("Signup failed: " + (data.error || "Unknown error"), false);
    }
  } catch (error) {
    console.error("Error during signup:", error);
    showMessage("Error signing up", false);
  }
}

// 🔹 Login Function
async function login(username, password) {
  if (!username || !password) {
    showMessage("Please enter username and password", false);
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      credentials: "include", // ✅ Required for HTTP-only cookies
    });

    const data = await response.json();
    console.log("Login Response:", data);

    if (response.ok) {
      showMessage("Login successful!");
      sessionStorage.setItem("isLoggedIn", "true"); // ✅ Store login state
      window.location.href = "dashboard.html";
    } else {
      showMessage(
        "Login failed: " + (data.error || "Invalid credentials"),
        false
      );
    }
  } catch (error) {
    console.error("Error during login:", error);
    showMessage("Error logging in", false);
  }
}

// 🔹 Refresh Token Function
async function refreshToken() {
  try {
    const response = await fetch("http://localhost:8000/api/token/refresh/", {
      method: "POST",
      credentials: "include",
    });

    const data = await response.json();
    console.log("Token Refresh Response:", data);

    if (response.ok) {
      showMessage("Access token refreshed!");
    } else {
      showMessage(
        "Token refresh failed: " + (data.error || "Invalid refresh token"),
        false
      );
    }
  } catch (error) {
    console.error("Error refreshing token:", error);
    showMessage("Error refreshing token", false);
  }
}

// 🔹 Logout Function
async function logout() {
  try {
    const response = await fetch("http://localhost:8000/api/logout/", {
      method: "POST",
      credentials: "include",
    });

    console.log("Logout Response:", await response.json());

    if (response.ok) {
      showMessage("Logged out successfully!");
      sessionStorage.removeItem("isLoggedIn"); // ✅ Clear session state
      window.location.href = "login.html";
    } else {
      showMessage("Logout failed!", false);
    }
  } catch (error) {
    console.error("Error during logout:", error);
    showMessage("Error logging out", false);
  }
}
