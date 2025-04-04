from flask import Flask, render_template, request, redirect, session
import json
import os
from flask import jsonify

USER_FILE = 'users.json'


def load_users():
	if os.path.exists(USER_FILE):
		with open(USER_FILE, 'r', encoding='utf-8') as f:
			return json.load(f)
	return {}


def save_users(data):
	with open(USER_FILE, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)
app = Flask(__name__)
app.secret_key = 'secret'  # 세션용

# 임시 유저 저장 (DB 대신 사용)
users = load_users()


@app.route('/')
def home():
	if 'user' in session:
		return render_template('home.html', user=session['user'])
	return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'GET':
		return render_template('signup.html', form={})

	form_data = request.form
	requested_id = form_data.get('id', '').strip()
	checked_id = session.get('checked_id')

	# ✅ 서버에서도 중복 확인 여부 검증
	if checked_id != requested_id:
		return render_template('signup.html', error="아이디 중복 확인이 필요합니다.", form=form_data)

	if form_data.get('password') != form_data.get('password_check'):
		return render_template('signup.html', error="비밀번호가 일치하지 않습니다.", form=form_data)

	if 'terms' not in form_data:
		return render_template('signup.html', error="이용약관에 동의해주세요.", form=form_data)

	users[requested_id] = {
		'password':form_data['password'],
		'name':form_data['name'],
		'email':form_data['email']
	}
	save_users(users)

	session.pop('checked_id', None)
	return redirect('/signup/success')


@app.route('/check_id', methods=['POST'])
def check_id():
	user_id = request.form.get('id', '').strip()
	if not user_id:
		return jsonify({'result':False, 'message':'아이디를 입력해주세요.'})
	if user_id in users:
		return jsonify({'result':False, 'message':'이미 존재하는 아이디입니다.'})

	# ✅ 중복 확인 통과 시 세션에 저장!
	session['checked_id'] = user_id

	return jsonify({'result':True, 'message':'사용 가능한 아이디입니다.'})


@app.route('/signup/success')
def signup_success():
	return render_template('signup_success.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		user = users.get(request.form['id'])
		if user and user['password'] == request.form['password']:
			session['user'] = request.form['id']
			return redirect('/')
		# 로그인 실패 시 에러 메시지와 함께 로그인 페이지 렌더
		return render_template('login.html', error="아이디 또는 비밀번호가 올바르지 않습니다.")
	return render_template('login.html')


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
	if 'user' not in session:
		return redirect('/login')

	if request.method == 'POST':
		user_id = session['user']
		if request.form['password'] != users[user_id]['password']:
			return "비밀번호 불일치"
		if 'agree' not in request.form:
			return "동의 필요"
		reason = request.form['reason']
		del users[user_id]
		save_users(users)
		session.pop('user')
		return render_template('withdraw_success.html', user=user_id, reason=reason)

	# GET 요청일 경우 → 탈퇴 폼 보여줌
	return render_template('withdraw.html')



@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect('/login')


if __name__ == '__main__':
	app.run(debug=True)
