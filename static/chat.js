const username = localStorage.getItem("username") || "Аноним";

document.addEventListener("DOMContentLoaded", () => {
  const usernameText = document.getElementById("usernameText");
  if (usernameText) {
    usernameText.textContent = username;
  }
});

const logoutBtn = document.getElementById("logoutBtn");
logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("username");
  window.location.href = "/login";
});

function loadMessages() {
  fetch("/messages")
    .then(res => res.json())
    .then(data => {
      const messagesDiv = document.getElementById("messages");
      messagesDiv.innerHTML = "";
      data.messages.forEach(msg => {
        const div = document.createElement("div");
        div.textContent = `${msg.username}: ${msg.text}`;
        messagesDiv.appendChild(div);
      });
      messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

document.getElementById("messageForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const input = document.getElementById("messageInput");
  const text = input.value.trim();
  if (text.length === 0) return;

  fetch("/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, text })
  })
  .then(() => {
    input.value = "";
    loadMessages();
  });
});

setInterval(loadMessages, 1000);
loadMessages();
