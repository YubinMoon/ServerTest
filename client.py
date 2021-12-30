import socket
import time

def log(title,content=None):
  if content:
    print("[{}]:{}".format(title,content))
  else:
    print("[{}]".format(title))

client = socket.socket()
c_name = socket.gethostname()

client.connect((c_name,999))

# name = input("이름을 입력하세요.")
for a in range(3):
  i = input("input:")
  client.send(bytes(i,"utf-8"))
  log("send","success")
  log("return",client.recv(1024).decode())