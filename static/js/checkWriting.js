//글쓰기 페이지의 유효성 검사

function checkWriting(){
    var form = document.writeForm       // 폼 선택
    var title = form.title.value        // 입력받은 제목값
    var content = form.content.value  // 입력받은 글내용값

    //만약 제목이 안 써있다면
    if(title == ""){
        alert ("제목은 필수 입력 항목입니다.");     //팝업창띄우기
        form.title.focus();     //화살표 보내기
        return false;
    }
    else if(content == ""){
        alert ("글 내용은 필수 입력 항목입니다.")
        form.content.focus();
        return false;
    }
    else{
        form.submit();  //폼 전송
    }
}

