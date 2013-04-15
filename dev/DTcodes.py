from snappy import *
from spherogram import FatGraph, FatEdge
from spherogram.links import Link, Crossing
import string

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

def char_to_int(x):
    sign = -1 if x.isupper() else 1
    return sign*(string.ascii_letters.index(x.lower())+1)

def string_to_ints(s):
    return [char_to_int(x) for x in s]

def partition_list(L, parts):
    assert sum(parts) == len(L)
    ans = []
    k = 0
    for p in parts:
        ans.append(L[k:k+p])
        k += p
    return ans
        

# To reconstruct a knot projection from a DT code we first construct
# a fat graph, which may not be a planar surface.  There are only
# two possible orderings of edges at each vertex, since we know which
# pairs of edges are opposites.  The process of finding the
# projection consists of reversing the orderings of some vertices
# to get a planar surface.
#
# Each crossing in the diagram is traversed twice in building the DT
# code.  Our convention is to initially label the four edges at the
# crossing as South, East, North, West in such a way that the first
# time a component passes through the vertex it enters at South and
# leaves at North; the second time it enters at East and leaves at
# West.
#
#        N
#        ^
#        |
#        |
# W <--------- E second         Initial vertex orientation 
#        |
#        |
#        S
#      first
#
# This determines an embedding of each crossing into the oriented
# plane, which may not extend to an embedding of the knot diagram.  In
# constructing the planar embedding of the diagram we preserve this
# embedding of the vertices, but adjust the fat graph by
# interchanging the attaching points of a pair of edges entering at
# opposite sides of the crossing.

South, East, North, West = 0, 1, 2, 3

class FlippingError(Exception):
    pass

class EmbeddingError(Exception):
    pass

class DTvertex:
    """
    A vertex of the 4-valent graph which is described by a DT code.
    Instantiate with an even-odd pair, in either order.
    """
    # In keeping with the philosphy of Spherogram.graphs, vertices
    # should never be changed by graph methods.  They are owned by
    # the DTcodec.

    def __init__(self, pair, overcrossing=1):
        self._first = min(pair)
        self._second = max(pair)
        self._even_over = True if overcrossing == -1 else False

    def __repr__(self):
        return str((self._first, self._second))

    def entry_slot(self, N):
        if N == self._first: return South
        elif N == self._second: return East
        else: raise ValueError('%d is not a label of %s'%(N,self))

    def exit_slot(self, N):
        if N == self._first: return North
        elif N == self._second: return West
        else: raise ValueError('%d is not a label of %s'%(N,self))

    def first_under(self):
        if self._even_over:
            return self._first-1 if self._first%2 == 1 else self._second-1
        else:
            return self._first-1 if self._first%2 == 0 else self._second-1

    def upper_pair(self):
        return (0,2) if bool(self._first%2) ^ self._even_over else (1,3)
    
class DTPath:
    """
    An iterator which starts at a FatEdge and walks around the
    link component containing that edge.  A DTPath raises
    StopIteration when it returns to its starting edge.
    """
    def __init__(self, edge, graph, forward=True):
        self.first_edge = edge
        self.next_edge = None
        self.graph = graph
        self.end = 1 if forward else 0

    def __iter__(self):
        return self

    def next(self):
        try:
            slot = self.next_edge.slots[self.end]
            self.next_edge = self.graph(self.next_edge[self.end])[slot+2]
            if self.next_edge == self.first_edge:
                raise StopIteration
        except AttributeError:
            self.next_edge = self.first_edge
        return self.next_edge

class DTFatEdge(FatEdge):
    """
    A fat edge which can be marked.
    """
    def __init__(self, x, y, twists=0):
        FatEdge.__init__(self, x, y, twists)
        self.marked = False

    def PD_index(self):
        v = self[0]
        if self.slot(v)%2 == 0:
            return v._first
        else:
            return v._second

class DTFatGraph(FatGraph):
    edge_class = DTFatEdge

    def __init__(self, pairs=[], singles=[]):
        FatGraph.__init__(self, pairs, singles)
        self.stack = []
        self.pushed = False

    def PD_list(self, vertex):
        edgelist = [e.PD_index() for e in self(vertex)]
        n = edgelist.index(vertex.first_under())
        return edgelist[n:] + edgelist[:n]

    def sign(self, vertex):
        flipped = bool(len([e for e in self(vertex) 
                       if e[1] == vertex and e.slots[1] in (2,3)])%2)
        even_first = bool(vertex._first%2 == 0)
        return -1 if (flipped ^ vertex._even_over ^ even_first) else 1

    def push(self, flips):
        # Ignore the first push -- the first arc always is ambiguous
        # but the choice is irrelevant, up to reflecting the plane.
        if not self.pushed:
            self.pushed = True
            return
        #print 'pushing %s'%flips
        self.stack.append( [flips,
                            [ ( (e[0], e.slots[0]), (e[1], e.slots[1]) )
                              for e in self.edges if e.marked],
                            [ ( (e[0], e.slots[0]), (e[1], e.slots[1]) )
                              for e in self.edges if not e.marked]
                            ]
                           )

    def pop(self):
        self.edges = set()
        flips, marked, unmarked = self.stack.pop()
        for x, y in marked:
            self.add_edge(x,y)
        for edge in self.edges:
            edge.marked = True
        for x, y in unmarked:
            self.add_edge(x,y)
        #print 'popped %s[%s]'%(vertex, flips)
        #print 'stack size: %d'%len(self.stack)
        return flips

    def clear_stack(self):
        self.stack = []
        self.pushed = False

    def path(self, vertex, edge):
        """
        Return an iteratator which iterates through the edges of a
        component, starting at the given edge, in the direction
        determined by the vertex.
        """
        if not vertex in edge:
            raise ValueError('That vertex is not an endpoint of the edge.')
        forward = True if vertex == edge[0] else False
        return DTPath(edge, self, forward)

    def marked_arc(self, vertex):
        """
        Given a vertex with marked valence 2, find the maximal marked
        arc containing the vertex for which all interior edges have
        marked valence 2.  If the marked subgraph is a circle, or a
        dead end is reached, raise ValueError.  Return a list of
        edges in the arc.
        """
        left_path, right_path, vertices = [], [], set()
        vertices.add(vertex)
        try:
            left, right = [e for e in self(vertex) if e.marked]
        except ValueError:
            raise RuntimeError('Vertex must have two marked edges.')
        for edge, path in (left, left_path), (right, right_path):
            V = vertex
            while True:
                path.append(edge)
                V = edge(V)
                if V == vertex:
                    raise ValueError('Marked graph is a circle')
                edges = [e for e in self(V) if e.marked and e != edge]
                if len(edges) == 0:
                    raise ValueError('Marked graph has a dead end at %s.'%V)
                if len(edges) > 1:
                    break
                else:
                    vertices.add(V)
                    edge = edges.pop()
        left_path.reverse()
        return left_path + right_path
                
    def unmarked_arc(self, vertex):
        """
        Starting at this vertex, find an unmarked edge and follow its
        component until we run into a vertex with at least one marked
        edge.  Remove loops to get an embedded arc. Return the list
        of edges traversed by the embedded arc.
        """
        valence = self.marked_valence(vertex)
        if valence == 4:
            raise ValueError('Vertex must have unmarked edges.')
        if valence == 0:
            raise ValueError('Vertex must lie in the subgraph.')
        edges, vertices, seen = [], [], set()
        for first_edge in self(vertex):
            if not first_edge.marked:
                break
        for edge in self.path(vertex, first_edge):
            edges.append(edge)
            vertex = edge(vertex)
            if self.marked_valence(vertex) > 0:
                break
            # Remove loops as they appear
            if vertex in seen:
                n = vertices.index(vertex)
                edges = edges[:n+1]
                vertices = vertices[:n+1]
                seen = set(vertices)
            else:
                vertices.append(vertex)
                seen.add(vertex)
        return edges, vertex

    def bridge(self, marked_arc):
        """
        Try to find an embedded path of unmarked edges joining a
        vertex in the given arc to a vertex of the marked subgraph
        which lies in the complement of the interior of the arc.  This
        uses a depth-first search, and raises ValueError on failure.
        Returns a triple (first vertex, last vertex, edge path).

        Suppose the marked subgraph has no vertices with marked
        valence 3 and has a unique planar embedding.  Choose a maximal
        arc with all interior vertices having marked valence 2. Then
        adding a bridge from that arc produces a new graph with a
        unique planar embedding.

        In the case where the diagram is prime, a bridge will exist
        for *some* vertex on the arc.  But, e.g. in the case where the
        arc snakes through a twist region, it will only exist for the
        two extremal vertices in the arc.
        """
        # Find the interior vertices on the arc.
        e0, e1 = marked_arc[:2]
        v = e0[0] if e0[1] in e1 else e0[1]
        vertex_list = []
        for edge in marked_arc[:-1]:
            v = edge(v)
            vertex_list.append(v)
        #print 'bridge:', marked_arc
        #print 'avoiding:', vertex_list
        for start_vertex in vertex_list:
            # the vertex_set gets expanded to include vertices visited
            # by the bridge path.
            vertex = start_vertex
            vertex_set = set(vertex_list)
            edge_path, vertex_path, seen_edges = [], [], set()
            while True:
                edges = [e for e in self(vertex) if
                         not e.marked 
                         and e not in seen_edges 
                         and e(vertex) not in vertex_set]
                try:
                    new_edge = edges.pop()
                    vertex = new_edge(vertex)
                    edge_path.append(new_edge)
                    if ( self.marked_valence(vertex) > 0 ):
                        return start_vertex, vertex, edge_path
                    seen_edges.add(new_edge)
                    vertex_path.append(vertex)
                    vertex_set.add(vertex)
                except IndexError: # Cannot continue: back up.
                    if len(edge_path) == 0:
                        break
                    edge_path.pop()
                    vertex_set.remove(vertex_path.pop())
                    try:
                        vertex = vertex_path[-1]
                    except IndexError:
                        vertex = start_vertex
        raise ValueError('Could not find a bridge.')

    def _boundary_slots(self, edge, side):
        """
        Assume that the marked subFatGraph has been embedded in the
        plane.  This generator starts at a marked FatEdge and walks
        around one of its adjacent boundary curves (left=-1, right=1),
        yielding all of the pairs (v, s) where s is a slot of the
        vertex v which lies on the specified boundary curve, or
        (v, None) if none of the slots at v lie on the curve.  (To
        extend the embedding over an unmarked arc, the ending slots of
        both ends of the arc must lie on the same boundary curve.)
        """
        if not edge.marked:
            raise ValueError('Must begin at a marked edge.')
        first_vertex = vertex = edge[1] 
        while True:
            end = 0 if edge[0] == vertex else 1
            slot = edge.slots[end]
            for k in range(3):
                slot += side
                interior_edge = self(vertex)[slot]
                if not interior_edge.marked:
                    # For lookups, slot values must be in 0,1,2,3
                    yield vertex, slot%4  
                else:
                    break
            if k == 0:
                yield (vertex, None)
            if edge == interior_edge:
                raise ValueError('Marked subgraph has a dead end.')
            edge = interior_edge
            vertex = edge(vertex)
            if vertex == first_vertex:
                break

    def left_slots(self, edge):
        return self._boundary_slots(edge, side=-1)

    def right_slots(self, edge):
        return self._boundary_slots(edge, side=1)

    def marked_valence(self, vertex):
        return len([e for e in self(vertex) if e.marked])

    def clear(self):
        for e in self.edges:
            e.marked = False
 
    def flip(self, vertex, slot):
        """
        Either an East-West or North-South flip, depending on the
        slot.  Move the edge at this slot to the opposite slot, and
        move the edge in the opposite slot to this slot.
        """
        #print 'flipping %s[%s]'%(vertex, slot)
        mv = self.marked_valence(vertex)
        if mv >= 3:
            msg = 'Cannot flip %s with marked valence %d.'%(vertex,mv)
            raise FlippingError(msg)
        if slot == South or slot == North:
            self.reorder(vertex, (North, East, South, West))
        elif slot == East or slot == West:
            self.reorder(vertex, (South, West, North, East))
        else:
            raise ValueError('Invalid slot index.')

# This assumes that the diagram is connected; that it has
# no loops, and that each component meets the next one.

class DTcodec:
    """
    Codec for DT codes of a link projection.  If instantiated with
    a DT code, as a list of tuples or an alphabetical code, it decodes
    the input as a knot projection.  If instantiated with a knot
    projection it encodes the projection as a DT code.
    """
    def __init__(self, input=None):
        if isinstance(input, str):
            self.decode(self.convert_alpha(input))
        if isinstance(input, list):
            self.decode(input)
        #encoding is not implemented yet.

    def convert_alpha(self, code):
        code = string_to_ints(code)
        num_crossings, components = code[:2]
        comp_lengths = code[2:2+components]
        crossings = [2*x for x in code[2+components:]]
        assert len(crossings) == num_crossings
        return partition_list(crossings, comp_lengths)
        
    def decode(self, code):
        if isinstance(code, (str, bytes)):
            code = self.convert_alpha(code)
        overcrossings = [sign(x) for comp in code for x in comp]
        evens = [abs(x) for comp in code for x in comp]
        self.size = size = 2*len(evens)
        pairs = zip(range(1, size, 2), evens)
        # Build a lookup table for the vertices.
        # (DT codes are 1-based; we just waste the 0 entry.) 
        self.lookup = lookup = [None for n in range(1+size)]
        for pair, overcrossing in zip(pairs, overcrossings):
            V = DTvertex(pair, overcrossing)
            m, n = pair
            lookup[m] = lookup[n] = V
        # Now build the fatgraph determined by the DT code.
        self.fat_graph = DTFatGraph()
        N = start = 1
        last_odd = -1
        for component in code:
            last_odd += 2*len(component)
            V = self[N]
            # Walk around this component, adding edges.
            while N <= last_odd:
                W = self[N + 1]
                self.fat_graph.add_edge( (V, V.exit_slot(N)),
                                         (W, W.entry_slot(N+1)) )
                N += 1
                V = W
            # Close up this component and go to the next one.
            S = self[start]
            self.fat_graph.add_edge( (V, V.exit_slot(N)),
                                     (S, S.entry_slot(start)) )
            start = N = N+1
        # Now find the planar embedding
        self.embed()

    def __getitem__(self, n):
        """
        A DTcode can look up a vertex by either of its labels.
        """
        return self.lookup[n]

    def mark(self, edgelist):
        for edge in edgelist:
            edge.marked = True

    def embed(self, edge=None):
        """
        Try to flip crossings in the FatGraph until it becomes planar.
        """
        G = self.fat_graph
        if edge is None: # OK. No problem. Just pick one at random.
            for edge in G.edges: break
        # Find a circle and embed it.
        vertices, circle_edges = self.find_circle(edge)
        self.mark(circle_edges)
        #print 'circle', circle_edges
        # Add one arc, to get a theta graph.
        # The first arc needs to be bridge!
        first, last, arc_edges = G.bridge(circle_edges[:2])
        #print 'first_arc', arc_edges
        self.do_flips(first, arc_edges[0], last, arc_edges[-1])
        self.mark(arc_edges)
        # Keep adding arcs until the whole graph is embedded.
        while True:
            try:
                if not self.embed_arc():
                    break
            except EmbeddingError:
                flips = G.pop()
                for vertex, slot in flips:
                    G.flip(vertex, slot)
        # Clean up.
        self.fat_graph.clear_stack()

    def find_circle(self, first_edge):
        """
        Follow a component, starting at the given (directed) edge,
        until the first time it crosses itself.  Throw away the tail
        to get a cycle.  Return the list of vertices and the list of
        edges traversed by the cycle.
        """
        edges = []
        vertices = [first_edge[0]]
        seen = set(vertices)
        for edge in self.fat_graph.path(first_edge[0], first_edge):
            vertex = edge[1]
            if vertex in seen:
                edges.append(edge)
                break
            else:
                seen.add(vertex)
                vertices.append(vertex)
                edges.append(edge)
        n = vertices.index(vertex)
        edges = edges[n:]
        vertices = vertices[n:]
        return vertices, edges

    def get_incomplete_vertex(self):
        """
        Return a vertex with some marked and some unmarked edges.
        If there are any, return a vertex with marked valence 3.
        """
        # This could be done with table lookups.
        G = self.fat_graph
        vertices = [v for v in G.vertices if 0 < G.marked_valence(v) < 4]
        vertices.sort( key=lambda v : -G.marked_valence(v) )
        try:
            v = vertices.pop(0)
            return v
        except IndexError:
            return None

    def do_flips(self, v, v_edge, w, w_edge):
        """
        Decide whether v and/or w needs to be flipped in order to add
        an arc from v to w starting with the v_edge and ending with
        the w_edge.  If flips are needed, make them.  If the embedding
        cannot be extended raise an exception.
        """
        G = self.fat_graph
        vslot = G(v).index(v_edge)
        wslot = G(w).index(w_edge)
        #print 'do_flips: %s[%s] %s[%s]'%(v, vslot, w, wslot) 
        not_unique = ( G.marked_valence(v) == G.marked_valence(w) == 2 )
        # starting from the v_edge, go ccw to a marked edge
        for k in range(1,3):
            ccw_edge = G(v)[vslot+k]
            if ccw_edge.marked:
                break
        if not ccw_edge.marked:
            raise ValueError('Invalid marking')
        # Here are the slots and vertices in the two boundary curves:
        left_slots = set(G.left_slots(ccw_edge))
        right_slots = set(G.right_slots(ccw_edge))
        v_valence, w_valence = G.marked_valence(v), G.marked_valence(w)
        if (v, vslot) in left_slots:
            v_slot_side, v_other_side = left_slots, right_slots
        else:
            v_slot_side, v_other_side = right_slots, left_slots
        w_on_slot_side = w in [ x[0] for x in v_slot_side ]
        w_on_other_side = w in [ x[0] for x in v_other_side ]
        if not w_on_slot_side and not w_on_other_side:
            raise EmbeddingError('Embedding does not extend.')
        if (w, wslot) in v_slot_side:
            if v_valence == w_valence == 2:
                # This is an ambiguous situation.  We could either do
                # nothing or flip both vertices.  push our
                # state with instructions to flip both vertices if we
                # pop.
                G.push([(v, vslot), (w, wslot)])
            return
        if w_valence != 2:
            G.flip(v, vslot)
            return
        elif v_valence != 2:
            G.flip(w, wslot)
            return
        # At this point we know that flips are needed *and* that both
        # vertices have marked valence 2.
        if w_on_slot_side and not w_on_other_side:
            G.flip(w, wslot)
            return
        if w_on_slot_side and w_on_other_side:
            # This is an ambiguous situation.  We know w does not have
            # a slot on the v slot side.  We are are about to flip v.
            # But we could leave v alone and flip w instead.  We
            # push our state with instructions to flip w if we
            # pop.
            G.push([(w, wslot)])
        G.flip(v, vslot)
        if not (w, wslot) in v_other_side:
            G.flip(w, wslot)

    def embed_arc(self):
        G = self.fat_graph
        v = self.get_incomplete_vertex()
        if v is None:
            return False
        if G.marked_valence(v) == 2:
        # This should work for any vertex if the diagram is reduced.
            try:
                first, last, arc_edges = G.bridge(G.marked_arc(v))
            except ValueError:
                print 'Failed to find a bridge on the first try.'
                for v in [x for x in G.vertices if G.marked_valence(v) == 2]:
                    try:
                        first, last, arc_edges = G.bridge(G.marked_arc(v))
                        break
                    except ValueError:
                        print 'Failed to find a bridge again.'
                        continue
            #print 'adding bridge', arc_edges
            self.do_flips(first, arc_edges[0], last, arc_edges[-1])
        else:
            arc_edges, last_vertex = G.unmarked_arc(v)
            #print 'adding arc', arc_edges
            # Since v has 3 marked edges, we put it second here.
            self.do_flips(last_vertex, arc_edges[-1], v, arc_edges[0])
        self.mark(arc_edges)
        return True

    def PD_code(self, KnotTheory=False):
        G = self.fat_graph
        PD = [ G.PD_list(v) for v in G.vertices ]
        if KnotTheory:
            PD = "PD" + repr(PD).replace('[', 'X[')[1:]
        return PD

    def link(self):
        G = self.fat_graph
        crossing_dict = {}
        for v in G.vertices:
            c = Crossing(v._first)
            c.make_tail(0)
            if G.sign(v) == 1:
                c.make_tail(3)
            else:
                c.make_tail(1)
            c.orient()
            crossing_dict[v] = c
        for edge in G.edges:
            if edge.slots[0] in edge[0].upper_pair():
                a = 1 if G.sign(edge[0]) == 1 else 3
            else:
                a = 2
            if edge.slots[1] in edge[1].upper_pair():
                b = 3 if G.sign(edge[1]) == 1 else 1
            else:
                b = 0
            crossing_dict[edge[0]][a] = crossing_dict[edge[1]][b]
        return Link(crossing_dict.values())

