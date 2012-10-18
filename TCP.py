import socket

class TCP:
    
    def __init__(self, ip, port):
        self.ip = ip
        self.port= port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.ip, self.port))
    
    #sends a string of information regarding the position selected by our agent
    def send_position(self, position_index):
        self.s.send(tr(position_index))
        return False
    
    #sends a string of inforamtino regarding the piece selected by our agent
    def send_piece(self, piece_index):
        self.s.send(str(piece_index))
        return False
    
    #receives a string of information regarding the position selected by a remote agent
    def receive_position(self):
        return self.s.recv(1024)
    
    #receives a string of informatino regarding the piece selected by a remote agent
    def receive_piece(self):
        return self.s.recv(1024)
 
#3 import socket
#   4 
#   5 
#   6 TCP_IP = '127.0.0.1'
#   7 TCP_PORT = 5005
#   8 BUFFER_SIZE = 1024
#   9 MESSAGE = "Hello, World!"
#  10 
#  11 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  12 s.connect((TCP_IP, TCP_PORT))
#  13 s.send(MESSAGE)
#  14 data = s.recv(BUFFER_SIZE)
#  15 s.close()
#  16 
#  17 print "received data:", data