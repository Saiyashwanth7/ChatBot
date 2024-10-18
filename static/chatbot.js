// Attach event listeners for input and button
document.getElementById("message-input").addEventListener("keydown", function(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // Prevent newline on Enter key
        sendMessage();
    }
});

document.getElementById("send-btn").addEventListener("click", sendMessage);

// Function to send the user's message to the server
function sendMessage() {
    const messageInput = document.getElementById("message-input");
    const userMessage = messageInput.value.trim();

    if (userMessage !== "") {
        // Add user's message to the chat
        addMessage(userMessage, "user-message");
        messageInput.value = ""; // Clear the input field

        // Send the user message to the Flask backend
        fetch('/api', {  // Update the endpoint to match your Flask API route
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Ensure the data contains the expected response structure
            if (data.response) {
                addMessage(data.response, "bot-message");
            } else {
                addMessage("Sorry, I encountered an error. Please try again.", "bot-message");
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage("Sorry, I encountered an error. Please try again.", "bot-message");
        });
    }
}

// Function to add a message to the chat box
function addMessage(content, className) {
    const chatBox = document.querySelector(".chat-box");
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", className);
    messageDiv.innerHTML = content;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}
