import socket 
import threading 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9000))

client.send(b"Hello Server, this is Client!")
client.recv(1024).decode()