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
            document.getElementById("jackpot").textContent = "--"             
            await rollAll();
            credits -= betAmount;
            document.getElementById("credits-display").textContent = credits ;
            document.getElementById("is_balance").textContent = betAmount;           
            if(winNumber != -1){
                credits += betAmount * magnificat[winNumber]
                document.getElementById("jackpot").textContent = betAmount * magnificat[winNumber] //倍率看圖案
            }
            console.log("中?水果",winNumber);
            handleData();
        }
    });
});

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
            document.getElementById('myChips').innerText = "你的籌碼：" + data.chips;
            document.getElementById("credits-display").textContent = data.chips;
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





