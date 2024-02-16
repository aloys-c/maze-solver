#main.py

import skimage as ski 
import matplotlib.pyplot as plt


imin = './mazes/maze8.jpg'
imout = './results/result8.jpg'
init = [100,120] #y,x
end = [[618,326]] 
COLORING_WIDTH =2

ITER_SHOW = 10000
THRESHOLD = 200
COLOR_THRESHOLD = 170
RED = [180,0,0]


def test_int(point):
    point = im[point[0],point[1]]
    if any(i>=THRESHOLD for i in point):
        return 1
    else:
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
    nexts = []
    for i in range(1,5):
        next = move_dir(current,i)
        if(test_int(next)):
            nexts.append(next)
            im[next[0],next[1]] = RED
    return nexts

def color_path(chain):
    global THRESHOLD
    THRESHOLD = COLOR_THRESHOLD
    for pos in chain:
        for i in range(1,5):
            border = False
            current = pos.copy()
            k = 0
            while((not border) and k<=COLORING_WIDTH):
                im[current[0],current[1]] = RED
                next = move_dir(current,i)
                if(test_int(next)):
                    current = next
                    k = k+1
                else:
                    border = True


im = ski.io.imread(imin)
im_or = im.copy()
steps = [[init]]
last = steps[0][-1]
im[last[0],last[1]] = RED

found = 0
n = 0
while(not found):
    
        for i in range(len(steps)-1,-1,-1):
            #We take the last steps of the current chain
            
            current = steps[i][-1]
            #We are on the target point
            if(current in end):
                found = 1
                print("Found :")
                chain = steps[i]
                print("Iterations: "+str(n))
                print("Chain length: "+str(len(chain))+"\n")
                im = im_or.copy()
                color_path(chain)
                
                ski.io.imsave(imout,im)
                plt.ioff()
                plt.imshow(im)
                plt.show()
                break

            #We are not on the target point
            else:
                n=n+1
                if(n%10000 == 1):
                    print("Iterations: "+str(n-1))
                    print("Current chains: "+str(len(steps))+"\n")
                if(n%ITER_SHOW == 1):
                    plt.imshow(im)
                    plt.ion()
                    plt.show()
                    plt.pause(0.5)
                #We find points around that are white, these are the new directions
                nexts = find_next(current)
                #No new point, it's a dead end
                if(len(nexts)==0):
                    #We remove this chain, next time we'll try the next one
                    del steps[i]
                
                #Only one new point, we add the new step    
                if(len(nexts)==1):
                    steps[i].append(nexts[0])
                    
                #More new directions, we add the new step and create extra chains.
                if(len(nexts)==2):
                    new_1 = steps[i].copy()
                    steps[i].append(nexts[0]) 
                    new_1.append(nexts[1])
                    steps.append(new_1)

                if(len(nexts)>2):
                    new_1 = steps[i].copy()
                    new_2 = steps[i].copy() 
                    steps[i].append(nexts[0]) 
                    new_1.append(nexts[1])
                    steps.append(new_1)
                    new_2.append(nexts[2])
                    steps.append(new_2)
        
       
       
        
        




