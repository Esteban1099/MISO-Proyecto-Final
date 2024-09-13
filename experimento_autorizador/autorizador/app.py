from flask import Flask, request, jsonify
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f8a5a5d3b80e57c47aebc8a0b7cb4239f35bd42a2039a1e9248d474bcd1183de'

users = {
    'client_user1': {'password': 'clientpass1', 'role': 'cliente'},
    'client_user2': {'password': 'clientpass2', 'role': 'cliente'},
    'consumer_user1': {'password': 'consumerpass1', 'role': 'consumidor'},
    'consumer_user2': {'password': 'consumerpass2', 'role': 'consumidor'}
}


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username]['password'] == password:
        token = jwt.encode({
            'username': username,
            'role': users[username]['role'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token})

    return jsonify({'message': 'Credenciales invalidas'}), 401


@app.route('/validate', methods=['POST'])
def validate():
    token = request.json.get('token')
    try:
        decoded_token = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'valid': True, 'role': decoded_token['role']})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'El token expiro'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token invalido'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
