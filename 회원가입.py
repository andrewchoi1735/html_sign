import time
import logging
from playwright.sync_api import Playwright, sync_playwright
from urllib.parse import urlparse
import signup as su
from colorama import Fore, Style, init, Back

init(autoreset=True)


# 🎨 컬러 로깅
class ColorFormatter(logging.Formatter):
	def format(self, record):
		level = record.levelname
		if level == 'ERROR':
			record.msg = Fore.RED + str(record.msg) + Style.RESET_ALL
		elif level == 'INFO':
			record.msg = Fore.CYAN + str(record.msg) + Style.RESET_ALL
		elif level == 'WARNING':
			record.msg = Fore.YELLOW + str(record.msg) + Style.RESET_ALL
		return super().format(record)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ColorFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.handlers = []  # 기존 핸들러 제거
logger.addHandler(stream_handler)

# 🌐 환경별 URL
ENV_URLS = {
	"stage": "http://127.0.0.1:5000",
	"qa": "http://127.0.0.1:5000",
	"prod": "http://127.0.0.1:5000"
}


# 📦 스텝 실행 + 로깅
def safe_step(func, page, step_name):
	try:
		logging.info(f"STEP: {step_name} - 시작")
		result = func(page)
		logging.info(f"STEP: {step_name} - 성공")
		return result
	except Exception as e:
		logging.error(f"STEP: {step_name} - 실패 ❌ ({str(e)})", exc_info=True)
		raise


# 🧩 회원가입 플로우
def signup_flow(page: any, url: str) -> str:
	page.goto(url)

	env = get_env_from_url(url)
	logging.info(f"감지된 환경: {env}")

	steps = [
		("화면 이동", su.move_to_signup_page),
		("아이디 설정", su.set_user_id),
		("비밀번호 설정", su.set_user_password),
		("이름 설정", su.set_user_name),
		("이메일 설정", su.set_user_email),
		("약관 동의", su.set_terms_check),
		("회원 가입", su.submit_signup),
		("가입 완료 확인", su.success_signup)
	]

	user_id = None
	for name, step in steps:
		result = safe_step(step, page, name)
		if name == "아이디 설정":
			user_id = result
		time.sleep(0.5)

	return user_id  # ✅ return


# 🌍 URL에서 환경 추출
def get_env_from_url(url: str) -> str:
	domain = urlparse(url).netloc
	if "stage" in domain:
		return "stage"
	elif "qa" in domain:
		return "qa"
	else:
		return "prod"


# ▶ 실행
def run(playwright: Playwright, env) -> None:
	logging.info("=== 회원가입 시작 ===")
	url = ENV_URLS.get(env)
	if not url:
		raise ValueError(f"알 수 없는 환경: {env}")

	browser = playwright.chromium.launch(headless=False)
	context = browser.new_context()
	page = context.new_page()

	user_id = None

	try:
		user_id = signup_flow(page, url)
		logging.info("✅ 회원가입 성공!")
	except Exception:
		logging.error("❌ 회원가입 중단 - 에러 발생")
	finally:
		if user_id:
			logging.info(Fore.BLACK + Back.LIGHTYELLOW_EX + f"  🆔 아이디: {user_id}  " + Style.RESET_ALL)
		else:
			logging.warning("⚠️ user_id가 생성되지 않았습니다.")
		context.close()
		browser.close()
		logging.info("=== 테스트 종료 ===")


# 🏁 시작점
if __name__ == "__main__":
	while True:
		env = input("어떤 환경에서 실행할까요? (stage / qa / prod, 종료하려면 'exit'): ").strip().lower()

		if env == "exit":
			print("프로그램을 종료합니다.")
			exit(0)  # 프로그램 종료

		if env not in ["stage", "qa", "prod"]:
			print("❌ 유효하지 않은 환경입니다. 'stage', 'qa', 'prod' 중에서 선택해주세요.")
		else:
			break  # Valid environment, exit the loop

	with sync_playwright() as playwright:
		run(playwright, env=env)
