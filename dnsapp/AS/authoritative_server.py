from socket import socket, AF_INET, SOCK_DGRAM
import json

sock = socket(AF_INET, SOCK_DGRAM)
server_port = 53533
sock.bind(('', server_port))
ip_dict = {}

def get_request(msg):
    message = json.loads(msg.decode())
    ip_addr = 'TTL' in message

    if ip_addr:
        host_name = message['NAME']
        ip = message['VALUE']
        request_type = message['TYPE']
        ttl = message['TTL']
        return register(host_name, ip, request_type, ttl)
    else:
        host_name = message['NAME']
        request_type = message['TYPE']
        return dns_query(host_name, request_type)

def register(hostname, ip, request_type, ttl):
    message = {'TYPE': request_type, 'NAME': hostname, 'VALUE': ip, 'TTL': ttl}
    key = request_type + ' ' + hostname
    ip_dict[key] = message
    return json.dumps('').encode()


def dns_query(hostname, request_type):
    content = ip_dict[request_type + ' ' + hostname]
    fs_ip = content['VALUE']
    return str(fs_ip).encode()



while True:
    query_message, addr = sock.recvfrom(2048)
    response_message = get_request(query_message)
    sock.sendto(response_message, addr)