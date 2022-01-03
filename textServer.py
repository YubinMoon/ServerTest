import socket
import time
import json
import threading

PORT = 999
BUFSIZE = 1024
messageQueue = {}
index = 0


def log(title, contents=None):
  if contents:
    print("[{}]:{}".format(title, contents))
  else:
    print("[{}]".format(title))


def makeReturn(type, subject):
  a = {
      "type": type,
      "subject": subject
  }
  temp = json.dumps(a)
  return temp


def connecting(client: socket.socket, address):
  global index
  while True:
    request = client.recv(BUFSIZE).decode()
    if request == "":
      log("종료됨", address)
      client.close()
      return
    temp = json.loads(request)
    if temp["type"] == "message":
      messageQueue[index] = temp["subject"]
      index += 1
      a = makeReturn("lastindex",str(index))
    elif temp["type"] == "getindex":
      a = makeReturn("message", messageQueue[temp["subject"]])
    elif temp["type"] == "lastindex":
      a = makeReturn("lastindex",str(index)) 
    client.send(bytes(a, "utf-8"))


server = socket.socket()
server.bind(("", PORT))

server.listen()
log("리스닝")

while True:
  log("입력대기")
  client, address = server.accept()
  log("연결됨", "address-{}".format(address))
  threading.Thread(target=connecting, args=(client, address)).start()
