#Vasileios Gewrgoulas
#AM 2954

import heapq
import math
import ast
import itertools
import sys

minDist = pow(2, 30)
counter = itertools.count()

graph = ''
struct = []
q = []
dictIndex = {}

def euc(s, e):
    return math.sqrt(pow(s[0] - e[0], 2) + pow(s[1] - e[1], 2))

################################queue manipulation###############################

def addNode(nId, dist):
    global q, dictIndex, counter

    if dictIndex.get(nId):
        removeNode(nId)
    count = next(counter)
    e = [dist, count, nId]
    dictIndex[nId] = e
    heapq.heappush(q, e)
        
def removeNode(nId):
    global dictIndex

    e = dictIndex.pop(nId)
    e[-1] = 'removed'

def popNode():
    global dictIndex, q

    while q:
        e = heapq.heappop(q)
        if e[-1] != 'removed':
            del dictIndex[e[-1]]
            return e
    return 'done'

######################################################################

def Dijstra(s, t):
    global struct, minDist, dictIndex, q

    spd = []
    path = []
    
    for v in struct:
        spd.append(minDist)
        path.append(None)
        v.append(False)
    q = []
    dictIndex = {}

    spd[s] = 0
    path[s] = str(s)
    addNode(s, spd[s])
    
    iterations = 0
    while q:
        v = popNode()
        struct[v[2]][-1] = True
        iterations += 1

        if v == 'done':
            return 'done'
        
        if t == v[2]:
            return (spd[t], path[t], iterations)
        for u in struct[v[2]][2]:
            if not struct[u[0]][-1]:
                if spd[u[0]] > spd[v[2]] + u[1]:
                    spd[u[0]] = spd[v[2]] + u[1]
                    path[u[0]] = str(path[v[2]]) + '->' + str(u[0])
                    addNode(u[0], spd[u[0]])
    return 'done'

def Astar(s, t):
    global struct, minDist, dictIndex, q

    spd = []
    path = []
    
    for v in struct:
        spd.append(minDist)
        path.append(None)
        v.append(False)
    q = []
    dictIndex = {}

    spd[s] = 0
    path[s] = str(s)
    addNode(s, spd[s] + euc(struct[s][1], struct[t][1]))
    
    iterations = 0
    while q:

        v = popNode()
        struct[v[2]][-1] = True
        iterations += 1

        if v == 'done':
            return 'done'

        if t == v[2]:
            return (spd[t], path[t] ,iterations)
        for u in struct[v[2]][2]:
            if not struct[u[0]][-1]:
                if spd[u[0]] > spd[v[2]] + u[1]:
                    spd[u[0]] = spd[v[2]] + u[1]
                    path[u[0]] = str(path[v[2]]) + '->' + str(u[0])
                    d = euc(struct[u[0]][1], struct[t][1])
                    addNode(u[0], spd[u[0]] + d)
    return 'done'

#############3#main#################3

points = []
try:
    graph = open('out.txt', 'r')
    points = [int(sys.argv[i]) for i in range(1, len(sys.argv))]
except:
    graph.close()
    exit(1)

e = graph.readline().rstrip("\n")
while e:
    struct.append(ast.literal_eval(e))
    e = graph.readline().rstrip("\n")
graph.close()

dijkstra = Dijstra(points[0], points[1])

if dijkstra == 'done':
    print('not connected')
    exit(1)

astar = Astar(points[0], points[1])

print('\nDijkstra results: ')
print('distance to node %s is: %s' % (points[1], dijkstra[0]))
print('total visits: ' , dijkstra[2])
print('path: ', dijkstra[1])
print('path length: ', len(dijkstra[1].split('->')))

print('\nA* results: ')
print('distance to node %s is: %s' % (points[1], astar[0]))
print('total visits: ' , astar[2])
print('path: ', astar[1])
print('path length: ', len(astar[1].split('->')))
