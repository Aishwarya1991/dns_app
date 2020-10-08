#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_api import status
import json
from socket import socket, AF_INET, SOCK_DGRAM
app = Flask(__name__)


@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    number = request.args['number']
    result = get_fibonacci(number)
    return 'Fibonacci of ' + number + ' is ' + str(result)

def get_fibonacci(number):
    number = int(number)
    if number <= 2:
        return 1
    return get_fibonacci(number-1) + get_fibonacci(number-2)


@app.route('/register', methods = ['PUT'])
def register():
    content = request.get_json()
    hostname = content['hostname']
    ip = content['ip']
    as_ip = content['as_ip']
    as_port = int(content['as_port'])
    register_json = {'TYPE': 'A', 'NAME': hostname, 'VALUE': ip, 'TTL': 10}
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.sendto(json.dumps(register_json).encode(), (as_ip, as_port))
    response_message, server_address = client_socket.recvfrom(2048)
    return 'success', status.HTTP_201_CREATED

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9090, debug=True)