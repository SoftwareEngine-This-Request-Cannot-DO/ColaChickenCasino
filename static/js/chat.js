const socket = io('http://localhost:5000');

socket.on('connect', function() {
    console.log('Connected to the server');
});

document.getElementById('send-button').addEventListener('click', function() {
    const message = document.getElementById('message-input').value;
    const user = document.getElementById('myName').innerHTML;
    if (message) {
        socket.emit('send_message', {
            message: message,
            user: user
        });
        document.getElementById('message-input').value = '';
    }
});

//Enter 發送
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
                return; // 如果還沒到 3 秒，則不執行任何操作
            }

            canChangeStatus = false; // 設置狀態切換標誌為 false
            setTimeout(() => {
                canChangeStatus = true; // 3秒後將標誌重置為 true
            }, 3000); // 3秒的計時器

            const isOnline = this.classList.contains('online');
            const user = document.getElementById('myName').innerHTML;
            const newStatus = isOnline ? 'offline' : 'online';
            this.classList.toggle('online', newStatus === 'online');
            this.classList.toggle('offline', newStatus === 'offline');

            socket.emit('change_status', { status: newStatus, user: user });
            console.log("OK")
        });
    });
});
function setupStatusIndicatorListeners() {
    document.querySelectorAll('.status-indicator').forEach(indicator => {
        indicator.addEventListener('click', function() {
            const user = document.getElementById('myName').innerHTML;
            const isOnline = this.classList.contains('online');
            const newStatus = isOnline ? 'offline' : 'online';
            socket.emit('change_status', { status: newStatus, user: user });
        });
    });
}


// document.addEventListener('DOMContentLoaded', function() {
//     setupStatusIndicatorListeners();
// });

const friends_list = document.getElementById("friends_list");
function getFriendsData() {
    fetch('/getFriends')
        .then(response => response.json())
        .then(data => {
            console.log('Data from Flask:', data);
            if(data.friends.length > 0){
                for(let f of data.friends){
                    const friend = document.createElement('li');
                    friend.innerHTML = f;
                    friends_list.appendChild(friend);
                }
                return;
            }
            const friend = document.createElement('li');
            friend.innerHTML = "你目前沒有朋友";
            friends_list.appendChild(friend);
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching data from Flask');
        });
}


function getAllUserData() {
    fetch('/getAllUser')
        .then(response => response.json())
        .then(data => {
            console.log('Data from Flask:', data);
            if(data.users.length > 0){
                friends_list.innerHTML = "";
                for(let f of data.users){
                    const friend = document.createElement('li');
                    friend.setAttribute('class', 'user_item')
                    friend.innerHTML = f;
                    friend.addEventListener('click', () => {
                        fetch('/addFriends', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({'username': friend.innerHTML}),
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log('Response from Flask:', data);
                            friends_list.innerHTML = ""
                            if(data.friends.length > 0){
                                for(let f of data.friends){
                                    const friend = document.createElement('li');
                                    friend.innerHTML = f;
                                    friends_list.appendChild(friend);
                                }
                                return;
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                            alert('Error sending data to Flask');
                        });
                    })
                    friends_list.appendChild(friend);
                }
                return;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error fetching data from Flask');
        });
}

document.getElementById('addFriends').addEventListener('click', () => {
    getAllUserData();
});
getFriendsData();