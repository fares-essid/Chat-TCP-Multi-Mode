import socket 
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"hello server from client", ("127.0.0.1", 8080))
data, addr =client.recvfrom(1024)

print(f"received from server: {data.decode()}")
