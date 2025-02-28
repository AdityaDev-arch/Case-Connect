// auth.js - Handles user authentication (signup, login, logout, refresh token)

// 🔹 Signup Function
async function signup(username, password) {
  try {
    const response = await fetch("http://localhost:8000/api/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    console.log("Signup Response:", data);

    if (response.ok) {
      alert("Signup successful! You can now log in.");
    } else {
      alert("Signup failed: " + (data.error || "Unknown error"));
    }
  } catch (error) {
    console.error("Error during signup:", error);
  }
}

// 🔹 Login Function
async function login(username, password) {
  try {
    const response = await fetch("http://localhost:8000/api/token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      credentials: "include", // 🔹 Required for cookies
    });

    const data = await response.json();
    console.log("Login Response:", data);

    if (response.ok) {
      alert("Login successful!");
      window.location.href = "dashboard.html"; // Redirect to dashboard
    } else {
      alert("Login failed: " + (data.error || "Invalid credentials"));
    }
  } catch (error) {
    console.error("Error during login:", error);
  }
}

// 🔹 Refresh Token Function
async function refreshToken() {
  try {
    const response = await fetch("http://localhost:8000/api/token/refresh/", {
      method: "POST",
      credentials: "include", // 🔹 Required for cookies
    });

    const data = await response.json();
    console.log("Token Refresh Response:", data);

    if (response.ok) {
      alert("Access token refreshed!");
    } else {
      alert("Token refresh failed: " + (data.error || "Invalid refresh token"));
    }
  } catch (error) {
    console.error("Error refreshing token:", error);
  }
}

// 🔹 Logout Function
async function logout() {
  try {
    const response = await fetch("http://localhost:8000/api/logout/", {
      method: "POST",
      credentials: "include", // 🔹 Required for cookies
    });

    console.log("Logout Response:", await response.json());

    if (response.ok) {
      alert("Logged out successfully!");
      window.location.href = "login.html"; // Redirect to login page
    } else {
      alert("Logout failed!");
    }
  } catch (error) {
    console.error("Error during logout:", error);
  }
}
