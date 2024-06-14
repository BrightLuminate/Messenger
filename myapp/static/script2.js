document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signup-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const username = document.getElementById('new-username').value.trim();
        const password = document.getElementById('new-password').value.trim();
        const confirmPassword = document.getElementById('confirm-password').value.trim();
        const email = document.getElementById('email').value.trim();

        if (!username || !password || !confirmPassword || !email) {
            alert('모든 필드를 입력하세요.');
            return;
        }

        if (password !== confirmPassword) {
            alert('비밀번호가 일치하지 않습니다.');
            return;
        }

        const formData = new URLSearchParams();
        formData.append('new_username', username);
        formData.append('new_password', password);
        formData.append('confirm_password', confirmPassword);
        formData.append('email', email);

        console.log('회원가입 요청을 보냅니다...');

        fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log('회원가입 응답:', data);
            alert('회원가입이 완료되었습니다.');
        })
        .catch(error => {
            console.error('회원가입 오류:', error);
            alert('회원가입 중 오류가 발생했습니다.');
        });
    });
});