#Vasileios Gewrgoulas
#AM 2954


nodes = ''
edges = ''
graph = ''
struct = []


def build():
    global nodes, edges, struct

    node = nodes.readline().rstrip("\n").split()
    while node:
        n = [int(node[0]), [float(node[1]), float(node[2])], []]         
        struct.append(n)
        node = nodes.readline().rstrip("\n").split()

    e = edges.readline().rstrip("\n").split()
    while e:
        struct[int(e[1])][2].append((int(e[2]), float(e[3])))
        struct[int(e[2])][2].append((int(e[1]), float(e[3])))
        e = edges.readline().rstrip("\n").split()

#############3#main#################3

try:
    nodes = open('nodes.txt', 'r')
    edges = open('edges.txt', 'r')
    graph = open('out.txt' , 'w')
except:
    graph.close()
    edges.close()
    nodes.close()
    exit(1)

build()

for s in struct:
   graph.write(str(s) + '\n')
graph.close()
edges.close()
nodes.close()
