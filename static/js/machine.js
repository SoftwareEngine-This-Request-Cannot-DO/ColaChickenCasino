

var is_reel = false;
var magnificat = [1000,100,100,10,10,10,3,3,3];
document.addEventListener("DOMContentLoaded", function(event) {
    const betButton = document.getElementById("bet-button");
    let credits = 10000; //我的點數
    betButton.addEventListener("click", function() {
        console.log("數字是",winNumber);
        const betAmount = parseInt(document.getElementById("bet-input").value);
        if (betAmount > credits) {
            alert("餘額不足！");
        }
        else if(betAmount <= 100 || isNaN(betAmount)){
            alert("下注過少");
        }
        else {             
            rollAll();
            credits -= betAmount;
            document.getElementById("credits-display").textContent = credits ;
            document.getElementById("is_balance").textContent = betAmount;           
            if(winNumber != -1){
                credits += betAmount * magnificat[winNumber]
                document.getElementById("credits-display").textContent = credits;
                document.getElementById("jackpot").textContent = betAmount * magnificat[winNumber] //倍率看圖案
            } 
            console.log("中?水果",winNumber);     
        }
    });
});

/*
function is_spin(){
    document.getElementById("bet-button").disabled = true;
    
    // 兩秒後再次啟用按鈕
    setTimeout(function() {
        document.getElementById("bet-button").disabled = false;
    }, 4000);
}*/





