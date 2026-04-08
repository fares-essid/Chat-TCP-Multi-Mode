import socket 

server =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 8080))

while True:
    data, addr = server.recvfrom(1024)
    print(f"msg received from client with {addr}: {data.decode()}")
    server.sendto(b'msg bien recu du client avec ', addr)