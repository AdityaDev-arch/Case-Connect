// auth.js - Handles user authentication (signup, login, logout)

// ✅ Helper function to show messages
function showMessage(message, isSuccess = true) {
  const msgBox = document.getElementById("auth-message");
  msgBox.innerText = message;
  msgBox.style.color = isSuccess ? "green" : "red";
}

// 🔹 Firebase Configuration
import { initializeApp } from "firebase/app";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// 🔹 Signup Function
async function signup(email, password) {
  if (!email || !password) {
    showMessage("Please enter email and password", false);
    return;
  }

  try {
    // Create a new user using Firebase Authentication
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    );
    const user = userCredential.user;

    console.log("Signup successful:", user);
    showMessage("Signup successful! You can now log in.");
    window.location.href = "signin.html"; // Redirect to login page
  } catch (error) {
    console.error("Error during signup:", error);
    showMessage("Signup failed: " + error.message, false);
  }
}

// 🔹 Login Function
async function login(email, password) {
  if (!email || !password) {
    showMessage("Please enter email and password", false);
    return;
  }

  try {
    // Sign in the user using Firebase Authentication
    const userCredential = await signInWithEmailAndPassword(
      auth,
      email,
      password
    );
    const user = userCredential.user;

    // Get the user's ID token
    const token = await user.getIdToken();

    // Send the token to the backend for verification
    const response = await fetch("http://localhost:8000/api/verify-token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });

    const data = await response.json();
    console.log("Login Response:", data);

    if (response.ok) {
      showMessage("Login successful!");
      sessionStorage.setItem("isLoggedIn", "true"); // ✅ Store login state
      window.location.href = "index.html"; // Redirect to dashboard
    } else {
      showMessage(
        "Login failed: " + (data.error || "Invalid credentials"),
        false
      );
    }
  } catch (error) {
    console.error("Error during login:", error);
    showMessage("Error logging in: " + error.message, false);
  }
}

// 🔹 Logout Function
async function logout() {
  try {
    // Sign out the user using Firebase Authentication
    await signOut(auth);

    showMessage("Logged out successfully!");
    sessionStorage.removeItem("isLoggedIn"); // ✅ Clear session state
    window.location.href = "signin.html"; // Redirect to login page
  } catch (error) {
    console.error("Error during logout:", error);
    showMessage("Error logging out: " + error.message, false);
  }
}

// 🔹 Fetch Protected Route
async function fetchProtectedRoute() {
  // Fetch the JWT token from sessionStorage or localStorage
  const token = sessionStorage.getItem("token"); // Or use localStorage.getItem('token')

  // Check if the token exists
  if (!token) {
    showMessage("You are not logged in. Please sign in first.", false);
    window.location.href = "/signin"; // Redirect to the sign-in page
    return;
  }

  try {
    // Make a request to the protected route
    const response = await fetch("/protected-route", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`, // Include the token
      },
    });

    const data = await response.json();

    if (response.ok) {
      console.log(data.message); // Log the welcome message
      showMessage(data.message, true); // Display the message in the UI
    } else {
      showMessage("Access denied: " + (data.message || "Unknown error"), false);
    }
  } catch (error) {
    console.error("Error accessing protected route:", error);
    showMessage("Error accessing protected route. Please try again.", false);
  }
}
