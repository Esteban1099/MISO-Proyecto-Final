from datetime import datetime

import json
import pika
import requests
import time


def enviarNotificacion(mensaje):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit'))
    channel = connection.channel()
    channel.queue_declare(queue='notificaciones')
    channel.basic_publish(exchange='', routing_key='notificaciones', body=mensaje)
    connection.close()
    print("Mensaje enviado: " + mensaje)


def monitor():
    url_pqrs_1 = "http://pqrs-1:5000/healthcheck"
    url_pqrs_2 = "http://pqrs-2:5000/healthcheck"
    url_clientes = "http://clientes:5000/healthcheck"
    while (True):
        response1 = requests.get(url_pqrs_1)
        if response1.status_code != 200:
            mensaje = {"instance": "pqrs-1", "status": "Servicio no disponible",
                       "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            enviarNotificacion(json.dumps(mensaje))

        response2 = requests.get(url_pqrs_2)
        if response2.status_code != 200:
            mensaje = {"instance": "pqrs-2", "status": "Servicio no disponible",
                       "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            enviarNotificacion(json.dumps(mensaje))

        response3 = requests.get(url_clientes)
        if response3.status_code != 200:
            mensaje = {"instance": "clientes", "status": "Servicio no disponible",
                       "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")}
            enviarNotificacion(json.dumps(mensaje))

        time.sleep(3)


if __name__ == '__main__':
    monitor()
