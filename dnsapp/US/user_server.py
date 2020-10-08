#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests
from flask_api import status
from flask import Flask, request
from socket import socket, AF_INET, SOCK_DGRAM
import json
app = Flask(__name__)


@app.route('/fibonacci', methods = ['GET'])
def accept_request():
    host_name = request.args['hostname']
    fs_port = request.args['fs_port']
    as_ip = request.args['as_ip']
    as_port = int(request.args['as_port'])
    number = request.args['number']
    params = [host_name, fs_port, as_ip, as_port, number ]
    if None in params or '' in params or not number.isdigit():
        return 'missing parameter(s)', status.HTTP_400_BAD_REQUEST
    fs_ip = query_authoritative_server(as_ip, as_port, host_name)
    real_add = 'http://' + fs_ip + ':' + fs_port
    dict_to_send_1 = {'number': number}
    result = requests.get(real_add + '/fibonacci', params=dict_to_send_1)
    return result.text, status.HTTP_200_OK

def query_authoritative_server(as_ip, as_port, host_name):
    sc = socket(AF_INET, SOCK_DGRAM)
    query_json = {'TYPE': 'A', 'NAME': host_name}
    sc.sendto(json.dumps(query_json).encode(), (as_ip, as_port))
    ip_address, server_address = sc.recvfrom(2048)
    return ip_address.decode()

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080, debug=True)
