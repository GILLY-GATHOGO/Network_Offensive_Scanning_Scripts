import socket

server_ip = "196.207.24.206"
port = 22

try:
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, port))
    print("Socket connection to port", port, "established.")

    # You can now send and receive data over the socket
    # For example, sending raw data (if you know the protocol)
    # s.sendall(b"Your data here")
    # data = s.recv(1024)
    # print("Received", repr(data))

finally:
    s.close()
    print("Socket closed.")
