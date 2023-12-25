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

socket.on('receive_message', function(data) {
    var chatContainer = document.getElementById('chat-container');
    var newMessageDiv = document.createElement('div');
    newMessageDiv.textContent = data.message;
    chatContainer.appendChild(newMessageDiv);
});