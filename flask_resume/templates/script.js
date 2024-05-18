// Sending request to Python server
const formsubmitted = async () => {
    // Get user input
    let userinput = document.getElementById('userinput').value;

    // Disable input and send button while waiting for response
    let sendbtn = document.getElementById('sendbtn');
    let userinputarea = document.getElementById('userinput');
    sendbtn.disabled = true;
    userinputarea.disabled = true;

    // Update UI to show user message
    appendUserMessage(userinput);

    try {
        // Send POST request to Flask server
        const response = await fetch("http://127.0.0.1:5000/search", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userinput }) // Send user input as JSON
        });

        // Parse JSON response
        const responseData = await response.json();

        // Extract unique sources from response
        const uniqueSources = responseData.unique_sources;

        // Update UI to show unique sources
        appendAppMessage(uniqueSources.join(', '));
    } catch (error) {
        console.error('Error:', error);
        // Update UI to show error message
        appendAppMessage('An error occurred while processing your request.');
    }

    // Enable input and send button
    sendbtn.disabled = false;
    userinputarea.disabled = false;
};

// Function to append user message to UI
function appendUserMessage(message) {
    let upperdiv = document.getElementById('upperid');
    upperdiv.innerHTML += `
        <div class="message">
            <div class="usermessagediv">
                <div class="usermessage">${message}</div>
            </div>
        </div>`;
    scrollToBottom();
}

// Function to append app message to UI
function appendAppMessage(message) {
    let upperdiv = document.getElementById('upperid');
    upperdiv.innerHTML += `
        <div class="message">
            <div class="appmessagediv">
                <div class="appmessage">${message}</div>
            </div>
        </div>`;
    scrollToBottom();
}

// Function to scroll to bottom of messages
function scrollToBottom() {
    let div = document.getElementById("upperid");
    div.scrollTop = div.scrollHeight;
}
