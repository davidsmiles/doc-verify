import requests
from flask import Flask, request, render_template

app = Flask(__name__)

uri = 'http://localhost:5000'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        url = f'{uri}/signup'
        data = dict(request.form)
        response = requests.post(url, json=data)
        r_json = response.json()
        return r_json

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        url = f'{uri}/login'
        data = dict(request.form)
        response = requests.post(url, json=data)
        r_json = response.json()
        return r_json

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


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        url = f'{uri}/sign'
        data = request.files
        response = requests.post(url, files=data)
        if response.ok:
            return render_template('valid.html')
        return render_template('invalid.html')

    return render_template('verify.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
