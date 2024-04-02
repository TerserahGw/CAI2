from flask import Flask, jsonify, request, render_template
from characterai import PyCAI

app = Flask(__name__, template_folder='.')
token = None

def get_client():
    return PyCAI(token)
    
@app.route('/')
def index():
    return ''
    
@app.route('/newchat')
def new_chat():
    global token
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_client()
    char_id = request.args.get('q', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    data = client.chat.new_chat(char_id)

    return jsonify(data), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/cai')
def cai_chat():
    global token
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_client()
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

@app.route('/delcai')
def delete_chat():
    global token
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_client()
    history_id = request.args.get('history_id', '')
    uuids_to_delete = request.args.get('uuids_to_delete', '')

    if not history_id:
        return jsonify({'error': 'History ID is required'}), 400
    if not uuids_to_delete:
        return jsonify({'error': 'UUIDs to delete are required'}), 400

    result = client.chat.delete_chat(history_id, uuids_to_delete)

    return jsonify(result), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/histories')
def get_histories():
    global token
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_client()
    char_id = request.args.get('charid', '')

    if not char_id:
        return jsonify({'error': 'Character ID is required'}), 400

    histories = client.chat.get_histories(char_id)

    return jsonify(histories), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/history')
def get_history():
    global token
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token is required'}), 400
    
    client = get_client()
    history_id = request.args.get('history_id', '')

    if not history_id:
        return jsonify({'error': 'History ID is required'}), 400

    history = client.chat.get_history(history_id)

    return jsonify(history), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
