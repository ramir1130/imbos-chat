document.getElementById("registerForm").addEventListener("submit", function(e) {
    e.preventDefault();
  
    const username = e.target.username.value;
    const password = e.target.password.value;
  
    fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        localStorage.setItem("username", username);
        alert("Регистрация прошла успешно!");
        window.location.href = "/login";
      } else {
        alert("Ошибка регистрации: " + data.message);
      }
    });
  });
  