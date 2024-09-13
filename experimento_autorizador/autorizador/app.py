from flask import Flask, request, jsonify
import jwt
import datetime
from datetime import timezone

app = Flask(__name__)
SECRET_KEY = 'f8a5a5d3b80e57c47aebc8a0b7cb4239f35bd42a2039a1e9248d474bcd1183de'


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == 'admin' and data['password'] == 'password':
        token = jwt.encode({
            'user': data['username'],
            'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(minutes=30)
        }, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/validate', methods=['POST'])
def validate_token():
    token = request.json.get('token')
    try:
        # Decode and validate the token
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'message': 'Valid token', 'user': decoded['user']})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
