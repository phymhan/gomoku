from socket import *
SOCKTYP = 'client'

def init_socket():
    if SOCKTYP == "client":
        host = raw_input("Input the server's IP address: ")
        if host == '':
            host = ""
        addr = (host, port)
        sock = socket(AF_INET, SOCK_DGRAM)
        while True:
            sock.sendto("Hi", addr)
            (data, addr) = sock.recvfrom(buf)
            if data == "Got it":
                addr2 = addr
                break
        print "Connected."
        ## Get self IP
        sock.sendto(addr2[0], addr2)
        (data, addr) = sock.recvfrom(buf)
        addr1 = (data, port)
    else:
        host = ""
        addr = (host, port)
        sock = socket(AF_INET, SOCK_DGRAM)
        #sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(addr)
        #sock.listen(1)
        
        print "Waiting for connection..."
        while True:
            (data, addr) = sock.recvfrom(buf)
            if data == "Hi":
                sock.sendto("Got it", addr)
                addr2 = addr
                break
        print "Connected."
        ## Get self IP
        sock.sendto(addr2[0], addr2)
        (data, addr) = sock.recvfrom(buf)
        addr1 = (data, port)

    print "My IP: " + addr1[0] + ", friend's IP: " + addr2[0]
    return sock, addr1, addr2
    
def init_game():
    while True:
        if SOCKTYP == "server":
            s = raw_input("Pick one color, black or white (k/w): ")
            if s == 'k':
                print "You are BLACK; Your friend is WHITE."
                FIRSTPLYR = PLAYER1
            else:
                print "You are WHITE; Your friend is BLACK"
                FIRSTPLYR = PLAYER2
            sock.sendto(s, addr2)
            return FIRSTPLYR
        else:
            print "Waiting for server to setup game..."
            (data, addr) = sock.recvfrom(buf)
            if data == 'k':
                FIRSTPLYR = PLAYER2
                print "You are WHITE; Your friend is BLACK"
            else:
                FIRSTPLYR = PLAYER1
                print "You are BLACK; Your friend is WHITE."
            return FIRSTPLYR

while True:
    global sock
    global addr2

    sock, addr1, addr2 = init_socket()
    FIRSTPLYR = init_game()
    print "First player: " + FIRSTPLYR
    
