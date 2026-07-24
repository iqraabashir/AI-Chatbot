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
    <div class="avatar">
        👤
    </div>
    <div class="user-bubble">
        ${message}
        <div class="time">
            ${new Date().toLocaleTimeString()}
        </div>
    </div>
`;
    chatBox.appendChild(userDiv);
    input.value = "";

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
        🤖
    </div>
    <div class="bot-bubble">
        ${data.response.replace(/\n/g, "<br>")}
        <div class="time">
            ${new Date().toLocaleTimeString()}
        </div>
    </div>
`;
    chatBox.appendChild(botDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
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
.addEventListener("click",()=>{

    document.body.classList.toggle("dark");
});
