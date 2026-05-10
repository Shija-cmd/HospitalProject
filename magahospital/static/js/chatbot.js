function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;

            }

        }

    }

    return cookieValue;

}
const chatToggle = document.getElementById("chat-toggle");
const chatBox = document.getElementById("chat-box");
const closeChat = document.getElementById("close-chat");

if(chatToggle && chatBox){

    chatToggle.onclick = () => {

        if(chatBox.style.display === "flex"){
            chatBox.style.display = "none";
        } else {
            chatBox.style.display = "flex";
        }

    };

}

if(closeChat){

    closeChat.onclick = () => {
        chatBox.style.display = "none";
    };

}

const sendBtn = document.getElementById("send-btn");
const chatInput = document.getElementById("chat-input");
const chatBody = document.getElementById("chat-body");

if(sendBtn){

    function sendMessage() {

    const message = chatInput.value.trim();

    if(message === "") return;

    // USER MESSAGE
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.innerText = message;

    chatBody.appendChild(userDiv);

    // BOT MESSAGE
    const botDiv = document.createElement("div");
    botDiv.className = "bot-message";
    let dots = 0;

    const typingAnimation = setInterval(() => {

    dots = (dots + 1) % 4;

    botDiv.innerText = "Typing" + ".".repeat(dots);

}, 500);

    chatBody.appendChild(botDiv);

    // SCROLL
    chatBody.scrollTo({
            top: chatBody.scrollHeight,
            behavior: "smooth"
        });

    // CLEAR INPUT
    chatInput.value = "";

    // FETCH REQUEST
    fetch("/chatbot/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },

        body: JSON.stringify({
            message: message
        })

    })

    .then(response => response.json())

    .then(data => {
        clearInterval(typingAnimation);
        botDiv.innerText = data.response;

        chatBody.scrollTo({
            top: chatBody.scrollHeight,
            behavior: "smooth"
        });

    })

    .catch(error => {

        console.error("Fetch Error:", error);

        botDiv.innerText = "Server error";

    });

}

// BUTTON CLICK
sendBtn.onclick = sendMessage;

// ENTER KEY
chatInput.addEventListener("keypress", function(event) {

    if(event.key === "Enter") {

        sendMessage();

    }

});

}