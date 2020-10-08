import requests

dict_to_send = {"hostname": "fibonacci.com", "ip": "127.0.0.1", "as_ip": "127.0.0.1", "as_port": "53533"}
fs_ip = 'http://127.0.0.1'
fs_port = '9090'
fs_add = fs_ip + ':' + fs_port + '/register'
res = requests.put(fs_add, json=dict_to_send)
print(res.text)


dict_to_send = {'hostname': 'fibonacci.com', 'fs_port': '9090', 'as_ip': '127.0.0.1', 'as_port': '53533', 'number': 6}
us_ip = 'http://127.0.0.1'
us_port = '8080'
us_add = us_ip + ':' + us_port + '/fibonacci'
res = requests.get(us_add, params=dict_to_send)
print(res.text)
