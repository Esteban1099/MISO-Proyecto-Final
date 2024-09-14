from flask import Flask, request, jsonify, g
import jwt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f8a5a5d3b80e57c47aebc8a0b7cb4239f35bd42a2039a1e9248d474bcd1183de'

consumidor_data = {}


@app.before_request
def authenticate():
    token = request.headers.get('Authorization')
    if token:
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            decoded_token = jwt.decode(
                token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.user = decoded_token['username']
            print(f"Authenticated user: {g.user}", flush=True)
        except jwt.ExpiredSignatureError:
            print("Token has expired", flush=True)
            g.user = None
        except jwt.InvalidTokenError:
            print("Invalid token", flush=True)
            g.user = None
        except Exception as e:
            print(f"Error decoding token: {e}", flush=True)
            g.user = None
    else:
        print("No token provided", flush=True)
        g.user = None


@app.route('/consumidor', methods=['POST'])
def create():
    if g.user is None:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.json
    consumidor_id = len(consumidor_data) + 1
    consumidor_data[consumidor_id] = {
        'data': data,
        'creator': g.user
    }
    return jsonify({'message': 'Consumidor creado', 'consumidor_id': consumidor_id}), 201


@app.route('/consumidor/<int:consumidor_id>', methods=['GET'])
def get(consumidor_id):
    if g.user is None:
        return jsonify({'message': 'Unauthorized'}), 401

    consumidor = consumidor_data.get(consumidor_id)
    if consumidor is None:
        return jsonify({'message': 'Consumidor no encontrado'}), 404

    if consumidor['creator'] != g.user:
        return jsonify({'message': 'Prohibido: Usted no es el creador de este Consumidor'}), 403

    return jsonify(consumidor['data'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
