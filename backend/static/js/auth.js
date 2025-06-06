// auth.js - Handles user authentication (signup, login, logout)

// ✅ Helper function to show messages
function showMessage(message, isSuccess = true) {
  const msgBox = document.getElementById("auth-message");
  msgBox.innerText = message;
  msgBox.style.color = isSuccess ? "green" : "red";
}

// 🔹 Firebase Configuration
// auth.js - Modular Firebase Authentication

import { initializeApp } from "firebase/app";
import { getDoc, doc } from "firebase/firestore";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from "firebase/auth";
import { getFirestore, doc, setDoc, serverTimestamp } from "firebase/firestore";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBGTHQb_4PTadKiHBsfh5PL9GyJ9MUprKU",
  authDomain: "caseconnect-87388.firebaseapp.com",
  projectId: "caseconnect-87388",
  storageBucket: "caseconnect-87388.appspot.com", // FIXED TYPING ISSUE
  messagingSenderId: "765279832041",
  appId: "1:765279832041:web:fe6f5bb802cb7a8f4fad78",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// ✅ Helper to show messages
function showMessage(message, isSuccess = true) {
  alert(message); // Replace with UI element if needed
}

// ✅ Signup handler (for signup.html)
const signupForm = document.getElementById("signup-form");
if (signupForm) {
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fullName = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const role = document.getElementById("role").value; // admin or user

    // 🔐 If admin, validate secret
    if (role === "admin") {
      const adminSecret = document.getElementById("admin_secret").value;
      const expectedSecret = "your-secret-key"; // Replace with secure value

      if (adminSecret !== expectedSecret) {
        showMessage("Invalid Admin Secret", false);
        return;
      }
    }

    try {
      const userCredential = await createUserWithEmailAndPassword(
        auth,
        email,
        password
      );
      const user = userCredential.user;

      await setDoc(doc(db, "users", user.uid), {
        name: fullName,
        email: user.email,
        role: role,
        createdAt: serverTimestamp(),
      });

      showMessage("Signup successful!");
      window.location.href = "/signin";
    } catch (error) {
      console.error("Signup error:", error);
      showMessage("Signup failed: " + error.message, false);
    }
  });
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

    // Debug: Log the token
    console.log("Generated ID Token:", token);

    // Send the token to the backend for verification
    const response = await fetch("http://localhost:8000/api/verify-token/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token }),
    });

    const data = await response.json();
    console.log("Login Response from Backend:", data);

    if (response.ok) {
      // Store the token and role in sessionStorage
      sessionStorage.setItem("token", token); // ✅ Store the token
      sessionStorage.setItem("role", data.role); // ✅ Store the user's role

      // Debug: Verify stored token and role
      console.log("Stored Token:", sessionStorage.getItem("token"));
      console.log("Stored Role:", sessionStorage.getItem("role"));

      // Redirect based on role
      if (data.role === "admin") {
        window.location.href = "/admin-dashboard";
      } else if (data.role === "user") {
        window.location.href = "/user-dashboard";
      } else {
        showMessage("Unknown role. Please contact support.", false);
      }
    } else {
      // Handle backend errors
      showMessage(
        "Login failed: " + (data.message || "Invalid credentials"),
        false
      );
    }
  } catch (error) {
    // Handle client-side errors
    console.error("Error during login:", error);
    showMessage("Error logging in: " + error.message, false);
  }
}

// Signin logic (inside your signin.html or linked script)
document
  .getElementById("signin-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    // Show loading spinner
    document.getElementById("signin-button").style.display = "none";
    document.getElementById("loading-spinner").style.display = "block";

    try {
      // Authenticate user
      const userCredential = await signInWithEmailAndPassword(
        auth,
        email,
        password
      );

      const user = userCredential.user;

      console.log("User signed in:", user.uid);

      // Retrieve user data from Firestore

      const userDocRef = doc(db, "users", user.uid);
      const docSnap = await getDoc(userDocRef);

      if (docSnap.exists) {
        console.log("User data found:", docSnap.data());

        // Get ID token
        const token = await user.getIdToken();
        const role = docSnap.data().role || "user";

        // Send token to backend
        const response = await fetch(
          "http://localhost:8000/api/verify-token/",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ token }),
          }
        );

        const data = await response.json();

        if (response.ok) {
          // Store in sessionStorage
          sessionStorage.setItem("token", token);
          sessionStorage.setItem("role", role);

          // Redirect
          if (role === "admin") {
            window.location.href = "/admin-dashboard";
          } else {
            window.location.href = "/user-dashboard";
          }
        } else {
          alert(data.message || "Token verification failed");
        }
      } else {
        alert("User data not found in Firestore.");
        console.error("User doc does not exist");
      }
    } catch (error) {
      console.error("Sign-in error:", error);
      alert("Sign-in failed: " + error.message);
    } finally {
      // Show button again if error
      document.getElementById("signin-button").style.display = "block";
      document.getElementById("loading-spinner").style.display = "none";
    }
  });

if (role === "admin") {
  const adminSecret = document.getElementById("admin_secret").value;
  if (adminSecret !== "your-secret-key") {
    showMessage("Invalid Admin Secret", false);
    return;
  }
}

// 🔹 Check Authentication (Protect Frontend Pages)
function checkAuthentication() {
  const token = sessionStorage.getItem("token");
  if (!token) {
    alert("You are not logged in. Redirecting to login page.");
    window.location.href = "/signin"; // Redirect to the sign-in page
    return;
  }

  // Verify the token with the backend
  fetch("/protected-route", {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`, // Include the token in the Authorization header
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Unauthorized access");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Authenticated:", data.message);
    })
    .catch((error) => {
      console.error("Authentication error:", error);
      alert("Session expired. Please log in again.");
      window.location.href = "/signin"; // Redirect to the sign-in page
    });
}

// 🔹 Logout Function
async function logout() {
  try {
    // Sign out the user using Firebase Authentication
    await signOut(auth);

    showMessage("Logged out successfully!");
    sessionStorage.removeItem("token"); // ✅ Clear the token
    sessionStorage.removeItem("role"); // ✅ Clear the role
    window.location.href = "signin.html"; // Redirect to login page
  } catch (error) {
    console.error("Error during logout:", error);
    showMessage("Error logging out: " + error.message, false);
  }
}

// 🔹 Fetch Protected Route
async function fetchProtectedRoute() {
  const token = sessionStorage.getItem("token"); // Retrieve the token

  if (!token) {
    alert("You are not logged in. Please log in first.");
    window.location.href = "/signin";
    return;
  }

  try {
    const response = await fetch("/protected-route", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`, // Include the token in the Authorization header
      },
    });

    const data = await response.json();

    if (response.ok) {
      console.log(data.message); // Log the welcome message
    } else {
      alert(data.message || "Access denied");
    }
  } catch (error) {
    console.error("Error accessing protected route:", error);
    alert("An error occurred. Please try again.");
  }
}

// 🔹 Decode Token (Optional)
function decodeToken(token) {
  const payload = JSON.parse(atob(token.split(".")[1])); // Decode the JWT payload
  return payload;
}

// Example usage of decodeToken
const token = sessionStorage.getItem("token");
if (token) {
  const userInfo = decodeToken(token);
  console.log("User Info:", userInfo);
}
