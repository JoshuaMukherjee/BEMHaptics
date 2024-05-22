import socket

def get_hand_from_unity(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()


host = '127.0.0.1'  # Localhost
port = 9999         # Port number should match the Unity server port


participants = 999999999

input('Generating hand')
get_hand_from_unity(host, port, "participant_"+str(participants))
     




