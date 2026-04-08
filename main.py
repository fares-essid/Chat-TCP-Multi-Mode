import subprocess
import time


server = subprocess.Popen(['python', 'server.py'])
time.sleep(1) 

client = subprocess.Popen(['python', 'client.py'])

server.wait()
client.wait()
