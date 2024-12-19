// Function to simulate sending a message and getting a response
function sendMessage() {
    const userInput = document.getElementById('user-input').value.trim();
    if (userInput === '') return;

    // Add user message to chat history
    const chatHistory = document.getElementById('chat-history');
    const userMessage = document.createElement('div');
    userMessage.classList.add('message', 'user-message');
    userMessage.textContent = userInput;
    chatHistory.appendChild(userMessage);

    // Clear input field
    document.getElementById('user-input').value = '';

    // Simulate bot response after a short delay
    setTimeout(() => {
        const botResponse = document.createElement('div');
        botResponse.classList.add('message', 'bot-message');
        botResponse.textContent = "This is the bot's response to: " + userInput;
        chatHistory.appendChild(botResponse);

        // Scroll to the bottom of the chat history
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }, 1000);
}

// Function to toggle login panel (simplified for demonstration)
function toggleLogin() {
    alert('Login functionality can be implemented here.');
}
