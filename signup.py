import time
import random
import string
import logging

def get_random_low_english(length=15):
	return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def set_user(page):
	user_id = get_random_low_english(5)
	page.get_by_role("link", name="회원가입").click()
	page.get_by_role("textbox", name="아이디").fill(user_id)
	page.get_by_role("textbox", name="비밀번호", exact=True).fill("123123")
	page.get_by_role("textbox", name="비밀번호 확인").fill("123123")
	page.get_by_role("textbox", name="이름").fill("test")
	page.get_by_role("textbox", name="이메일").fill("testqwer1234@test.co.kr")
	page.get_by_role("checkbox", name="이용약관 동의").check()
	time.sleep(1)
	page.get_by_role("button", name="회원가입").click()


	logging.info(user_id)
