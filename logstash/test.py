# PUSH DATA TO logstash:

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'99 54 55', 0, ('127.0.0.1', 5044))
sock.close()