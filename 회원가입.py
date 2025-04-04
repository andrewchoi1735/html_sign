import time
import logging
from playwright.sync_api import Playwright, sync_playwright, TimeoutError as PlaywrightTimeoutError
from urllib.parse import urlparse
import signup as su
# 로깅 설정
logging.basicConfig(
	level=logging.INFO,
	format="[%(asctime)s] %(levelname)s: %(message)s",
	handlers=[logging.StreamHandler()]
)

ENV_URLS = {
	"stage": "http://127.0.0.1:5000",
	"qa": "http://127.0.0.1:5000",
	"prod": "http://127.0.0.1:5000"
}


def safe_step(func, page, step_name):
	try:
		logging.info(f"STEP: {step_name} - 시작")
		func(page)
		logging.info(f"STEP: {step_name} - 성공")
	except Exception as e:
		logging.error(f"STEP: {step_name} - 실패 ❌ ({str(e)})", exc_info=True)
		raise  # 전체 플로우 중단을 원하면 이 라인 유지, 아니면 주석 처리


def signup_flow(page: any, url: str) -> None:
	page.goto(url)

	# 환경 추출
	env = get_env_from_url(url)
	logging.info(f"감지된 환경: {env}")

	steps = [
		("회원 가입", su.set_user)
	]

	for name, step in steps:
		safe_step(step, page, name)
		time.sleep(0.5)  # 로딩 처리


def get_env_from_url(url: str) -> str:
	domain = urlparse(url).netloc
	if "stage" in domain:
		return "stage"
	elif "qa" in domain:
		return "qa"
	else:
		return "prod"


def run(playwright: Playwright, env) -> None:
	logging.info("=== 회원가입 시작 ===")
	url = ENV_URLS.get(env)
	if not url:
		raise ValueError(f"알 수 없는 환경: {env}")

	browser = playwright.chromium.launch(headless=False)
	context = browser.new_context()
	page = context.new_page()

	try:
		signup_flow(page, url)
		logging.info("✅ 회원가입 성공!")
	except Exception:
		logging.error("❌ 회원가입 중단 - 에러 발생")
	finally:
		context.close()
		browser.close()
		logging.info("=== 테스트 종료 ===")


if __name__ == "__main__":
	env = input("어떤 환경에서 실행할까요? (stage / qa / prod): ").strip().lower()

	if env not in ["stage", "qa", "prod"]:
		print("❌ 유효하지 않은 환경입니다. 'stage', 'qa', 'prod' 중에서 선택해주세요.")
	else:
		with sync_playwright() as playwright:
			run(playwright, env=env)
