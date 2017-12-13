from socket import *

SOCKTYP = "client"
port = 13000
buf = 1024

def init_socket():
    if SOCKTYP == "client":
        host = raw_input("Input the server's IP address: ")
        if host == '':
            host = "127.0.0.1"
        addr = (host, port)
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        while True:
            UDPSock.sendto("Hi", addr)
            (data, addr) = UDPSock.recvfrom(buf)
            if data == "Got it":
                addr2 = addr
                break
        print "Connected."
        ## Get self IP
        UDPSock.sendto(addr2[0], addr2)
        (data, addr) = UDPSock.recvfrom(buf)
        addr1 = (data, port)
        print "My IP: " + addr1[0] + ", friend's IP: " + addr2[0]
    else:
        host = ""
        addr = (host, port)
        UDPSock = socket(AF_INET, SOCK_DGRAM)
        UDPSock.bind(addr)
        print "Waiting for connection..."
        while True:
            (data, addr) = UDPSock.recvfrom(buf)
            if data == "Hi":
                UDPSock.sendto("Got it", addr)
                addr2 = addr
                break
        print "Connected"
        ## Get self IP
        UDPSock.sendto(addr2[0], addr2)
        (data, addr) = UDPSock.recvfrom(buf)
        addr1 = (data, port)
        print "My IP: " + addr1[0] + ", friend's IP: " + addr2[0]
        
    return UDPSock, addr1, addr2

UDPSock, addr1, addr2 = init_socket()
