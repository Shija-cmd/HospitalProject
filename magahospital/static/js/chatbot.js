function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

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


/* AUTO POPUP */
window.addEventListener("load", () => {

    if (!sessionStorage.getItem("chatbotShown")) {

        setTimeout(() => {

            if (chatBox) {

                chatBox.style.display = "flex";

                sessionStorage.setItem(
                    "chatbotShown",
                    "true"
                );

            }

        }, 3000);

    }

});


/* TOGGLE CHAT */
if (chatToggle && chatBox) {

    chatToggle.addEventListener("click", () => {

        if (chatBox.style.display === "flex") {

            chatBox.style.display = "none";

        } else {

            chatBox.style.display = "flex";

        }

    });

}


/* CLOSE CHAT */
if (closeChat && chatBox) {

    closeChat.addEventListener("click", () => {

        chatBox.style.display = "none";

    });

}


/* SEND MESSAGE */
if (sendBtn && chatInput && chatBody) {

    async function sendMessage() {

        const message = chatInput.value.trim();

        if (!message) return;


        /* USER MESSAGE */
        const userDiv = document.createElement("div");

        userDiv.className = "user-message";

        userDiv.innerText = message;

        chatBody.appendChild(userDiv);


        /* BOT MESSAGE */
        const botDiv = document.createElement("div");

        botDiv.className = "bot-message";

        botDiv.innerText = "Typing...";

        chatBody.appendChild(botDiv);


        /* SCROLL */
        chatBody.scrollTop = chatBody.scrollHeight;


        /* CLEAR INPUT */
        chatInput.value = "";


        try {

            const response = await fetch("/chatbot/", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json",

                    "X-CSRFToken": getCookie("csrftoken")

                },

                body: JSON.stringify({

                    message: message

                })

            });


            if (!response.ok) {

                throw new Error(
                    "Server returned status " + response.status
                );

            }


            const data = await response.json();

            console.log("CHATBOT RESPONSE:", data);

            botDiv.innerText = data.response;

        }

        catch (error) {

            console.error("FETCH ERROR:", error);

            botDiv.innerText =
                "Sorry, server error occurred.";

        }


        chatBody.scrollTop = chatBody.scrollHeight;

    }


    /* BUTTON CLICK */
    sendBtn.addEventListener("click", sendMessage);


    /* ENTER KEY */
    chatInput.addEventListener("keypress", function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();

        }

    });

}