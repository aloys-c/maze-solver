#main.py

import skimage as ski 
import matplotlib.pyplot as plt
import time
start_time = time.time()


imin = './mazes/maze8.jpg'
imout = './results/result8.jpg'
init = [60,545] #y,x
end = [[60,1505]] 
COLORING_WIDTH =2

ITER_SHOW = 100000
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
id_n = 0
chains = {id_n:{"prev":-1,"next":0,"chain":[init]}}

found = 0
n = 0
active_chains = [id_n]
current = chains[id_n].get("chain")[-1]
im[current[0],current[1]] = RED


while(not found):

    for i in range(len(active_chains)-1,-1,-1):

        #We take the last chain of the active chains
        id_i = active_chains[i]

        current = chains[id_i].get("chain")[-1]
        #We are on the target point, let's print the path
        if(current in end):
            print("--- %s seconds ---" % (time.time() - start_time))
            found = 1
            print("Found :")
            prev_id = id_i
            chain = []
            while(not prev_id == -1):
                chain = chains[prev_id].get('chain') + chain 
                prev_id = chains[prev_id].get('prev')
            
            print("Iterations: "+str(n))
            print("Chain length: "+str(len(chain))+"\n")
            im = im_or.copy()
            color_path(chain)
            print("--- %s seconds ---" % (time.time() - start_time))
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
                print("Current chains: "+str(len(chains))+"\n")
                print("active chains: "+str(len(active_chains))+"\n")
            if(n%ITER_SHOW == 1):
                plt.imshow(im)
                plt.ion()
                plt.show()
                plt.pause(0.5)

            #We find points around that are white, these are the new directions
            nexts = find_next(current)
            #No new point, it's a dead end
            if(len(nexts)==0):
                #We remove this chain, and also the parent unused ones
                del active_chains[i]
                prev_id = id_i
                next = 0
                while(not next):
                    id_i = prev_id
                    prev_id = chains[id_i].get('prev')
                    del chains[id_i]
                    
                    chains[prev_id]['next'] -=1
                    next = chains[prev_id]['next']
                           

            #Only one new point, we add the new step    
            if(len(nexts)==1):
                chains[id_i]['chain'].append(nexts[0])
                
            #More new directions, we fork in new chains.
            if(len(nexts)==2):

                chains[id_i]["next"]+=2
                id_n +=1 
                chains[id_n] = {"prev":id_i,"next":0,"chain":[nexts[0]]} 
                active_chains.append(id_n)
                id_n +=1
                chains[id_n] = {"prev":id_i,"next":0,"chain":[nexts[1]]} 
                active_chains.append(id_n)
                del active_chains[i]
                
            if(len(nexts)>2): #Not only 3 to take into account the first iteration

                chains[id_i]["next"]+=3
                id_n +=1 
                chains[id_n] = {"prev":id_i,"next":0,"chain":[nexts[0]]} 
                active_chains.append(id_n)
                id_n +=1
                chains[id_n] = {"prev":id_i,"next":0,"chain":[nexts[1]]} 
                active_chains.append(id_n)
                id_n +=1
                chains[id_n] = {"prev":id_i,"next":0,"chain":[nexts[2]]} 
                active_chains.append(id_n)
                del active_chains[i]
               

       
        
        




