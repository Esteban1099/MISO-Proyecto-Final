import requests
from flask import Flask

app = Flask(__name__)


@app.route('/pqrs', methods=['POST'])
def pagarNomina():
    return 'PQRs creado desde la instancia 1!', 200


@app.route('/healthcheck')
def healthcheck():
    response = requests.get("http://mockserver:8080/mock1/health")
    return '', response.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
