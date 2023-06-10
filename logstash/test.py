# PUSH DATA TO logstash:

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'127001 - - [09/Jun/2023:11:54:31 +0000] "GET /api/v1/status HTTP/11" 503 43 "-" "curl/7740"', 0, ('127.0.0.1', 12201))
sock.close()