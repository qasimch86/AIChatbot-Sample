// ************************************************
// Now need to route the history UI from chatui.js. Verify variable is storing values for sql tables.
//

// Store chat histories
const chatHistories = {};

// Active chat ID
let activeChatId = null;
document.addEventListener("DOMContentLoaded", () => {
    const newChatIcon = document.querySelector(".add-new");
    const chatTabsList = document.getElementById("chat-tabs-list");
    // const renameTabsList = document.getElementById("chat-tabs-list");
    const chatList = document.getElementById("chat-list");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    // Add initial chat tab
    if (!newChatIcon) {
    addNewChatTab();
    }
    // Add new chat tab with creation time and default name
    function addNewChatTab() {
        const chatId = `chat-${Date.now()}`;
        const chatData = {
            id: chatId,
            name: "Untitled Chat",
            createTime: getCurrentTime(),
            unreadCount: 0
        };
                    chatHistories[chatId] = chatData;
            addChatTab(chatTabsList, chatData);
    }

    if (newChatIcon && chatTabsList) {
        newChatIcon.addEventListener("click", () => {
            const chatId = `chat-${Date.now()}`;
            const chatData = {
                id: chatId,
                name: "Untitled Chat",
                messages: [], // Message history for this chat
                time: getCurrentTime(),
                unreadCount: 0
            };

            chatHistories[chatId] = chatData;
            addChatTab(chatTabsList, chatData);
            switchChat(chatId); // Automatically switch to the new chat
        });
    }

    chatTabsList.addEventListener("click", (event) => {
        const chatTab = event.target.closest(".chat-tab");
        if (chatTab) {
            const chatId = chatTab.dataset.chatId;
            if (chatId) {
                switchChat(chatId);
            }
        }
        const chatNameElement = event.target.closest(".chat-name");
        if (chatNameElement) {
            enableRename(chatNameElement);
        }
    });

    sendButton.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (!message) return;

        const time = getCurrentTime();
        const userMessage = {
            sender: "You",
            text: message,
            time
        };

        // Add message to active chat's history
        if (activeChatId && chatHistories[activeChatId]) {
            chatHistories[activeChatId].messages.push(userMessage);
            // updateChatContainer(activeChatId);
            userInput.value = ""; // Clear the input box

            try {
                // Send the message to the backend and get AI response
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message }),
                });
                const data = await response.json();

                const aiMessage = {
                    sender: "AI Bot",
                    text: data.response_llm || "No response received.",
                    sqlResults: data.final_sql_results || " There was no output table.",
                    time: getCurrentTime()
                };

                // Add AI response to the active chat's history
                chatHistories[activeChatId].messages.push(aiMessage);
                // updateChatContainer(activeChatId); // Refresh UI with the AI response
            } catch (error) {
                console.error("Error communicating with the backend:", error);
            }
        }
    });
    function addChatTab(chatTabsList, chatData) {
        const newChatTabHTML = `
            <li class="p-2 border-bottom chat-tab" style="background-color: #eee;" data-chat-id="${chatData.id}">
              <a href="#!" class="d-flex justify-content-between">
                <div class="d-flex flex-row">
                  <div class="pt-1">
                    <p class="fw-bold mb-0 chat-name">${chatData.name}</p>
                    <p class="small text-muted chat-message">No messages yet.</p>
                  </div>
                </div>
                <div class="pt-1">
                  <p class="small text-muted mb-1 chat-time">${chatData.time}</p>
                  <span class="badge bg-danger float-end chat-unread-count">${chatData.unreadCount}</span>
                </div>
              </a>
            </li>
        `;

        chatTabsList.innerHTML += newChatTabHTML;
        console.log(`New chat tab added: ${chatData.name}`);
    }

    function switchChat(chatId) {
        if (!chatHistories[chatId]) return;

        activeChatId = chatId;
        updateChatContainer(chatId);

        // Highlight the active chat tab
        const allTabs = document.querySelectorAll(".chat-tab");
        allTabs.forEach(tab => {
            tab.style.backgroundColor = tab.dataset.chatId === chatId ? "#d3f2f8" : "#eee";
        });
    }

    function updateChatContainer(chatId) {
        const chatHistory = chatHistories[chatId];
        if (!chatHistory) return;

        // Update the chat list with the messages
        chatList.innerHTML = chatHistory.messages
            .map(
                (msg) => `
                <li class="d-flex justify-content-between mb-4 ${msg.sender === "You" ? "user-message" : "bot-message"}">
                  <div class="card">
                    <div class="card-header d-flex justify-content-between p-3">
                      <p class="fw-bold mb-0">${msg.sender}</p>
                      <p class="text-muted small mb-0">${msg.time}</p>
                    </div>
                    <div class="card-body">
                      <p class="mb-0">${msg.text}</p>
                    </div>
                  </div>
                </li>`
            )
            .join("");

        // Clear the unread count for this chat
        const chatTab = document.querySelector(`[data-chat-id="${chatId}"]`);
        if (chatTab) {
            const unreadCountBadge = chatTab.querySelector(".chat-unread-count");
            if (unreadCountBadge) unreadCountBadge.textContent = "";
        }

        console.log(`Switched to chat: ${chatId}`);
    }

    function enableRename(chatNameElement) {
        const currentName = chatNameElement.textContent;
        const parent = chatNameElement.parentNode;
    
        // Create an input field with the current name
        const input = document.createElement("input");
        input.type = "text";
        input.value = currentName;
        input.className = "rename-input form-control";
        input.style.maxWidth = "200px";
    
        // Replace the <p> element with the input
        parent.replaceChild(input, chatNameElement);
    
        // Focus the input and select its contents
        input.focus();
        input.select();
    
        // Handle renaming when the input loses focus or Enter key is pressed
        input.addEventListener("blur", () => saveNewName(input, parent));
        input.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                saveNewName(input, parent);
            }
        });
    }
    
    function saveNewName(input, parent) {
        const newName = input.value.trim() || "Untitled Chat"; // Default to "Untitled Chat" if empty
    
        // Create a new <p> element with the updated name
        const chatNameElement = document.createElement("p");
        chatNameElement.textContent = newName;
        chatNameElement.className = "fw-bold mb-0 chat-name";
    
        // Replace the input with the <p> element
        parent.replaceChild(chatNameElement, input);
    
        console.log(`Chat renamed to: ${newName}`);
    }

    function getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    }
});
