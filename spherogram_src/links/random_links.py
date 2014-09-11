"""
Generating random knots starting with randomly generated planar maps.

Code written as part of a 2013 Illinois Geometry Lab project by

Nathan Dunfield, Alexander Ehrenberg, Shiladitya Bhattacharyya, and Dongming Lei

Details to hopefullly appear in some paper or other.  
"""

import os, sys, re, gzip, random
from .. import graphs
from . import links, twist
from spherogram.planarmap import random_map as raw_random_map

def random_map(num_verts, edge_conn_param=4, initial_map_gives_knot=False):
    """
    Returns a dictionary of endpoints of edges in the form:

    (signed edge) -> (vertex, position)
    """
    if isinstance(num_verts, list):
        data = num_verts
    else:
        num_link_comps = 1 if initial_map_gives_knot else 0
        data = raw_random_map(num_verts, edge_conn_param, num_link_comps)

    vertex_adjacencies = []
    for vertex, adjacencies in data:
        if random.randrange(2):
            adjacencies = adjacencies[1:] + adjacencies[:1]
        vertex_adjacencies.append(adjacencies)

    edge_adjacencies = dict()
    for v, edges in enumerate(vertex_adjacencies):
        for i, edge in enumerate(edges):
            edge_adjacencies[edge] = (v, i)
    return edge_adjacencies
        
def map_to_link(map):
    num_edges = len(map) // 2
    crossings = [links.Crossing() for i in range(num_edges//2)]
    for e in range(1, num_edges+1):
        (a, i), (b,j) = map[e], map[-e]
        crossings[a][i] = crossings[b][j]
    ans = links.Link(crossings, check_planarity=False)
    return ans

def self_crossings(component):
    comp_set = set(component)
    return  [ce for ce in component if ce.other() in comp_set]
    
def longest_component(link):
    self_crosses = [self_crossings(comp) for comp in link.link_components]
    longest = max(self_crosses, key=len)
    crossings = list(set(ce.crossing for ce in longest))
    for i, ce0 in enumerate(longest):
        A, a = ce0.rotate(2)
        B, b = longest[(i+1)%len(longest)]
        A[a] = B[b]
    return links.Link(crossings, check_planarity=False)

def simplified_prime_pieces(link):
    link.basic_simplify()
    ans = []
    cur = link.deconnect_sum(True)
    while len(cur):
        L = cur.pop()
        if L.basic_simplify():
            cur += L.deconnect_sum(True)
        else:
            ans.append(L)
    return ans

def largest_prime_piece(link):
    pieces = simplified_prime_pieces(link)
    if len(pieces) == 0:
        return links.Link([])
    return max(pieces, key=lambda L:len(L.crossings))

def random_knot(crossings,
                edge_conn_param=4,
                initial_map_gives_knot=False, 
                return_all_pieces=False, 
                prime_decomposition=True,
                consistient_twist_regions=False):
    if initial_map_gives_knot:
        plane_map = random_map(crossings, edge_conn_param, 1)
        initial_knot = map_to_link(plane_map)
    else:
        plane_map = random_map(crossings, edge_conn_param)
        initial_knot = longest_component(map_to_link(plane_map))

    if consistient_twist_regions:
        twist.make_twist_regions_consistent(initial_knot)
        
    initial_knot.simplify()
    if prime_decomposition:
        if return_all_pieces:
            return simplified_prime_pieces(initial_knot)
        else:
            return largest_prime_piece(initial_knot)
    else:
        return initial_knot

def new_random_knot(crossings, prime_decomposition=True):
    return random_knot(crossings, edge_conn_param=4,
                initial_map_gives_knot=True, 
                return_all_pieces=False, 
                prime_decomposition=prime_decomposition,
                consistient_twist_regions=True)

