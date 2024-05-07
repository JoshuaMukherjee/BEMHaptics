from acoustools.Mesh import load_scatterer, get_centres_as_points, scatterer_file_name
import acoustools.Constants as c
from acoustools.Visualiser import Visualise_mesh, Visualise
from acoustools.BEM import get_cache_or_compute_H, compute_E, propagate_BEM_pressure
from acoustools.Utilities import BOTTOM_BOARD, create_points, propagate, forward_model
from acoustools.Solvers import wgs, gradient_descent_solver

import torch, os, vedo, numpy

import matplotlib.pyplot as plt



hand_origional = load_scatterer('Media/ExportedMesh1.obj',dx=0.072, dy=-2.53,dz=-0.47+0.03)
# hand_origional = load_scatterer('Media/Sphere-lam2.stl',dy=-0.06,dz=0.04)


hand = hand_origional.clean()
print(hand.is_closed())



# p = create_points(1,1,-0.082,-0.017,0.0434)

hand.subdivide(2)
hand.filename = scatterer_file_name(hand)

hand.compute_cell_size()
print(hand.celldata['Area'])

com = hand.center_of_mass()
print(com)
# p = hand.intersect_with_line([com[0], com[1],com[2]+1],[com[0], com[1],com[2]-1])[1]
p = hand.intersect_with_line([-0.025, -0.025,1],[-0.025, -0.025,-1])[1]

centres = hand.cell_centers
_, centre = vedo.closest(p, centres)
ID = numpy.where(centre==centres)[0][0]
print(ID)


print(centre)
# exit()

# vedo.show(hand,vedo.Point(p),axes=1)
# exit()

p = create_points(1,1,x=centre[0],y=centre[1],z=centre[2])


# centres = get_centres_as_points(hand)

# ps = get_centres_as_points(hand)
# p = ps[:,:,ID].unsqueeze_(2).to(torch.float64)
# print(p)

print(hand)

print('Compute Matricies...')
H = get_cache_or_compute_H(hand, board=BOTTOM_BOARD)
E = compute_E(hand,points=p, board=BOTTOM_BOARD,H=H)
print('Computed')

print(E.shape)
# prop = H[:,ID,:].unsqueeze(1)
# print(prop.shape)
x = wgs(p,A=E, board = BOTTOM_BOARD, iter=500)
print(x.shape)

print('Plotting...')

pressure = torch.abs(H@x)
# pressure[:,ID] = 1000000
print(pressure[:,ID])

p_pressure = torch.abs(E@x)
print(p_pressure)

centres = get_centres_as_points(hand)
E_centres = compute_E(hand,centres,BOTTOM_BOARD, H=H)
F_centres = forward_model(centres,BOTTOM_BOARD)
pressure_E = torch.abs(E_centres@x)
pressure_F = torch.abs(F_centres@x)


A = torch.tensor((-0.12,-0.025, 0.12))
B = torch.tensor((0.12,-0.025, 0.12))
C = torch.tensor((-0.12,-0.025, -0.12))
normal = (0,1,0)
origin = (0,0,0)

# Visualise(A,B,C, x, points=p,vmax=5000,colour_function_args=[{'board':BOTTOM_BOARD}])



fig = plt.figure()
ax =  Visualise_mesh(hand, pressure_E.flatten(), points=p, show=False, subplot=121, fig=fig, vmax=4000)
ax2 = Visualise_mesh(hand, pressure_F.flatten(), points=p, show=False, subplot=122, fig=fig, vmax = 4000)

def update_view(event):
    if event.name == 'button_press_event' and event.inaxes == ax:
        ax2.view_init(elev=ax.elev, azim=ax.azim)

# Connect the event handler
fig.canvas.mpl_connect('button_press_event', update_view)


plt.show()
