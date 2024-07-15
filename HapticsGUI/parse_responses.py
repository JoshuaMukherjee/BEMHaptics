import sys
import os

path = sys.argv[1]


with open('responses.csv','w') as response_file:
    for fname in os.listdir(path):
        part_id = fname.split('_')[0]
        index = fname.split('_')[1].split('.')[0]
        with open(path+'/'+fname,'r') as f:
            res = f.readlines()
            response_file.write(part_id + ',')
            response_file.write(index)
            for r in res:
                response_file.write(',')
                response_file.write(r.rstrip())
            response_file.write('\n')
