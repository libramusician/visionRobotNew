import socket


class UDPSender():
    def __init__(self, addr):
        # create a UDP socket
        self.addr = addr
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # send a string message to address
    def send(self, response:str):
        self.s.sendto(response.encode(), self.addr)

    def close(self):
        self.s.close()