from acoustools.Mesh import centre_scatterer, load_scatterer, scatterer_file_name
from acoustools.Paths import get_numeral, interpolate_path
from acoustools.Solvers import wgs
from acoustools.BEM import compute_E, get_cache_or_compute_H
from acoustools.Utilities import BOTTOM_BOARD, create_points
from acoustools.Levitator import LevitatorController
import vedo
import numpy as np
import json
import torch
import time
import socket
import random
import os



def get_hand_to_path(participant_id, path):
    SAMPLE_FRACTION = 0.65
    ITERATIONS = 5

    with torch.no_grad():

        def get_best_position(intersections, centres, normals, index_pos):
            possible_points = []
            for p in intersections:
                _, closest_centre_ids = vedo.closest(p, centres, return_ids =True)
                normal = normals[closest_centre_ids]
                if normal[2] < 0 :
                    possible_points.append(p)
                
            if len(possible_points) == 0:
                return []
            if len(possible_points) == 1:
                return possible_points[0]
            else:
                min_dist = 0
                best_p = None
                for p in possible_points:
                    dist_z = (p[2] - index_pos[2])**2
                    if dist_z < min_dist:
                        best_p = p
                        min_dist = dist_z
                return best_p


        def rescale_ABC(A,B,C, factor=1):
            AB = B-A
            AC = C-A
            
            B = A + (factor) * AB + (1-factor)*AC
            C = A + (1-factor) * AB + (factor)*AC
            A = A + (1-factor) * AB + (1-factor)*AC

            return A,B,C
            

        #STEP 1: GET HAND FROM UNITY

        def get_hand_from_unity(host, port, message):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            client_socket.sendall(message.encode('utf-8'))
            client_socket.close()
        
        init_time = time.monotonic_ns()


        host = '127.0.0.1'  # Localhost
        port = 9999         # Port number should match the Unity server port

        # input("Press enter when hand in position")

        start_time = time.monotonic_ns()

        HAND_ID = 'Participant_' + participant_id
        print(HAND_ID)
        get_hand_from_unity(host, port,HAND_ID)

        #STEP 2: LOAD MESH

        MAX_WAIT = 100000000
        waits = 0
        METADATA_PATH = path + 'Metadata/' + HAND_ID + '_metadata.json'
        print(METADATA_PATH)
        while not os.path.isfile(METADATA_PATH) and waits < MAX_WAIT:
            waits -= 1

        print('Got Hand')
        get_hand_time = time.monotonic_ns()

        HAND_HIEGHT = 0.06
        HAND_PATH = path + 'Hands/' + HAND_ID + '.obj'
        hand_origional = load_scatterer(HAND_PATH) # SOLVE CRASH WHEN HAND NOT FOUND
        h = hand_origional.clone()

        correction = centre_scatterer(hand_origional)

        corrected_hand_time = time.monotonic_ns()

        #STEP 3: PROCESS MESH
        
        hand = hand_origional.clean().smooth()
        

        # hand.collapse_edges(c.wavelength/2)
        # hand.filename = scatterer_file_name(hand)

        edges = hand.count_vertices()
        mask = np.where(edges != 3)[0]
        hand.delete_cells(mask)
        hand.filename = scatterer_file_name(hand)


        hand.subdivide(2)        
        hand = hand.decimate(SAMPLE_FRACTION)
        
        hand.compute_normals()
        hand = hand.reverse(cells=True, normals=True)

        hand.compute_cell_size()
        hand.filename = scatterer_file_name(hand)

        process_mesh_time = time.monotonic_ns()

        #STEP 4: LOAD METADATA

        metadata = json.load(open(METADATA_PATH))

        metadata_laod_tome = time.monotonic_ns()

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

        _, centre_i = vedo.closest(index, centres)

        _, centre_l = vedo.closest(little, centres)

        find_corners_time = time.monotonic_ns()

        #STEP 6: COMPUTE PATH

        number = random.randint(1,9)


        # print(number)
        A,B,C = rescale_ABC(centre_i, centre_l, centre_t, factor=0.9)
        path = get_numeral(number, A,B,C) #COME BACK - CAN LEAD TO NUMBER OFF THE HAND. MAYBE SCALE BOX?
        path = interpolate_path(path, 200)

        compute_path_time = time.monotonic_ns()

        #STEP 7: MAP TO HAND

        DELTA = 0.05
        lines_points = [((x,y,z-DELTA),(x,y,z+DELTA)) for (x,y,z) in path]
        lines = [[p0,p1] for (p0, p1) in lines_points]


        intersections = [hand.intersect_with_line(p0,p1) for (p0, p1) in lines_points ]
        best_ps = [get_best_position(inter, centres, hand.cell_normals, centre_i) for inter in intersections]

        best_point_time = time.monotonic_ns()

        #STEP 8: COMPUTE PHASES


        board = BOTTOM_BOARD
        H = get_cache_or_compute_H(hand, board, use_LU=True)

        compute_H_time = time.monotonic_ns()

   
        holograms = []
        bem = random.choice([0,1])

        for p in best_ps:
            if len(p) > 0:
                p = create_points(1,1,x=p[0],y=p[1],z=p[2])
                if bem:
                    E = compute_E(hand, p, board, H=H)
                    x = wgs(p, board=board, A=E, iter=ITERATIONS) #BEM
                else:
                    x = wgs(p, board=board, iter=ITERATIONS) # Piston Model
                holograms.append(x)


        compute_holograms_time = time.monotonic_ns()

        times = [init_time, start_time, get_hand_time, corrected_hand_time, process_mesh_time, metadata_laod_tome, find_corners_time, compute_path_time, best_point_time, compute_H_time, compute_holograms_time]

        return holograms, times, number, bem