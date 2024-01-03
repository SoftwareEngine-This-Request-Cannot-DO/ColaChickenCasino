var is_reel = false;
var magnificat = [1000,100,100,10,10,10,3,3,3];
document.addEventListener("DOMContentLoaded", function(event) {
    const betButton = document.getElementById("bet-button");
    betButton.addEventListener("click", async function() {
        console.log("數字是",winNumber);
        const betAmount = parseInt(document.getElementById("bet-input").value);
        let credits = parseInt(document.getElementById("credits-display").innerHTML); //我的點數
        if (betAmount > credits) {
            alert("餘額不足！");
        }
        else if(betAmount <= 100 || isNaN(betAmount)){
            alert("下注過少");
        }
        else {
            document.getElementById("is_balance").textContent = betAmount; 
            document.getElementById("jackpot").textContent = "--"             
            await rollAll(); // 等待 rollAll 跑完
            credits -= betAmount;          
            if(winNumber != -1){
                credits += betAmount * magnificat[winNumber]
                document.getElementById("jackpot").textContent = betAmount * magnificat[winNumber] //倍率看圖案
            }
            console.log("中?水果",winNumber);
            handleData();
        }
    });
});

// 傳送資料至 flask 後端進行資料更新
const handleData = () => {
    const credits = document.getElementById('credits-display').innerHTML;
    const pay = document.getElementById('bet-input').value;
    const result = document.getElementById('jackpot').innerHTML;
    if(parseInt(credits) === NaN || parseInt(pay) === NaN) return;
    const requestOptions = {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        "current": credits,
        "pay": pay,
        "result": result,
        })
    }
    fetch('http://127.0.0.1:5000/slotrun', requestOptions)
        .then(response => {
            if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            document.getElementById('myChips').querySelector(".number").innerText = data.chips;
            document.getElementById("credits-display").textContent = data.chips;
            document.getElementById("play-times-reel").innerHTML = data.gameT;
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
}

/*
function is_spin(){
    document.getElementById("bet-button").disabled = true;
    
    // 兩秒後再次啟用按鈕
    setTimeout(function() {
        document.getElementById("bet-button").disabled = false;
    }, 4000);
}*/





