# 119319353
import time

class Vertex:
    """ A Vertex in a graph. """
    
    def __init__(self, element):
        """ Create a vertex, with a data element.

        Args:
            element - the data or label to be associated with the vertex
        """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        """ Return true if this element is less than v's element.

        Args:
            v - a vertex object
        """
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element
    
    
class Edge:
    """ An edge in a graph.

        Implemented with an order, so can be used for directed or undirected
        graphs. Methods are provided for both. It is the job of the Graph class
        to handle them as directed or undirected.
    """
    
    def __init__(self, v, w, cost, element=None):
        """ Create an edge between vertices v and w, with a data element.

        Element can be an arbitrarily complex structure.

        Args:
            element - the data or label to be associated with the edge.
        """
        self._vertices = (v,w)
        self._cost = cost
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        retstr = '(' + str(self._vertices[0]) + '--' + str(self._vertices[1]) + ' costs ' + str(self._cost)
        if self._element != None:
            retstr +=  + ', elem: ' + str(self._element)
        retstr += ')'
        return retstr

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge.

        Args:
            v - a vertex object
        """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def cost(self):
        """ Return the cost for this edge. """
        return self._cost

    def element(self):
        """ Return the data element for this edge. """
        return self._element


class Graph:
    """ Represent a simple graph.

    This version maintains directed graphs.

    Implements the Adjacency Map style. Also maintains a top level
    dictionary of vertices.
    """

    #   Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the sets of edges for the corresponding vertex.
    #    Each edge set is also maintained as a dictionary,
    #    with the opposite vertex as the key and the edge object as the value.
    
    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr
    
    #-----------------------------------------------------------------------#

    # ADT methods to query the graph
    
    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for e in self.edges():
            num += 1
        return num

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                # #to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v.

        Args:
            v - a vertex object
        """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None.

        Args:
            v - a vertex object
            w - a vertex object
        """
        if (self._structure is not None
                         and v in self._structure):
            for k in self._structure[v]:
                if k[0] == w:
                    return self._structure[v][k]
        return None

    def degree(self, v):
        """ Return the degree of vertex v.

        Args:
            v - a vertex object
        """
        return len(self._structure[v])

    
    #----------------------------------------------------------------------#

    # ADT methods to modify the graph
    
    def add_vertex(self, element):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

        Checks for equality between the elements. If there is special
        meaning to parts of the element (e.g. element is a tuple, with an
        'id' in cell 0), then this method may create multiple vertices with
        the same 'id' if any other parts of element are different.

        To ensure vertices are unique for individual parts of element,
        separate methods need to be written.

        """
        for v in self._structure:
            if v.element() == element:
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element, oneway=False):
        """ Add and return an edge between two vertices v and w, with  element.

        If either v or w are not vertices in the graph, does not add, and
        returns None.
            
        If an edge already exists between v and w, this will
        replace the previous edge.

        Args:
            v - a vertex object
            w - a vertex object
            element - a label
        """
        if v not in self._structure or w not in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][(w, element)] = e
        if not oneway:
            self._structure[w][(v, element)] = e
        return e, oneway

    #---------------------------------------------------------------------#

    # Implementing Dijkstra's algorithm

    def dijkstra(self,s):
        '''

        '''
        open_pq = APQ()
        locs = dict()
        closed = dict()
        preds = {s:None}

        v = open_pq.add(0, s)
        locs[s] = v

        while not open_pq.is_empty():
            cost, v = open_pq.remove_min()
            locs.pop(v)
            pred = preds.pop(v)
            closed[v] = (cost, pred)
            for e in self.get_edges(v):
                w = e.opposite(v)
                if w not in closed:
                    newcost = cost + e.cost()
                    if w not in locs:
                        preds[w] = v
                        elem = open_pq.add(newcost, w)
                        locs[w] = elem
                    elif newcost < open_pq.get_key(w):
                        oldcost = open_pq.get_key(w)
                        open_pq.update_key(w, newcost)
                        preds[w] = v
        return closed


class APQ:
    def __init__(self):
        '''
        initialises an empty priority queue
        '''
        self._queue = []

    def __str__(self):
        retstr = '['
        for elem in self._queue:
            retstr += elem.__str__() + ', '
        retstr += ']'
        return retstr

    def add(self,key,value):
        '''
        add a new item into the priority queue with priority key, and return its Element
        in the APQ
        '''
        elem = Element(key, value, self.length())
        self._queue.append(elem)
        if self.length() > 1:
            self._add(elem,self.length()-1)
        return elem

    def _add(self,elem,i):
        '''
        rebalance heap when bubbling up the tree
        '''
        parent = (i-1)//2
        while self._queue[i] < self._queue[parent]:
            self._queue[parent], self._queue[i] = self._queue[i], self._queue[parent]
            elem.setIndex(parent)
            self._queue[i].setIndex(i)
            i = parent
            if i <= 0:
                break
            parent = (i-1)//2

    def min(self):
        '''
        return the value with the minimum key
        '''
        if len(self._queue) > 0:
            return self._queue[0]
        return None

    def remove_min(self):
        '''
        remove and return the value with the minimum key
        '''
        element = self._queue[0]
        return self.remove(element)
                
    def _remove(self, current, last):
        '''
        Rebalance heap when bubbling element down tree
        '''
        if current == last:
            return 0

        lchild = (2*current)+1
        rchild = (2*current)+2

        if lchild > last:
            return 0
        elif rchild > last or self._queue[lchild] < self._queue[rchild]:
            if self._queue[current] > self._queue[lchild]:
                self._queue[current], self._queue[lchild] = self._queue[lchild], self._queue[current]
                self._queue[lchild].setIndex(lchild)
                self._queue[current].setIndex(current)
                self._remove(lchild, last)
        else:
            if self._queue[current] > self._queue[rchild]:
                self._queue[current], self._queue[rchild] = self._queue[rchild], self._queue[current]
                self._queue[rchild].setIndex(rchild)
                self._queue[current].setIndex(current)
                self._remove(rchild, last)

    def update_key(self, element, newkey):
        '''
        update the key in element to be newkey, and rebalance the APQ
        '''
        oldkey = self.get_key(element)
        elem = self.get_element(element)
        elem.setKey(newkey)
        i = elem.getIndex()
        if newkey > oldkey:
            self._remove(i, self.length()-1)
        else:
            self._add(elem, i)

    def get_element(self, value):
        '''
        return first element with matching value
        '''
        for elem in self._queue:
            if elem.getValue() == value:
                return elem

    def is_empty(self):
        '''
        returns True if queue is empty
        '''
        if len(self._queue) > 0:
            return False
        return True
        
    def get_key(self, element):
        '''
        return the current key for the element
        '''
        return self.get_element(element)._key

    def remove(self,element):
        '''
        remove element from APQ and rebalance it
        '''
        last = self.length()-1
        i = element.getIndex()
        if i != last:
            self._queue[i], self._queue[last] = self._queue[last], self._queue[i]
            self._queue[i].setIndex(i)
            last -= 1

            while last > 0:
                self._remove(i, last)
                last -= 1

        elem = self._queue.pop(self.length()-1)
        return elem.getKey(), elem.getValue()

    def length(self):
        '''
        return length of queue
        '''
        return len(self._queue)



class Element:
    def __init__(self, key, value, index):
        self._key =  key
        self._value =  value
        self._index =  index

    def __str__(self):
        retstr = str(self._value) + ' with cost ' + str(self._key)
        return retstr
    
    def __eq__(self, other):
        return self._key == other._key
    
    def __lt__(self, other):
        return self._key < other._key

    def __gt__(self, other):
        return self._key > other._key

    def getValue(self):
        return self._value

    def getKey(self):
        return self._key

    def setKey(self, key):
        self._key = key

    def getIndex(self):
        return self._index

    def setIndex(self, index):
        self._index = index

    def _wipe(self):
        self._key =  None
        self._value =  None
        self._index =  None


class RouteMap(Graph):
    def __init__(self):
        super().__init__()
        self._coords = dict()
        self._search = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        num_v = self.num_vertices()
        num_e = self.num_edges()
        if num_v >= 100 or num_e >= 100:
            return None
        hstr = ('|V| = ' + str(num_v)
                + '; |E| = ' + str(num_e))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + str(self._coords[v]) + '--'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    #-----------------------------------------------------------------------#

    # ADT methods to query the graph

    def get_vertex_by_label(self, element):
        """ Return the first vertex that matches element. """
        try:
            return self._search[element]
        except KeyError:
            return None

    #----------------------------------------------------------------------#

    # ADT methods to modify the graph

    def add_vertex(self, element, coords):
        """ Add a new vertex with data element.

        If there is already a vertex with the same data element,
        this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        self._search[element] = v
        self._coords[v] = coords
        return v

    #----------------------------------------------------------------------#

    def sp(self, v, w):
        v_path = self.dijkstra(v)
        target = w
        path = [w]
        while v_path[target][1] != None:
            path.append(v_path[target][1])
            target = v_path[target][1]
        path.reverse()
        return path

    def print_path(self, path):
        print('type', 'latitude', 'longitude', 'element', 'cost', sep='\t')
        i = 0
        cost = 0
        while i < len(path)-1:
            e = self.get_edge(path[i], path[i+1])
            cost += e.cost()
            retstr = 'W' + '\t' + str(self._coords[path[i]][0]) + '\t' +  str(self._coords[path[i]][1])
            retstr +=  '\t' + path[i].__str__() + '\t' +  str(cost)
            print(retstr)
            i += 1


def graphreader1(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    return graph

def test1(filename):
    graph = graphreader1(filename)
    v = graph.get_vertex_by_label(1)
    paths = (graph.dijkstra(v))
    retstr = ''
    for v in paths:
        retstr += 'Vertex: ' + str(v) + '\t Cost: ' + str(paths[v][0]) +'\t Preceded By Vertex: ' + str(paths[v][1]) + '\n'
    print(retstr)

test1('simplegraph1.txt')
# test1('simplegraph2.txt')



def graphreader2(filename):
    """ Read and return the route map in filename. """
    graph = RouteMap()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        line = file.readline().split()
        coords = (float(line[1]), float(line[2]))
        vertex = graph.add_vertex(nodeid, coords)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        file.readline()
        time = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, time)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    return graph

def test2(filename):
    routemap = graphreader2(filename)
    if filename == 'simpleroute.txt':
        simpleroute(routemap)
    elif filename == 'corkCityData.txt':
        corkcityMap(routemap)

def simpleroute(routemap):
    v = routemap.get_vertex_by_label(1)
    w = routemap.get_vertex_by_label(4)
    # path = routemap.sp(v, w)
    # routemap.print_path(path)
    paths = (routemap.dijkstra(v))
    retstr = ''
    for v in paths:
        retstr += 'Vertex: ' + str(v) + '\t Cost: ' + str(paths[v][0]) +'\t Preceded By Vertex: ' + str(paths[v][1]) + '\n'
    print(retstr)

def corkcityMap(routemap):
    ids = {}
    ids['wgb'] = 1669466540
    ids['turnerscross'] = 348809726
    ids['neptune'] = 1147697924
    ids['cuh'] = 860206013
    ids['oldoak'] = 358357
    ids['gaol'] = 3777201945
    ids['mahonpoint'] = 330068634
    sourcestr = 'wgb'
    deststr='neptune'
    source = routemap.get_vertex_by_label(ids[sourcestr])
    dest = routemap.get_vertex_by_label(ids[deststr])
    time1 = time.time()
    tree = routemap.sp(source,dest)
    time2 = time.time()
    routemap.print_path(tree)
    print(time2-time1)

# test2('simpleroute.txt')
print()
test2('corkCityData.txt')