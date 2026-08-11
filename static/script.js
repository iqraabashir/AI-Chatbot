async function sendMessage()
{
    let input = document.getElementById("user-input");
    let message = input.value.trim();
    if(message === "")
        return;
    let chatBox = document.getElementById("chat-box");
    let userDiv = document.createElement("div");
    userDiv.className = "user-row";
    userDiv.innerHTML = `
        <div class="user-message-wrapper">
            <div class="sender-name user-name">
                You
            </div>
            <div class="user-bubble">
                ${message}
                <div class="time">
                    ${new Date().toLocaleTimeString()}
                </div>
            </div>
        </div>
        <div class="user-avatar">
            <i class="bi bi-person-fill"></i>
        </div>
    `;

    chatBox.appendChild(userDiv);
    input.value = "";
    chatBox.scrollTo({
    top: chatBox.scrollHeight,
    behavior: "smooth"
});

    const response = await fetch("/get_response", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    });

    const data = await response.json();
    let botDiv = document.createElement("div");
    botDiv.className = "bot-row";
    botDiv.innerHTML = `
        <div class="avatar">
            <i class="bi bi-robot"></i>
        </div>

        <div class="message-wrapper">
            <div class="sender-name">
                CUS AI Assistant
            </div>

            <div class="bot-bubble">
                ${data.response.replace(/\n/g, "<br>")}
                <div class="time">
                    ${new Date().toLocaleTimeString()}
                </div>
            </div>
        </div>
    `;

    chatBox.appendChild(botDiv);
    chatBox.scrollTo({
    top: chatBox.scrollHeight,
    behavior: "smooth"
});
}
document.getElementById("user-input")
.addEventListener("keypress", function(event){
    if(event.key === "Enter"){
        sendMessage();
    }
});
function quickQuestion(text)
{
    document.getElementById("user-input").value = text;
    sendMessage();
}
document
.getElementById("theme-btn")
.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const icon =
        document.querySelector("#theme-btn i");
    if (document.body.classList.contains("dark")) {
        icon.className = "bi bi-sun-fill";
    } else {
        icon.className = "bi bi-moon-stars-fill";
    }
});
