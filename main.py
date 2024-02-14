#main.py
#import matplotlib.pyplot as plt

import skimage as ski 
import sys
import matplotlib.pyplot as plt


THRESHOLD = 200
RED = [180,0,0]
init = [[63,541,3]]
end = [63,1500]
steps = [init]

def test_int(point):
    point = im[point[0],point[1]]
    if any(i>=THRESHOLD for i in point):
        return 1
    else :
        return 0
    
def move_dir(point,dir):
    
    if(dir == 1):
        x = point[0]
        y = point[1]-1
    if(dir == 2):
        x = point[0]+1
        y = point[1]
    if(dir == 3):
        x = point[0]
        y = point[1]+1
    if(dir == 4):
        x = point[0]-1
        y = point[1]
    return [x,y]

def find_next(current):
    dirs = []
    for i in range(1,5):
        next = move_dir(current,i)
        if(test_int(next)):
            dirs.extend([i])
    return dirs

    
im = ski.io.imread('maze.jpg')
im_or = im.copy()
#ski.io.imshow(im)
#ski.io.show()
last = steps[0][-1]
im[last[0],last[1]] = RED

found = 0
n = 0
while(not found):
    
    #We take the last steps of the first chain
    last = steps[0][-1]
    #We move to the new one and paint it
    current = move_dir(last,last[2])
    im[current[0],current[1]] = RED
    #We are on the target point
    if(current == end):
        found = 1
        print("found !")
        chain = steps[0]
        for i in range(0,len(chain)):
            im_or[chain[i][0],chain[i][1]] = RED
        ski.io.imshow(im_or)
        ski.io.show()

    #We are not on the target point
    else:
        n=n+1
        if(n%10000 == 1):
            print(n)
            print(len(steps))
            print(current)
        #if(n%50000 == 1):
            #plt.imshow(im)
            #plt.ion()
            #plt.show()
            #plt.pause(1)
        #We find points around that are white, these are the new directions
        dirs = find_next(current)
        #print(dirs)
        #No new point, it's a dead end
        if(len(dirs)==0):
            #We remove this chain, next time we'll try the next one
            del steps[0]
        #Only one new point, we add the new step    
        if(len(dirs)==1):
            steps[0].append([current[0],current[1],dirs[0]])
            
        #More new directions, we add the new step and create extra chains.
        if(len(dirs)==2):
            new_1 = steps[0].copy()
            steps[0].append([current[0],current[1],dirs[0]]) 
            new_1.append([current[0],current[1],dirs[1]])
            steps.append(new_1)

        if(len(dirs)==3):
            new_1 = steps[0].copy()
            new_2 = steps[0].copy() 
            steps[0].append([current[0],current[1],dirs[0]]) 
            new_1.append([current[0],current[1],dirs[1]])
            steps.append(new_1)
            new_2.append([current[0],current[1],dirs[2]])
            steps.append(new_2)
        #print(steps)
        
        




