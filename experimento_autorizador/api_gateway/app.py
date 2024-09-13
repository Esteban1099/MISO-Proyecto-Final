from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
AUTORIZADOR_URL = 'http://autorizador:5000/validate'

# A protected route


@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    # Validate the token with the auth service
    response = requests.post(AUTORIZADOR_URL, json={'token': token})
    if response.status_code == 200:
        return jsonify({'message': 'Access granted'})
    else:
        return jsonify({'message': 'Access denied'}), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
