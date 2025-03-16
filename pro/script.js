document.addEventListener("DOMContentLoaded", function() {
    console.log("VoiceMate website loaded successfully!");
    document.getElementById("loginButton").addEventListener("click", function() {
        window.location.href = "login.html";
    });
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const username = document.getElementById("username").value;
            alert(`Welcome, ${username}! Redirecting to chatbot...`);
            window.location.href = "chatbot.html";
        });
    }
    const sendButton = document.getElementById("sendButton");
    if (sendButton) {
        sendButton.addEventListener("click", function() {
            const userInput = document.getElementById("userInput").value;
            if (userInput.trim() !== "") {
                const chatBox = document.getElementById("chatBox");
                const userMessage = document.createElement("div");
                userMessage.classList.add("user-message");
                userMessage.innerText = userInput;
                chatBox.appendChild(userMessage);
                document.getElementById("userInput").value = "";
                setTimeout(() => {
                    const botMessage = document.createElement("div");
                    botMessage.classList.add("bot-message");
                    botMessage.innerText = "I'm here to help! What do you need?";
                    chatBox.appendChild(botMessage);
                }, 1000);
            }
        });
    }
});
document.getElementById("voiceForm").addEventListener("submit", function (event) {
    event.preventDefault();

    let name = document.getElementById("name").value;
    let voiceFile = document.getElementById("voice").files[0];

    if (!name || !voiceFile) {
        document.getElementById("statusMessage").innerText = "Please enter name and upload voice.";
        return;
    }

    // Simulating saving the file
    let formData = new FormData();
    formData.append("name", name);
    formData.append("voice", voiceFile);

    // Here, you would typically send formData to a server
    console.log("Saving data:", name, voiceFile);

    document.getElementById("statusMessage").innerText = "Data saved successfully!";
});
document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage("user", message);

        setTimeout(() => {
            const botResponse = getBotResponse(message);
            appendMessage("bot", botResponse);
        }, 1000);

        userInput.value = "";
    }

    function appendMessage(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.innerText = text;
        chatBox.appendChild(messageDiv);

        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    }

    function getBotResponse(userMessage) {
        const responses = {
            "hello": "Hey there! How can I assist you today? 😊",
            "how are you": "I'm an AI, but I'm always here to help! 🤖",
            "what is your name": "I'm VoiceMate AI, your smart assistant!",
            "bye": "Goodbye! Have a fantastic day! 🌟",
        };

        return responses[userMessage.toLowerCase()] || "I'm not sure, but I'm always learning! 🚀";
    }
});
