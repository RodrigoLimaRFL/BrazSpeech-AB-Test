import json
from flask import Blueprint, jsonify, render_template, send_file, current_app, request, current_app, session, redirect, url_for
from .readAssignment import get_xab_total, get_mos_total, get_mos_audio, get_xab_audio_x, get_xab_audio_a, get_xab_audio_b, set_mos_answer, set_xab_answer


main = Blueprint('main', __name__)


def load_credentials() -> list:
    """Loads the credentials from the credentials.json file.

    Returns:
        list: List of all the accounts in the credentials.json file.
    """
    with open(current_app.static_folder + '/json/credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials.get('accounts', [])


def update_mos_number(user_id: str, mos_number: int):
    """Updates the current audio file number of the mos test for the specified user.

    Args:
        user_id (str): The username of the user.
        mos_number (int): The new audio file number.
    """
    with open(current_app.static_folder + '/json/credentials.json', 'r') as f:
        credentials = json.load(f)
    for user in credentials['accounts']:
        if user['username'] == user_id:
            user['mos_number'] = mos_number
    with open(current_app.static_folder + '/json/credentials.json', 'w') as f:
        json.dump(credentials, f)


def update_xab_number(user_id, xab_number):
    """Updates the current audio file number of the xab test for the specified user.

    Args:
        user_id (_type_): The username of the user.
        xab_number (_type_): The new audio file number.
    """
    with open(current_app.static_folder + '/json/credentials.json', 'r') as f:
        credentials = json.load(f)
    for user in credentials['accounts']:
        if user['username'] == user_id:
            user['xab_number'] = xab_number
    with open(current_app.static_folder + '/json/credentials.json', 'w') as f:
        json.dump(credentials, f)


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


@main.route('/xab', methods=['POST', 'GET'])
def xab():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        xab_number = session.get('xab_number', 0)
        return render_template('xab.html', 
                            audio_file_x = get_xab_audio_x(session["user_id"], xab_number),
                            audio_file_a = get_xab_audio_a(session["user_id"], xab_number),
                            audio_file_b = get_xab_audio_b(session["user_id"], xab_number),
                            xab_number = xab_number,
                            xab_total = get_xab_total(session['user_id']),)
    if request.method == 'POST':
        data = request.get_json()
        set_xab_answer(session['user_id'], session['xab_number'], data.get('selectedAudio'))
        session['xab_number'] = session.get('xab_number', 0) + 1
        update_xab_number(session['user_id'], session['xab_number'])
        return jsonify({'success': True, 'redirect': url_for('main.xab')})


@main.route('/mos', methods=['POST', 'GET'])
def mos():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        mos_number = session.get('mos_number', 0)
        print(url_for("static", filename=get_mos_audio(session["user_id"], mos_number)))
        return render_template('mos.html', audio_file = get_mos_audio(session["user_id"], mos_number),
                            mos_number = mos_number,
                            mos_total = get_mos_total(session['user_id']))
    if request.method == 'POST':
        data = request.get_json()
        set_mos_answer(session['user_id'], session['mos_number'], data.get('selectedGrade'))
        session['mos_number'] = session.get('mos_number', 0) + 1
        update_mos_number(session['user_id'], session['mos_number'])
        return jsonify({'success': True, 'redirect': url_for('main.mos')})


@main.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        print(username)
        password = data.get('password')
        print(password)

        users = load_credentials()

        # check if form is correct
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user_id'] = username
                session['xab_number'] = user['xab_number']
                session['mos_number'] = user['mos_number']

                return jsonify({'success': True, 'redirect': url_for('main.index')})

        # If no matching user is found, return a JSON response with an error message and clears the session
        session.clear()
        return jsonify({'success': False, 'error': 'Invalid username or password'})
    if request.method == 'GET':
        return render_template('login.html')