from flask import Flask, jsonify, request, render_template
from characterai import PyCAI

app = Flask(__name__, template_folder='.')
token_main = '29422450f9ebdf864bb798a6f9796cdab019d9f1'  # Token dari kode 1
token_api2 = None

def get_api2_client():
    global token_api2
    return PyCAI(token_api2)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/api')
def home():
    global token_main
    client = PyCAI(token_main)
    return render_template('oldhome.html')

@app.route('/home')
def api():
    return render_template('home.html')

@app.route('/api/search')
def search_character():
    global token_main
    client = PyCAI(token_main)
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    results = client.character.search(query)

    return jsonify(results), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/newchat')
def new_chat():
    global token_main
    client = PyCAI(token_main)
    char_id = request.args.get('q', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    data = client.chat.new_chat(char_id)

    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/trending')
def trending_characters():
    global token_main
    client = PyCAI(token_main)
    trending = client.character.trending()

    return jsonify(trending), 200, {'Content-Type': 'application/json; charset=utf-8'}
    
@app.route('/api/rec')
def rec_characters():
    global token_main
    client = PyCAI(token_main)
    rec = client.character.recommended()

    return jsonify(rec), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/info')
def info_character():
    global token_main
    client = PyCAI(token_main)
    char_id = request.args.get('id', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    info = client.character.info(char_id)

    return jsonify(info), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/cai')
def cai_chat():
    global token_main
    client = PyCAI(token_main)
    char_id = request.args.get('charid', '')
    message = request.args.get('message', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    chat = client.chat.get_chat(char_id)
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    data = client.chat.send_message(chat['external_id'], tgt, message)

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    return jsonify({'name': name, 'reply': text}), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api2/newchat')
def new_chat_api2():
    global token_api2
    token_api2 = request.args.get('token')
    if not token_api2:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_api2_client()
    char_id = request.args.get('charid', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    data = client.chat.new_chat(char_id)

    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api2/cai')
def cai_chat_api2():
    global token_api2
    token_api2 = request.args.get('token')
    if not token_api2:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_api2_client()
    char_id = request.args.get('charid', '')
    message = request.args.get('message', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400
    if not message:
        return jsonify({'error': 'Message is required'}), 400

    chat = client.chat.get_chat(char_id)
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    data = client.chat.send_message(chat['external_id'], tgt, message)

    name = data['src_char']['participant']['name']
    text = data['replies'][0]['text']

    return jsonify({'name': name, 'reply': text}), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api2/delcai')
def delete_chat():
    global token_api2
    token_api2 = request.args.get('token')
    if not token_api2:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_api2_client()
    history_id = request.args.get('history_id', '')
    uuids_to_delete = request.args.get('uuids_to_delete', '')

    if not history_id:
        return jsonify({'error': 'History ID is required'}), 400
    if not uuids_to_delete:
        return jsonify({'error': 'UUIDs to delete are required'}), 400

    result = client.chat.delete_chat(history_id, uuids_to_delete)

    return jsonify(result), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api2/histories')
def get_histories():
    global token_api2
    token_api2 = request.args.get('token')
    if not token_api2:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_api2_client()
    char_id = request.args.get('charid', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    histories = client.chat.get_histories(char_id)

    return jsonify(histories), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api2/history')
def get_history():
    global token_api2
    token_api2 = request.args.get('token')
    if not token_api2:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_api2_client()
    history_id = request.args.get('history_id', '')

    if not history_id:
        return jsonify({'error': 'History ID is required'}), 400

    history = client.chat.get_history(history_id)

    return jsonify(history), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
