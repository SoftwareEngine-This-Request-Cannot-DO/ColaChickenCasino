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

    // 如果是系統消息，使用不同的樣式
    if (data.username === '系統') {
        newMessageDiv.innerHTML = `<em>${data.message}</em>`;
    } else {
        // 普通消息
        newMessageDiv.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
    }
    
    chatContainer.appendChild(newMessageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight; // 滾動到最新消息
});

socket.on('status_updated', function(data) {
    const userElements = document.querySelectorAll('.user .username');
    userElements.forEach(elem => {
        if (elem.textContent === data.user) {
            const statusIndicator = elem.previousElementSibling;
            statusIndicator.className = 'status-indicator ' + (data.status === 'online' ? 'online' : 'offline');
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    let canChangeStatus = true; // 用來控制狀態切換的標誌

    document.querySelectorAll('.status-indicator').forEach(indicator => {
        indicator.addEventListener('click', function() {
            if (!canChangeStatus) {
                console.log("You can only change status every 3 seconds.");
                return; // 如果還沒到3秒，則不執行任何操作
            }

            canChangeStatus = false; // 設置狀態切換標誌為 false
            setTimeout(() => {
                canChangeStatus = true; // 3秒後將標誌重置為 true
            }, 3000); // 3秒的計時器

            const isOnline = this.classList.contains('online');
            const newStatus = isOnline ? 'offline' : 'online';
            this.classList.toggle('online', newStatus === 'online');
            this.classList.toggle('offline', newStatus === 'offline');

            socket.emit('change_status', { status: newStatus });
        });
    });
});
function setupStatusIndicatorListeners() {
    document.querySelectorAll('.status-indicator').forEach(indicator => {
        indicator.addEventListener('click', function() {
            const isOnline = this.classList.contains('online');
            const newStatus = isOnline ? 'offline' : 'online';
            socket.emit('change_status', { status: newStatus });
        });
    });
}


document.addEventListener('DOMContentLoaded', function() {
    setupStatusIndicatorListeners();
});
