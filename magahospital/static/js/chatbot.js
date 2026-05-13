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


/* ELEMENTS */
const chatToggle = document.getElementById("chat-toggle");
const chatBox = document.getElementById("chat-box");
const closeChat = document.getElementById("close-chat");

const sendBtn = document.getElementById("send-btn");
const chatInput = document.getElementById("chat-input");
const chatBody = document.getElementById("chat-body");


/* AUTO POPUP AFTER 3 SECONDS */
window.addEventListener("load", () => {

    if (!sessionStorage.getItem("chatbotShown")) {

        setTimeout(() => {

            if (chatBox) {

                chatBox.style.display = "flex";

                sessionStorage.setItem("chatbotShown", "true");

            }

        }, 3000);

    }

});


/* TOGGLE CHAT */
if (chatToggle && chatBox) {

    chatToggle.onclick = () => {

        if (chatBox.style.display === "flex") {

            chatBox.style.display = "none";

        } else {

            chatBox.style.display = "flex";

        }

    };

}


/* CLOSE CHAT */
if (closeChat && chatBox) {

    closeChat.onclick = () => {

        chatBox.style.display = "none";

    };

}


/* SEND MESSAGE FUNCTION */
if (sendBtn && chatInput && chatBody) {

    function sendMessage() {

        const message = chatInput.value.trim();

        if (message === "") return;


        /* USER MESSAGE */
        const userDiv = document.createElement("div");

        userDiv.className = "user-message";

        userDiv.innerText = message;

        chatBody.appendChild(userDiv);


        /* BOT MESSAGE */
        const botDiv = document.createElement("div");

        botDiv.className = "bot-message";

        botDiv.innerText = "Typing";

        chatBody.appendChild(botDiv);


        /* TYPING ANIMATION */
        let dots = 0;

        const typingAnimation = setInterval(() => {

            dots = (dots + 1) % 4;

            botDiv.innerText = "Typing" + ".".repeat(dots);

        }, 500);


        /* SCROLL */
        chatBody.scrollTo({

            top: chatBody.scrollHeight,

            behavior: "smooth"

        });


        /* CLEAR INPUT */
        chatInput.value = "";


        /* FETCH REQUEST */
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

        .then(response => {

            if (!response.ok) {

                throw new Error("HTTP Error: " + response.status);

            }

            return response.json();

        })

        .then(data => {

            clearInterval(typingAnimation);

            botDiv.innerText = data.response || "No response from server.";

            chatBody.scrollTo({

                top: chatBody.scrollHeight,

                behavior: "smooth"

            });

        })

        .catch(error => {

            clearInterval(typingAnimation);

            console.error("Fetch Error:", error);

            botDiv.innerText = "Sorry, server error occurred.";

            chatBody.scrollTo({

                top: chatBody.scrollHeight,

                behavior: "smooth"

            });

        });

    }


    /* BUTTON CLICK */
    sendBtn.onclick = sendMessage;


    /* ENTER KEY */
    chatInput.addEventListener("keypress", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    });

}