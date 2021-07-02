import requests
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, send_file, make_response

app = Flask(__name__)

uri = 'http://localhost:5000'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        url = f'{uri}/admin/signup'
        data = dict(request.form)
        req_signup = requests.post(url, json=data)
        if req_signup.ok:
            return redirect(url_for('login'))
        return req_signup.json()

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        url = f'{uri}/login'
        data = dict(request.form)
        response = requests.post(url, json=data)
        if response.ok:
            r_json = response.json()
            logged_in_as = r_json['logged_in_as']
            return redirect(url_for('verify', logged_in_as=logged_in_as))
        print('unsuccessful')

    return render_template('login.html')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        url = f'{uri}/sign'
        data_files = request.files
        data_json = request.form
        print(request.files)
        print(request.form)
        response = requests.post(url, files=data_files, data=data_json)

        if response.ok:
            response = make_response(response.content)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = \
                'inline; filename=%s.pdf' % 'yourfilename'
            return response
        else:
            return render_template('signdoc.html', data=response.json())

    return render_template('signdoc.html')


@app.route('/verify/<logged_in_as>', methods=['GET', 'POST'])
def verify(logged_in_as='user'):
    url = f'{uri}/verify'
    if 'doc_id' in request.values:
        response = requests.post(url, data=request.values)
        data = response.json()
        if response.ok:
            return render_template('profile.html', data=data)
        elif response.status_code == 404:
            return render_template('invalid.html')
        else:
            return render_template('invalid.html')

    if request.method == 'POST':
        response = requests.post(url, data=request.form)
        data = response.json()
        if response.ok:
            return render_template('profile.html', data=data)
        elif response.status_code == 404:
            return render_template('invalid.html')
        else:
            return render_template('invalid.html')

    return render_template('verifyDoc.html', logged_in_as=logged_in_as)


@app.route('/request', methods=['GET', 'POST'])
def requesttrans():
    if request.method == 'POST':
        school = request.form['institution']

        filename = f'{school}-david-transcript.pdf'
        return send_from_directory('static', path=filename,
                                   as_attachment=True, filename=filename)
    return render_template('requesttrans.html')


@app.route('/gen/transcript', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        return send_from_directory('static', path='uniben-david-transcript.pdf',
                                   as_attachment=True, filename='uniben-david-transcript.pdf')
    return render_template('gentranscript.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
