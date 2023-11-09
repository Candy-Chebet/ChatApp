// scrollToBottom.js
export default function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}
