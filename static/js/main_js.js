// 마우스 이벤트 효과

var pic = document.getElementById('pic')

pic.onmouseover = changePic; // 함수 호출
pic.onmouseout = originPic;

function changePic(){
    pic.src = "../static/images/healing.jpg";
}
function originPic(){
    pic.src ="../static/images/activity.jpg";
}