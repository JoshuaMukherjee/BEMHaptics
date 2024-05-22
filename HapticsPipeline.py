import socket
import random
import os

from acoustools.Mesh import centre_scatterer, load_scatterer, scatterer_file_name, get_centre_of_mass_as_points, get_centres_as_points
from acoustools.Visualiser import Visualise_mesh
import acoustools.Constants as c
import vedo
import numpy as np
import json
import torch

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
h = hand_origional.clone()

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

#STEP 5: GET PALM POSITIONS

thumb_UC = metadata['Fingers']['TYPE_THUMB']['TYPE_METACARPAL']['NextJoint']
index_UC = metadata['Fingers']['TYPE_INDEX']['TYPE_METACARPAL']['NextJoint']
little_UC = metadata['Fingers']['TYPE_PINKY']['TYPE_METACARPAL']['NextJoint']


thumb = [thumb_UC[i] + correction[i] for i in [0,1,2]]
index = [index_UC[i] + correction[i] for i in [0,1,2]]
little = [little_UC[i] + correction[i] for i in [0,1,2]]

thumb[2] -= 0.01
index[2] -= 0.01
little[2] -= 0.01

centres = hand.cell_centers

N = len(centres)

_, centre_t = vedo.closest(thumb, centres)
ID_t = np.where(centre_t==centres)[0][0]

_, centre_i = vedo.closest(index, centres)
ID_i = np.where(centre_i==centres)[0][0]

_, centre_l = vedo.closest(little, centres)
ID_l = np.where(centre_l==centres)[0][0]

print(ID_t, ID_i, ID_l)
colours = torch.zeros((N))
colours[ID_t] = 1
colours[ID_i] = 1
colours[ID_l] = 1

#STEP 6: COMPUTE PATH

#STEP 7: COMPUTE PHASES

#STEP 8: RENDER HAPTICS 

Visualise_mesh(hand,colours ,equalise_axis=True)
