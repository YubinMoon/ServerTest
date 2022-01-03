from tkinter import *
import socket
import json
import time
import sys
import threading

RUNNING = True
SERVERIP = "192.168.21.57"
PORT = 999
BUFSIZE = 1024
netQueue = []
last_index = 0

def dataCheck():
  makeRequest("lastindex",last_index)
  window.after(100,dataCheck)

def makeRequest(type, subject):
  a = {
      "type": type,
      "subject": subject
  }
  temp = json.dumps(a)
  netQueue.append(temp)


def setSocket():
  global last_index
  client.connect((SERVERIP, PORT))
  while RUNNING:
    while netQueue:
      request = bytes(netQueue.pop(0), "utf-8")
      if len(request) < BUFSIZE:
        client.send(request)
        result = json.loads(client.recv(BUFSIZE).decode())
        if result["type"] == "message":
          subject = result["subject"]
          makeLine(subject["name"], subject["content"])
        elif result["type"]  == "lastindex":
          if last_index == 0:
            last_index = int(result["subject"])
          for i in range(last_index,int(result["subject"])):
            makeRequest("getindex",i)
          last_index = int(result["subject"])
    time.sleep(0.2)    


def makeLine(name, content):
  frame = Frame(contents_frame, width=100, bg='red', bd=5)
  frame.pack(side=TOP, fill=X, expand=True)
  Label(frame, text=name).pack(side=LEFT)
  Message(frame, text=content, anchor=W, justify=LEFT,
          width=200).pack(side=TOP, fill=X)


def strInput(event: Event):
  text = entry_input.get()
  name = entry_name.get()
  a = {
    "name":name,
    "content":text
  }
  makeRequest("message",a)
  entry_input.delete(0, END)


client = socket.socket()
window = Tk()
window.title("test_GUI")
window.geometry("400x500")
window.resizable(False, False)

frame_top = Frame(window, bg='blue', bd=5)
frame_top.pack(side=TOP, fill=BOTH, expand=True)
frame_bottom = Frame(window, bg='yellow', bd=5)
frame_bottom.pack(side=BOTTOM, fill=BOTH, expand=False)
entry_name = Entry(frame_bottom,width=10)
entry_name.insert(0,"Name")
entry_name.pack(side=LEFT)
frame_input = Frame(frame_bottom, bg='orange', bd=5)
frame_input.pack(side=BOTTOM, fill=BOTH)
entry_input = Entry(frame_input)
entry_input.bind("<Return>", strInput)
entry_input.pack(side=BOTTOM, fill=X)
scrollbar = Scrollbar(frame_top, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)
canvas = Canvas(frame_top, bg='green', yscrollcommand=scrollbar.set)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
contents_frame = Frame(canvas, bg='gray', bd=5)
contents_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
contents_frame.pack(side=TOP, fill=X, expand=True)
frame_canvas = canvas.create_window((0, 0), window=contents_frame, anchor="nw")
canvas.bind("<Configure>", lambda event: canvas.itemconfig(
    frame_canvas, width=event.width))
scrollbar.configure(command=canvas.yview)
threading.Thread(target=setSocket).start()
window.after(100,dataCheck)
window.mainloop()
RUNNING = False