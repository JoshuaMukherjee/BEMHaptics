import os, pickle
from acoustools.Mesh import load_scatterer, get_edge_data

import matplotlib.pyplot as plt

total_distance = 0
N = 0

maxs = []
mins = []
aves = []
sums = []

compute = False
if compute:
    for pth in os.listdir('HapticsGUI\Media\Hands'):
        m = load_scatterer(f'HapticsGUI\Media\Hands\{pth}')
        (max_distance, min_distance, average_distance), (distance_sum, n) = get_edge_data(m, break_down_average=True, print_output=False)
        total_distance += distance_sum
        N += n

        maxs.append(max_distance)
        mins.append(min_distance)
        aves.append(average_distance)
        sums.append((distance_sum, n))

        print('.',end='',flush=True)

    print(total_distance/N)

    pickle.dump([maxs, mins, aves, sums], open('edge_data.pth', 'wb'))

maxs, mins, aves, sums = pickle.load(open('edge_data.pth', 'rb'))

plt.boxplot(aves,vert=False)
plt.show()