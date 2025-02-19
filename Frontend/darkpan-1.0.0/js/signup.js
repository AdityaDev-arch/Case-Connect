//for handling the Sign Up form submission
document
  .getElementById("signup-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the page from reloading

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const signupData = {
      username: username,
      email: email,
      password: password,
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/api/signup/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(signupData),
      });

      const result = await response.json();

      if (response.ok) {
        document.getElementById("signup-message").innerText =
          "Signup successful!";
        document.getElementById("signup-message").style.color = "green";
        document.getElementById("signup-form").reset();
      } else {
        document.getElementById("signup-message").innerText =
          result.error || "Signup failed.";
        document.getElementById("signup-message").style.color = "red";
      }
    } catch (error) {
      document.getElementById("signup-message").innerText =
        "An error occurred.";
      document.getElementById("signup-message").style.color = "red";
    }
  });
