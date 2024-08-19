import socket
import cv2
import numpy as np
import pickle
import trimesh

HOST, PORT = "localhost", 9999

data = 'Hello'

vid = cv2.VideoCapture(0)

def recvall(sock):
    BUFF_SIZE = 4096 
    print(BUFF_SIZE)
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        if len(part) == 0:
            break
        data += part
  
    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    _, frame = vid.read()
    print(frame.dtype, frame.shape)
    
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, encimg = cv2.imencode('.jpg', frame, encode_param)


    # cv2.imwrite('img.jpeg', cv2.imdecode(encimg, 1))

    sock.sendall(bytes(encimg))

    result = recvall(sock)
    meshes = pickle.loads(result)

#0=LEFT, 1=RIGHT
i=0
for mesh in meshes:
    with open('HapticsGUI2/Meshes/mesh' + str(i) + '.stl', 'w') as f:
        f.write(trimesh.exchange.stl.export_stl_ascii(mesh))
    i+=1