#Vasileios Gewrgoulas
#AM 2954

import sys
import heapq
import ast
import itertools

minDist = pow(2, 30)
counter = itertools.count()

graph = ''
struct = []
pqs = []
dicts = []
spds = []
paths = []
bounds = []
visited = []

LBq = []
bests = {}

found = False

best = None
idIndex = {}

def addNode(nId, dist, s):
    global pqs, dicts, counter

    if dicts[s].get(nId):
        removeNode(nId, s)
    count = next(counter)
    e = [dist, count, nId]
    dicts[s][nId] = e
    heapq.heappush(pqs[s], e)
            
def removeNode(nId, s):
    global dicts

    e = dicts[s].pop(nId)
    e[-1] = 'removed'

def popNode(s):
    global pqs, dicts

    while pqs[s]:
        e = heapq.heappop(pqs[s])
        if e[-1] != 'removed':
            del dicts[s][e[-1]]
            return e
    return 'done'

#####################################################################################################33

def checkBest():
    global found, best, bests, LBq, bounds

    if best is None:
        return

    v = LBq[0]
    while bests.get(v[1]) and LBq:
        heapq.heappop(LBq)
        if LBq:
            v = LBq[0]

    if not LBq:
        return

    if v[0] > bounds[best][1]:
        print('stoped by condition\n')
        found = True
        
def updateBest(nId):
    global best, bounds

    bests[nId] = True

    if best is None:
        best = nId
    elif bounds[best][1] > bounds[nId][1]:
        best = nId
    
def Dijkstra(ni):  #continue dijkstra from ni
    global spds, paths, idIndex, visited

    i = idIndex[ni]
    v = popNode(i)

    if v == 'done':
        return 'done'
    
    visited[i][v[2]] = 1
    for u in struct[v[2]][2]:
        if not visited[i][u[0]]:
            if spds[i][u[0]] > spds[i][v[2]] + u[1]:
                spds[i][u[0]] = spds[i][v[2]] + u[1]
                paths[i][u[0]] = str(paths[i][v[2]]) + '->' + str(u[0])
                addNode(u[0], spds[i][u[0]], i)
    return v

def NRA(ids):
    global pqs, bounds, spds, paths, dicts, idIndex, found, LBq, visited

    j = 0
    for i in range(0, len(ids)):
        if idIndex.get(ids[i]) is None:
            idIndex[ids[i]] = j
            j += 1

    t = len(idIndex)
    bounds = [[minDist, 0] for i in range(0, len(struct))]
    spds = [[minDist for i in range(0, len(struct))] for j in range(0, t)]
    paths = [[None for i in range(0, len(struct))] for j in range(0, t)]
    dicts = [{} for i in range(0, t)]
    pqs = [[] for j in range(0, t)]
    visited = [[0 for i in range(0, len(struct))] for j in range(0, t)]
    
    j = 0
    for key in idIndex:
        spds[j][key] = 0
        paths[j][key] = key
        addNode(key, 0, j)
        j += 1

    if t == 1:
        updateBest(pqs[0][0][-1])
        return

    while not found:
        for key in idIndex:
            v = Dijkstra(key)  

            if v == 'done':
                return

            if v[0] < bounds[v[2]][0]:
                bounds[v[2]][0] = v[0]
                
            heapq.heappush(LBq, (bounds[v[2]][0], v[2]))
            maxD = max([spds[k][v[2]] for k in range(0, t)])
            bounds[v[2]][1] = maxD

            if maxD < minDist: #found another candidate
                updateBest(v[2])        
        checkBest()

#############3#main#################

ids = []
try:
    graph = open('out.txt', 'r')
    ids = [int(sys.argv[i]) for i in range(1, len(sys.argv))]
except:
    graph.close()
    exit(1)

e = graph.readline().rstrip("\n")
while e:
    struct.append(ast.literal_eval(e))
    e = graph.readline().rstrip("\n")
graph.close()

NRA(ids)

if best is None:
    print('meeting point doesnt exist')
else:
    print('The optimal meeting point is: ', best)
    print('Shortest path distance: ', bounds[best][1])
    print('paths')
    for i in range(0 , len(idIndex)):
        result = [spds[i][best], paths[i][best]]
        print(result)
        print()
        
