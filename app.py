import requests
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

uri = 'http://localhost:5000'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/admin')
def index_admin():
    return render_template('admin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        url = f'{uri}/signup'
        data = dict(request.form)
        print(data)
        response = requests.post(url, json=data)
        r_json = response.json()
        return redirect(url_for('verify', logged_in_as='user'))

    return render_template('signup.html')


@app.route('/admin/signup', methods=['GET', 'POST'])
def adminsignup():
    if request.method == 'POST':
        url = f'{uri}/admin/signup'
        data = dict(request.form)
        response = requests.post(url, json=data)
        r_json = response.json()
        return redirect(url_for('verify', logged_in_as='admin'))

    return render_template('adminsignup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        url = f'{uri}/login'
        data = dict(request.form)
        response = requests.post(url, json=data)
        if response.ok:
            r_json = response.json()
            logged_in_as = r_json['logged_in_as']
            print(logged_in_as)
            return redirect(url_for('verify', logged_in_as=logged_in_as))
        print('unsuccessful')

    return render_template('login.html')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        url = f'{uri}/sign'
        data = request.files
        response = requests.post(url, files=data)
        if response.ok:
            return render_template('signed.html')

    return render_template('sign.html')


@app.route('/verify/<logged_in_as>', methods=['GET', 'POST'])
def verify(logged_in_as):
    if request.method == 'POST':
        url = f'{uri}/verify'
        data = request.files
        response = requests.post(url, files=data)
        if response.ok:
            return render_template('valid.html')
        return render_template('invalid.html')

    return render_template('verify.html', logged_in_as=logged_in_as)


@app.route('/upload')
def upload():
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
