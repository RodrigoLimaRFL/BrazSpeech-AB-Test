import json
from flask import Flask, Blueprint, jsonify, render_template, send_file, current_app, request, current_app, session, redirect, url_for


main = Blueprint('main', __name__)


def load_credentials():
    with open(current_app.static_folder + '/json/credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials.get('accounts', [])


@main.route('/read_json')
def read_json():
    file_path = current_app.static_folder + '/json/credentials.json'

    try:
        return send_file(file_path, mimetype="application/json")
    except FileNotFoundError:
        return 'File not found'
    

@main.route('/logged_status')
def logged_status():
    if request.method == 'POST':
        print(request.form['data'])
        return request.form['data']
    return False


@main.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    return redirect(url_for('main.login'))


@main.route('/xab')
def xab():
    return render_template('xab.html', 
                           audio_file_x = '/audio/audio_x.wav',
                           audio_file_a = '/audio/audio_a.wav',
                           audio_file_b = '/audio/audio_b.wav',)


@main.route('/mos')
def mos():
    return render_template('mos.html', audio_file = '/audio/audio_x.wav',)


@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        print(username)
        password = data.get('password')
        print(password)

        users = load_credentials()

        for user in users:
            if user['username'] == username and user['password'] == password:
                # Authentication successful, set the user_id in the session
                session['user_id'] = username

                return jsonify({'success': True, 'redirect': url_for('main.index')})

        # If no matching user is found, return a JSON response with an error message
        session.clear()
        return jsonify({'success': False, 'error': 'Invalid username or password'})
    if request.method == 'GET':
        return render_template('login.html')