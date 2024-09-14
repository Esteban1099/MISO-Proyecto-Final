from flask import Flask

app = Flask(__name__)


@app.route('/pqrs', methods=['POST'])
def pagarNomina():
    return 'PQRs creado desde la instancia backup!', 200


@app.route('/healthcheck')
def healthcheck():
    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
