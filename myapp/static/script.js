function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    if (!username || !password) {
        alert('모든 필드를 입력하세요.');
        return;
    }

    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/people';
        } else {
            alert('로그인 실패');
        }
    })
    .catch(error => {
        console.error('로그인 오류:', error);
        alert('로그인 중 오류가 발생했습니다.');
    });
}