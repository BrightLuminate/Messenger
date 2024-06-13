function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // 올바른 인증 정보
    var correctUsername = "불독";
    var correctPassword = "1234";
    var correctUsername = "골든 리트리버";
    var correctPassword = "1234";
    var correctUsername = "래브라도 리트리버";
    var correctPassword = "1234";
    var correctUsername = "푸들";
    var correctPassword = "1234";
    var correctUsername = "시베리안 허스키";
    var correctPassword = "1234";
    var correctUsername = "치와와";
    var correctPassword = "1234";
    var correctUsername = "보더 콜리";
    var correctPassword = "1234";
    var correctUsername = "도베르만 핀셔";
    var correctPassword = "1234";
    var correctUsername = "말티즈";
    var correctPassword = "1234";
    var correctUsername = "요크셔 테리어";
    var correctPassword = "1234";
    var correctUsername = "보스턴 테리어";
    var correctPassword = "1234";
    var correctUsername = "프렌치 불도그";
    var correctPassword = "1234";
    var correctUsername = "저먼 셰퍼드";
    var correctPassword = "1234";
    var correctUsername = "퍼그";
    var correctPassword = "1234";
    var correctUsername = "시추";
    var correctPassword = "1234";
    var correctUsername = "사모예드";
    var correctPassword = "1234";
   

    // 인증 정보 확인
    if(username === correctUsername && password === correctPassword) {
        // 프로젝트 페이지로 리디렉션
        window.location.href = "people";
    } else {
        alert("잘못된 인증 정보");
    }
}

function logout() {
    // 로그인 컨테이너 표시
    document.getElementById('login-container').style.display = 'block';
    // 로그아웃 컨테이너 숨김
    document.getElementById('logout-container').style.display = 'none';
    // 입력 필드 지우기
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}