# By Lucas Rosvall, MPHPC

import sys
import os.path
import pandas as pd
from math import sqrt, pow

#threshold distance between alpha carbons
threshold = 4;

def get_neighbors(file):
    data = pd.read_csv(file, sep='\t', header=None)
    closest_pairs = {}
    for i, row in data.iterrows():
        current_i = data.iloc[:, 0][i]
        neighbors = []
        parsed_row = row[1].split(' ')
        
        x1 = float(parsed_row[0])
        y1 = float(parsed_row[1])
        z1 = float(parsed_row[2])
        
        for j,row in data.iterrows():
            current_j = data.iloc[:, 0][j]
            if current_j != current_i: #skip if the same
                parsed_row = row[1].split(' ')
                x2 = float(parsed_row[0])
                y2 = float(parsed_row[1])
                z2 = float(parsed_row[2])

                # calculate distance
                distance = sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2) + pow((z2 - z1), 2))

                if(distance > 3.6 and distance < threshold):
                    neighbors.append(current_j)

        closest_pairs[current_i] = neighbors
    return closest_pairs

def dynamaic(pairs,node,chain):
    allChains = []
    if(len(pairs[node]) > 0):
        next_nodes = pairs[node]
        chain.append(node)
        for next in next_nodes:
            if(node in pairs[next]):
                pairs[next].remove(node) #remove the previous value
                return dynamaic(pairs,next,chain)
    else:
        return chain

def print_chain(pairs):
    length = len(pairs)

    startnodes = []

    #find the beginning/end of the chain
    for pair in pairs:
        if(len(pairs[pair]) == 1):
            startnodes.append(pair)
 

    for node in startnodes:
        res = dynamaic(pairs,node,[])
        if(isinstance(res,list)):
            print(res)
        

    #loop though and print the chain

    return


filename = sys.argv[1]

if(os.path.isfile(filename)):
    #get closest neighbors
    pairs = get_neighbors(filename)
    #find and print the chain
    print_chain(pairs)
else:
    print("Error! Input file does not exist!")
