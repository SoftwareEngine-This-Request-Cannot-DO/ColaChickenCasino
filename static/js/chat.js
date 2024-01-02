const socket = io('http://localhost:5000');

socket.on('connect', function() {
    console.log('Connected to the server');
});

document.getElementById('send-button').addEventListener('click', function() {
    const message = document.getElementById('message-input').value;
    if (message) {
        socket.emit('send_message', { message: message });
        document.getElementById('message-input').value = '';
    }
});

//Enter發送
document.getElementById('message-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // 阻止 Enter 鍵的默認行為
        
        // 觸發發送消息
        const message = this.value;
        const user = document.getElementById('myName').innerHTML;
        if (message) {
            socket.emit('send_message', {
                message: message,
                user: user
            });
            this.value = ''; // 清空輸入框
        }
    }
});

socket.on('receive_message', function(data) {
    var chatContainer = document.getElementById('chat-container');
    var newMessageDiv = document.createElement('div');

    // 格式化消息內容
    newMessageDiv.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
    
    chatContainer.appendChild(newMessageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // 滾動到最新消息
});
