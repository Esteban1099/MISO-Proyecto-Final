from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
AUTORIZADOR_URL = 'http://autorizador:5000/validate'
CLIENTE_URL = 'http://cliente:5002/cliente'
CONSUMIDOR_URL = 'http://consumidor:5003/consumidor'


@app.route('/cliente', methods=['POST'])
def create_cliente():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Falta el token'}), 401

        response = requests.post(AUTORIZADOR_URL, json={'token': token})
        if response.status_code != 200:
            return jsonify({'message': 'Acceso denegado'}), 401

        token_data = response.json()
        user_role = token_data.get('role')

        if user_role != 'cliente':
            return jsonify({'message': 'Se requiere rol de cliente para esta accion'}), 403

        cliente_response = requests.post(
            CLIENTE_URL, headers={'Authorization': token}, json=request.json)
        return jsonify(cliente_response.json()), cliente_response.status_code
    except Exception as e:
        # Catch and log the exception
        print(f"An error occurred: {str(e)}", flush=True)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/cliente/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Falta el token'}), 401

        response = requests.post(AUTORIZADOR_URL, json={'token': token})
        if response.status_code != 200:
            return jsonify({'message': 'Acceso denegado'}), 401

        token_data = response.json()
        user_role = token_data.get('role')

        if user_role != 'cliente':
            return jsonify({'message': 'Se requiere rol de cliente para esta accion'}), 403

        cliente_response = requests.get(
            f'{CLIENTE_URL}/{cliente_id}', headers={'Authorization': token})
        return jsonify(cliente_response.json()), cliente_response.status_code
    except Exception as e:
        # Catch and log the exception
        print(f"An error occurred: {str(e)}", flush=True)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/consumidor', methods=['POST'])
def create_consumidor():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Falta el token'}), 401

        response = requests.post(AUTORIZADOR_URL, json={'token': token})
        if response.status_code != 200:
            return jsonify({'message': 'Acceso denegado'}), 401

        token_data = response.json()
        user_role = token_data.get('role')

        if user_role != 'consumidor':
            return jsonify({'message': 'Se requiere rol de consumidor para esta accion'}), 403

        consumidor_response = requests.post(
            CONSUMIDOR_URL, headers={'Authorization': token}, json=request.json)
        return jsonify(consumidor_response.json()), consumidor_response.status_code
    except Exception as e:
        # Catch and log the exception
        print(f"An error occurred: {str(e)}", flush=True)
        return jsonify({'message': 'Internal Server Error'}), 500


@app.route('/consumidor/<int:consumidor_id>', methods=['GET'])
def get_consumidor(consumidor_id):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Falta el token'}), 401

        response = requests.post(AUTORIZADOR_URL, json={'token': token})
        if response.status_code != 200:
            return jsonify({'message': 'Acceso denegado'}), 401

        token_data = response.json()
        user_role = token_data.get('role')

        if user_role != 'consumidor':
            return jsonify({'message': 'Se requiere rol de consumidor para esta accion'}), 403

        cliente_response = requests.get(
            f'{CONSUMIDOR_URL}/{consumidor_id}', headers={'Authorization': token})
        return jsonify(cliente_response.json()), cliente_response.status_code
    except Exception as e:
        # Catch and log the exception
        print(f"An error occurred: {str(e)}", flush=True)
        return jsonify({'message': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
