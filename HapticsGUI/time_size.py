import os, pickle
from acoustools.Mesh import load_scatterer, get_edge_data

import matplotlib.pyplot as plt


aves = []
times = []

compute = False
if compute:
    for pth in os.listdir('HapticsGUI\Media\Hands'):   
        try:
            time_pth = 'HapticsGUI\Media\Times\\times_' + pth.replace('Participant_','').replace('.obj','')
            t = pickle.load(open(time_pth,'rb'))
            time = (t[-1]-t[2])/1e9

            m = load_scatterer(f'HapticsGUI\Media\Hands\{pth}')
            (max_distance, min_distance, average_distance), (distance_sum, n) = get_edge_data(m, break_down_average=True, print_output=False)

            aves.append(average_distance)
            times.append(time)

           
        except:
            print(pth) 
    
    pickle.dump([aves,times], open('time_size.pth', 'wb'))

aves,times = pickle.load(open('time_size.pth', 'rb'))
plt.scatter(aves, times)
plt.show()