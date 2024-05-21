import socket
import random
import os

from acoustools.Mesh import centre_scatterer, load_scatterer, scatterer_file_name, get_centre_of_mass_as_points
from acoustools.Visualiser import Visualise_mesh
import acoustools.Constants as c
import vedo
import numpy as np
import json


#STEP 1: GET HAND FROM UNITY

def get_hand_from_unity(host, port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.sendall(message.encode('utf-8'))
    client_socket.close()


host = '127.0.0.1'  # Localhost
port = 9999         # Port number should match the Unity server port

input("Press enter when hand in position")

HAND_ID = "BEM_HAND" + str(random.randint(0,1000))
print(HAND_ID)
get_hand_from_unity(host, port,HAND_ID)

#STEP 2: LOAD MESH

MAX_WAIT = 100000000
waits = 0
METADATA_PATH = './Media/Metadata/'+ HAND_ID + '_metadata.json'
while not os.path.isfile(METADATA_PATH) and waits < MAX_WAIT:
    waits -= 1


HAND_HIEGHT = 0.06
HAND_PATH = './Media/Hands/'+ HAND_ID + '.obj'
hand_origional = load_scatterer(HAND_PATH)

correction = centre_scatterer(hand_origional)
print(correction)

#STEP 3: PROCESS MESH

hand = hand_origional.clean().smooth()
print(hand.is_closed())

hand.collapse_edges(c.wavelength/2)
hand.filename = scatterer_file_name(hand)

edges = hand.count_vertices()
mask = np.where(edges != 3)[0]
hand.delete_cells(mask)
hand.filename = scatterer_file_name(hand)


hand.subdivide(2)
hand.compute_cell_size()
hand.filename = scatterer_file_name(hand)


#STEP 4: LOAD METADATA

metadata = json.load(open(METADATA_PATH))

#STEP 5: GET PALM POSITION

# palm_position = metadata['Hand']['PalmPosition']
# palm_position[1] *= -1

# palm_position_m = [i/1000 for i in palm_position]

# # print(palm_position_m, palm_position_corrected, correction)

# vedo.show(hand, vedo.Point(palm_position_m),axes=1)


# print(p)
# _, centre = vedo.closest(p, centres)
# ID = np.where(centre==centres)[0][0]
