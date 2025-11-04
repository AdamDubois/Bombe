import socket
import class_DEL as led

LED = led.DEL()

UDP_IP = "0.0.0.0" # listen to everything
UDP_PORT = 12345 # port

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(512) # random buffer size, doesn't matter here..
  print("received message:", data)
  #simplest way to react.. of course, a better parser should be used, and add GPIO code, etc..
  if data==b'LED=1\n':
    LED.set_all_del_color((0,255,0)) #green
    LED.strip.show()
  elif data==b'LED=0\n':
    LED.set_all_del_color((0,0,0)) #off
    LED.strip.show()