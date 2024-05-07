from acoustools.Mesh import load_scatterer, get_centres_as_points, scatterer_file_name
import acoustools.Constants as c
from acoustools.Visualiser import Visualise_mesh, Visualise
from acoustools.BEM import get_cache_or_compute_H, compute_E, propagate_BEM_pressure
from acoustools.Utilities import BOTTOM_BOARD, create_points
from acoustools.Solvers import wgs

import torch


hand_origional = load_scatterer('Media/ExportedMesh1.stl',dx=0.072, dy=-2.53,dz=-0.47+0.03)
# hand_origional = load_scatterer('Media/Sphere-lam2.stl',dy=-0.06,dz=0.04)


hand = hand_origional.clean()
print(hand.is_closed())


com = hand.center_of_mass()
p = hand.intersect_with_line([com[0], com[1],com[2]+1],[com[0], com[1],com[2]-1])[0]
print(p)


p = create_points(1,1,x=p[0],y=p[1],z=p[2]-0.015)
# p = create_points(1,1,-0.082,-0.017,0.0434)

hand.subdivide(2)
hand.filename = scatterer_file_name(hand)

H = get_cache_or_compute_H(hand, board=BOTTOM_BOARD)
E = compute_E(hand,points=p, board=BOTTOM_BOARD)

x = wgs(p,A=E)
pressure = torch.abs(H@x)
# print(pressure)

p_pressure = torch.abs(E@x)
print(p_pressure)



A = torch.tensor((-0.12,0, 0.12))
B = torch.tensor((0.12,0, 0.12))
C = torch.tensor((-0.12,0, -0.12))
normal = (0,1,0)
origin = (0,0,0)

Visualise(A,B,C, x, points=p,vmax=5000,colour_functions=[propagate_BEM_pressure], colour_function_args=[{'scatterer':hand,'board':BOTTOM_BOARD}],clr_label="Pressure (Pa)")




# Visualise_mesh(hand, pressure.flatten(), points=p, p_pressure=p_pressure,vmax=7000)
