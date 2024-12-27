document.getElementById("send-button").addEventListener("click", sendMessage);

async function sendMessage() {
  const userInput = document.getElementById("user-input").value.trim();
  const chatList = document.getElementById("chat-list");

  if (!userInput) {
    alert("Please type a message.");
    return;
  }

  // Add user message to the chat UI
  const userMessage = `
    <li class="d-flex justify-content-between mb-4 user-message">
      <div class="card">
        <div class="card-header d-flex justify-content-between p-3" style="background-color: #f7f6f6;">
          <p class="fw-bold mb-0">You</p>
          <p class="text-muted small mb-0"><i class="far fa-clock"></i> just now</p>
        </div>
        <div class="card-body">
          <p class="mb-0">${userInput}</p>
        </div>
      </div>
    </li>`;
  chatList.innerHTML += userMessage;
  try {
    // Send user input to the backend
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userInput }),
    });
    const data = await response.json();
    console.log(data)
    // Add bot response to the chat UI
    const botMessage = `
      <li class="d-flex justify-content-between mb-4 bot-message">
        <div class="card">
          <div class="card-header d-flex justify-content-between p-3" style="background-color:rgb(74, 255, 213);">
            <p class="fw-bold mb-0">AI Bot</p>
            <p class="text-muted small mb-0"><i class="far fa-clock"></i> just now</p>
          </div>
          <div class="card-body">
            <p class="mb-0">${data.response_llm}</p>
          </div>
        </div>
      </li>`;
    chatList.innerHTML += botMessage;

    // Render the table if results are available
    const sqlResults = data.sql_results;
    if (sqlResults && sqlResults.length > 0) {
      const tableHTML = generateTableHTML(sqlResults);
      chatList.innerHTML += tableHTML;
    }
  } catch (error) {
    console.error("Error communicating with backend:", error);
    const errorMessage = `
      <li class="d-flex justify-content-between mb-4 bot-message">
        <div class="card">
          <div class="card-header d-flex justify-content-between p-3" style="color: rgb(255, 255, 255); background-color:rgb(196, 0, 0);">
            <p class="fw-bold mb-0">Error</p>
            <p class="small mb-0"><i class=""></i> just now</p>
          </div>
          <div class="card-body">
            <p class="mb-0">Failed to get a response. Please try again later.</p>
          </div>
        </div>
      </li>`;
    chatList.innerHTML += errorMessage;
  }

  // Scroll to the latest message
  chatList.scrollTop = chatList.scrollHeight;

  // Clear the input field
  document.getElementById("user-input").value = "";
}
// Function to generate table HTML dynamically
function generateTableHTML(results) {
  let tableHTML = `<div class="mt-4">
                    <h3>SQL Results:</h3>
                      <div class="table-responsive">
                        <table class="table table-bordered">
                          <thead>
                              <tr>`;
  // Headers
  results[0].forEach(header => {
    tableHTML += `<th>${header}</th>`;
  });
  tableHTML += `</tr></thead><tbody>`;

  // Rows
  for (let i = 1; i < results.length; i++) {
    tableHTML += `<tr>`;
    results[i].forEach(value => {
      tableHTML += `<td>${value}</td>`;
    });
    tableHTML += `</tr>`;
  }

  tableHTML += `</tbody></table></div></div>`;
  return tableHTML;
}