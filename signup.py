import time
import random
import string
import logging

def get_random_low_english(length=15):
	return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def get_random_keyword():
	keywords = ["테스트", "자동화", "플레이라이트", "퇴근", "출근", "휴가", "반차", "시차", "연차", "월차"]
	return random.choice(keywords)


def move_to_signup_page(page):
	page.get_by_role("link", name="회원가입").click()


def set_user_id(page):
	while True:  # 중복되지 않는 ID가 생성될 때까지 반복
		user_id = get_random_low_english(5)
		page.get_by_role("textbox", name="아이디").fill(user_id)
		time.sleep(0.3)
		page.get_by_role("button", name="중복 확인").click()
		time.sleep(0.5)  # 결과 메시지가 표시될 시간을 기다림

		# 중복 여부 확인
		if not page.get_by_text("이미 존재하는 아이디입니다").is_visible():
			break  # 중복 메시지가 보이지 않으면 루프 종료

	return user_id

def set_user_password(page):
	password = "qwer1234!@#$"
	page.get_by_role("textbox", name="비밀번호", exact=True).fill(password)
	time.sleep(0.3)
	page.get_by_role("textbox", name="비밀번호 확인", exact=True).fill(password)
	time.sleep(0.3)

def set_user_name(page):
	user_name = get_random_keyword()
	page.get_by_role("textbox", name="이름").fill(user_name)
	time.sleep(0.3)

def set_user_email(page):
	user_email = "test" + get_random_low_english(5) + "@test1234.co.kr"
	page.get_by_role("textbox", name="이메일").fill(user_email)
	time.sleep(0.3)

def set_terms_check(page):
	page.get_by_role("checkbox", name="이용약관 동의").check()
	time.sleep(0.3)


def submit_signup(page):
	# "회원가입" 버튼이 비활성화 상태인 경우 확인
	if not page.get_by_role("button", name="회원가입").is_enabled():
		logging.error("회원 가입 비활성화 > 필수값 누락 확인")
		return False
	else:
		# 버튼 활성화 상태이면 클릭 처리
		page.get_by_role("button", name="회원가입").click()
		return True

def success_signup(page):
	if page.get_by_role("link", name="로그인하러 가기").is_visible():
		return True
	else:
		return False
