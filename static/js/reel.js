//中獎設定
var probabilityArr = [0.5,1.5,1.5,8,8,8,10,10,10];
function setProbability(){
  var randomNum = Math.random();
  for(var i=0;i<9;i++){
    if(probabilityArr[i] > randomNum * 100){
      if(i == 0)
        return 0;
      else if(i == 1){
        randomNum = Math.random();
        return Math.floor(randomNum * 2) + 1;
      }
      else if(i == 3){
        randomNum = Math.random();
        return Math.floor(randomNum * 3) + 3;
      }
      else if(i == 6){
        randomNum = Math.random();
        return Math.floor(randomNum * 3) + 6;
      }
    }
  }
  return -1;
}

const debugEl = document.getElementById('debug'),
  iconMap = ["banana", "seven", "cherry", "plum", "orange", "bell", "bar", "lemon", "melon"];
  let tolProbabilty = 1;
  const random_number = Math.random() ;
  let probability = [];
  let money = [];
  icon_width = 79,
  icon_height = 79,
  num_icons = 9,
  time_per_icon = 100,
  indexes = [0, 0, 0];


var resetPos = [0,0,0], failNumber = -1,notWin,winNumber = -1;
var count = -1,closeProbablity = true;
const roll = (reel, offset = 0) => {
  count++;
  if(count % 3 == 0){ 
    winNumber = setProbability();
    if(winNumber != -1){
      closeProbablity = true;
      console.log("中獎",winNumber);
    }
    else{
      closeProbablity = false;
    }
  }
  if(closeProbablity){
    failNumber = 0;
    resetPos[count % 3 ] %= 9;
    if(resetPos[count % 3] > winNumber){
      cycle = 9 - (resetPos[count % 3] - winNumber); 
    }
    else{
      cycle = winNumber - resetPos[count % 3];
    }
    resetPos[count % 3] = winNumber; //復位
  }
  else{
    cycle = 0;
    failNumber = Math.round(Math.random() * num_icons); 
    resetPos[count % 3] += failNumber;
    notWin = resetPos[0] % 9; //確保不會中獎
    if(count % 3 == 2 && resetPos[2] == notWin){ 
      if ((notWin + 1) == 9){  
        failNumber -= 2;  
        resetPos[count % 3] -= 2;
      }
      else{
        failNumber += 1;  
        resetPos[count % 3] += 1;
      }
    }
  }

  const delta =  ((offset + 2) * num_icons) + failNumber + cycle;
  console.log("delta",delta);

  return new Promise((resolve, reject) => {
    const style = getComputedStyle(reel),
      backgroundPositionY = parseFloat(style["background-position-y"]),
      targetBackgroundPositionY = backgroundPositionY + delta * icon_height,
      normTargetBackgroundPositionY = targetBackgroundPositionY % (num_icons * icon_height);

  setTimeout(() => {
      reel.style.transition = `background-position-y ${(8 + 1 * delta) * time_per_icon}ms cubic-bezier(.41,-0.01,.63,1.09)`;

      reel.style.backgroundPositionY = `${backgroundPositionY + delta * icon_height}px`;
    }, offset * 150);

    setTimeout(() => {
      reel.style.transition = `none`;
      reel.style.backgroundPositionY = `${normTargetBackgroundPositionY}px`;
      resolve(delta % num_icons);
    }, (8 + 1 * delta) * time_per_icon + offset * 150);  
  });
};


let winCls = "";
function rollAll() {
  debugEl.textContent = 'rolling...';
  const reelsList = document.querySelectorAll('.slots > .reel');
  Promise
  .all([...reelsList].map((reel, i) => roll(reel, i)))

  .then(deltas => {
    deltas.forEach((delta, i) => indexes[i] = (indexes[i] + delta) % num_icons);
    debugEl.textContent = indexes.map(i => iconMap[i]).join(' - ');
    if (indexes[0] == indexes[1] && indexes[1] == indexes[2]) {
      winCls = "win2" ;
      document.querySelector(".slots").classList.add(winCls);
      setTimeout(() => document.querySelector(".slots").classList.remove(winCls), 2000);
    }
  });
}
;
setTimeout(rollAll, 500);







