document.addEventListener('DOMContentLoaded', function () {
    const idInput = document.getElementById('id-input');
    const checkBtn = document.getElementById('check-id-btn');
    const idValid = document.getElementById('id-valid');
    const password = document.getElementById('password');
    const passwordCheck = document.getElementById('password-check');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const terms = document.getElementById('terms');
    const signupBtn = document.getElementById('signup-btn');

    const msgBox = document.getElementById('check-id-msg');
    const form = document.querySelector('form');

    // ✅ AJAX 아이디 중복 확인
    checkBtn.addEventListener('click', function () {
        const idValue = idInput.value.trim();
        fetch('/check_id', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: 'id=' + encodeURIComponent(idValue)
        })
            .then(res => res.json())
            .then(data => {
                msgBox.textContent = data.message;
                msgBox.style.color = data.result ? '#16a34a' : '#dc2626';
                idValid.value = data.result ? 'true' : 'false';
                checkAllValid();  // 상태 업데이트
            });
    });

    // ✅ 유효성 검사 함수
    function checkAllValid() {
        const idOk = idValid.value === 'true';

        const pwNotEmpty = password.value.trim() !== '' && passwordCheck.value.trim() !== '';
        const pwMatch = password.value === passwordCheck.value;
        const pwOk = pwNotEmpty && pwMatch;

        const nameOk = nameInput.value.trim() !== '';
        const emailOk = emailInput.value.trim() !== '';
        const termsOk = terms.checked;

        const isValid = idOk && pwOk && nameOk && emailOk && termsOk;
        signupBtn.disabled = !isValid;
    }

    // ✅ 모든 입력 요소에 이벤트 연결
    [password, passwordCheck, nameInput, emailInput, terms].forEach(el => {
        el.addEventListener('input', checkAllValid);
        el.addEventListener('change', checkAllValid);
    });

    // ✅ 아이디 수정 시 중복 확인 다시 필요
    idInput.addEventListener('input', () => {
        idValid.value = 'false';
        msgBox.textContent = '';
        checkAllValid();
    });

    // ✅ 초기 상태 체크
    checkAllValid();
});
