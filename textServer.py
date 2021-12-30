import socket
import time
import threading

PORT = 999
BUFSIZE = 1024


def log(title, contents=None):
  if contents:
    print("[{}]:{}".format(title, contents))
  else:
    print("[{}]".format(title))


def connecting(client: socket.socket, address):
  print(client)
  while True:
    a = client.recv(BUFSIZE).decode()
    log("입력",a)
    if a == ""or a == 'a':
      log("종료됨",address)
      client.close()
      return
    client.send(bytes(a,"utf-8"))

server = socket.socket()
server.bind(("", PORT))

server.listen()
log("리스닝")

while True:
  log("입력대기")
  client, address = server.accept()
  log("연결됨", "address-{}".format(address))
  threading.Thread(target=connecting, args=(client, address)).start()
