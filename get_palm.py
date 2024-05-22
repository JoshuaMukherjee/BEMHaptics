from acoustools.Mesh import load_scatterer , centre_scatterer, scatterer_file_name
import acoustools.Constants as c
from acoustools.Visualiser import Visualise_mesh


import numpy as np
import json
import vedo
import torch

HAND_ID = 'participant_999999999'
METADATA_PATH = './Media/Metadata/'+ HAND_ID + '_metadata.json'
HAND_PATH = './Media/Hands/'+ HAND_ID + '.obj'

hand_origional = load_scatterer(HAND_PATH)
correction = centre_scatterer(hand_origional)

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


metadata = json.load(open(METADATA_PATH))
palm_position_uncorrected = metadata['Hand']['PalmPosition']
palm_position= [palm_position_uncorrected[i] + correction[i] for i in [0,1,2]]

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

Visualise_mesh(hand, colours, equalise_axis=True)
