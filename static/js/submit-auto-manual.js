let enterEnabled = true; // Default: Enter submits message

    // Handle Enter key behavior
    document.getElementById("user-input").addEventListener("keydown", function(event) {
      if (enterEnabled && event.key === "Enter") {
        event.preventDefault(); // Prevent adding new line
        document.getElementById("send-button").click(); // Trigger Send button click
      }
    });

    // Handle checkbox toggle
    document.getElementById("enter-toggle").addEventListener("change", function() {
      enterEnabled = this.checked; // Enable/Disable Enter key to submit based on checkbox
      if (enterEnabled) {
        alert("Enter to submit is enabled.");
      } else {
        alert("Enter to submit is disabled. You must click the send button.");
      }
    });