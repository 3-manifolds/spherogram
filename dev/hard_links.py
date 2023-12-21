"""
A bunch of tricky links that used to break simplify.
"""

import spherogram
import random
import spherogram.links.simplify as simplify

def test(link):
    for i in range(10):
        L = link.copy()
        L.simplify('global')
        L.PD_code()
        expected = len(link.link_components) + L.unlinked_unknot_components
        print(L, L.unlinked_unknot_components, '\n')


C = spherogram.Link([(9, 17, 10, 16), (5, 18, 6, 19), (17, 4, 18, 5), (2, 15, 3, 16), (14, 8, 15, 7), (6, 14, 7, 13), (1, 13, 2, 12), (28, 22, 29, 21), (19, 11, 20, 10), (8, 4, 9, 3), (24, 27, 25, 0), (26, 23, 27, 24), (22, 25, 23, 26), (11, 21, 12, 20), (29, 0, 28, 1)])

test(C)

B = spherogram.Link([(9, 19, 10, 18), (4, 17, 5, 18), (16, 3, 17, 4), (2, 15, 3, 16), (14, 8, 15, 7), (6, 14, 7, 13), (1, 13, 2, 12), (28, 22, 29, 21), (19, 11, 20, 10), (8, 6, 9, 5), (24, 27, 25, 0), (26, 23, 27, 24), (22, 25, 23, 26), (11, 21, 12, 20), (29, 0, 28, 1)])

test(B)

# component incorrectly updated?
A = spherogram.Link([(21, 31, 22, 30), (16, 29, 17, 30), (28, 15, 29, 16),
                     (14, 27, 15, 28), (26, 20, 27, 19), (18, 26, 19, 25),
                     (13, 25, 14, 24), (37, 7, 32, 6), (5, 37, 6, 36),
                     (35, 3, 36, 2), (9, 34, 10, 35), (33, 8, 34, 9),
                     (31, 23, 0, 22), (20, 18, 21, 17), (7, 12, 8, 13),
                     (11, 4, 12, 5), (3, 10, 4, 11), (32, 1, 33, 2), (23, 1, 24, 0)])

test(A)


# Crazy recursion error
N = spherogram.Link([(14, 5, 15, 0), (6, 2, 7, 1), (15, 18, 16, 19), (17, 20, 18, 21),
                     (19, 16, 20, 17), (13, 2, 14, 3), (12, 10, 13, 9),
                     (8, 12, 9, 11), (10, 8, 11, 7), (21, 5, 6, 4), (3, 0, 4, 1)])

test(N)


# Failure to pull off a component sitting on top/bottom
M = spherogram.Link([(9,17,10,16),(5,18,6,19),(17,4,18,5),(2,15,3,16),(14,8,15,7),(6,14,7,13),(1,13,2,12),(28,22,29,21),(19,11,20,10),(8,4,9,3),(24,27,25,0),(26,23,27,24),(22,25,23,26),(11,21,12,20),(29,0,28,1)])
N = M.copy().mirror()

test(M)
test(N)

A = spherogram.Link([(13, 2, 14, 3), (21, 5, 6, 4), (15, 18, 16, 19), (17, 20, 18, 21), (19, 16, 20, 17), (14, 5, 15, 0), (12, 10, 13, 9), (8, 12, 9, 11), (10, 8, 11, 7), (6, 2, 7, 1), (3, 0, 4, 1)])

test(A)


X = spherogram.Link([(25, 30, 26, 31), (6, 30, 7, 33), (18, 11, 19, 12), (23, 15, 24, 14), (8, 15, 9, 16), (16, 3, 17, 4), (20, 10, 21, 9), (10, 22, 11, 21), (26, 29, 27, 0), (4, 27, 5, 28), (28, 5, 29, 6), (1, 13, 2, 12), (31, 24, 32, 25), (32, 8, 33, 7), (22, 20, 23, 19), (2, 17, 3, 18), (13, 1, 14, 0)])

Y = spherogram.Link([(8, 32, 9, 35), (29, 34, 30, 35), (1, 14, 2, 15), (26, 14, 27, 13), (12, 26, 13, 25), (24, 12, 25, 11), (10, 20, 11, 19), (7, 4, 8, 5), (31, 6, 0, 7), (5, 30, 6, 31), (20, 4, 21, 3), (2, 24, 3, 23), (27, 18, 28, 19), (21, 17, 22, 16), (32, 10, 33, 9), (33, 28, 34, 29), (15, 23, 16, 22), (17, 0, 18, 1)])

test(X)
test(Y)

B = spherogram.Link([(28, 39, 29, 40), (7, 39, 8, 38), (20, 13, 21, 14), (26, 16, 27, 15), (9, 16, 10, 17), (19, 2, 20, 3), (23, 11, 24, 10), (11, 25, 12, 24), (29, 37, 30, 36), (3, 30, 4, 31), (31, 4, 0, 5), (33, 12, 34, 13), (40, 27, 41, 28), (41, 9, 38, 8), (25, 23, 26, 22), (34, 22, 35, 21), (14, 35, 15, 36), (17, 33, 18, 32), (6, 37, 7, 32), (18, 2, 19, 1), (5, 0, 6, 1)])
test(B)

L = spherogram.Link([(28, 39, 29, 40), (7, 39, 8, 38), (20, 13, 21, 14), (26, 16, 27, 15), (9, 16, 10, 17), (19, 2, 20, 3), (23, 11, 24, 10), (11, 25, 12, 24), (29, 37, 30, 36), (3, 30, 4, 31), (31, 4, 0, 5), (33, 12, 34, 13), (40, 27, 41, 28), (41, 9, 38, 8), (25, 23, 26, 22), (34, 22, 35, 21), (14, 35, 15, 36), (17, 33, 18, 32), (6, 37, 7, 32), (18, 2, 19, 1), (5, 0, 6, 1)])
test(L)


P0 = spherogram.Link([(31, 38, 32, 39), (37, 30, 38, 31), (12, 29, 13, 30), (18, 50, 19, 49), (48, 20, 49, 19), (46, 11, 47, 12), (45, 36, 46, 37), (7, 44, 8, 45), (2, 10, 3, 9), (20, 0, 21, 27), (56, 18, 57, 17), (23, 14, 24, 15), (35, 9, 36, 8), (15, 55, 16, 54), (16, 25, 17, 26), (22, 51, 23, 52), (26, 57, 27, 54), (55, 24, 56, 25), (10, 4, 11, 3), (28, 48, 29, 47), (43, 35, 44, 34), (50, 14, 51, 13), (52, 21, 53, 22), (6, 34, 7, 33), (5, 43, 6, 42), (4, 2, 5, 1), (39, 32, 40, 33), (40, 53, 41, 42), (41, 0, 28, 1)])

P0.simplify('global')

test(P0)

P1 = spherogram.Link([(6, 32, 7, 31), (33, 38, 34, 39), (59, 35, 60, 34), (16, 54, 17, 53), (66, 8, 67, 7), (48, 46, 49, 45), (40, 48, 41, 47), (46, 40, 47, 39), (63, 44, 64, 45), (43, 21, 44, 20), (37, 59, 38, 58), (36, 26, 37, 25), (69, 14, 56, 15), (15, 68, 16, 69), (29, 18, 30, 19), (24, 57, 25, 58), (4, 13, 5, 14), (35, 26, 0, 27), (5, 57, 6, 56), (54, 18, 55, 17), (55, 2, 52, 3), (3, 52, 4, 53), (22, 42, 23, 41), (23, 32, 24, 33), (8, 20, 9, 19), (65, 43, 66, 42), (67, 30, 68, 31), (9, 63, 10, 62), (21, 65, 22, 64), (10, 61, 11, 62), (11, 28, 12, 29), (12, 1, 13, 2), (49, 60, 50, 61), (50, 27, 51, 28), (51, 0, 36, 1)])

test(P1)

P2 = spherogram.Link([(13, 19, 14, 18), (17, 39, 18, 38), (15, 20, 16, 21), (12, 8, 13, 7), (6, 12, 7, 11), (10, 40, 11, 39), (8, 41, 9, 42), (40, 5, 41, 6), (52, 47, 53, 48), (46, 53, 47, 54), (37, 57, 38, 56), (54, 0, 55, 21), (30, 52, 31, 51), (19, 42, 20, 43), (50, 32, 51, 31), (4, 9, 5, 10), (3, 16, 4, 17), (57, 2, 46, 3), (61, 35, 58, 34), (27, 48, 28, 49), (49, 26, 50, 27), (32, 26, 33, 25), (44, 55, 45, 56), (43, 15, 44, 14), (33, 61, 34, 60), (24, 59, 25, 60), (58, 23, 59, 24), (35, 28, 36, 29), (22, 30, 23, 29), (36, 2, 37, 1), (45, 0, 22, 1)])

test(P2)

P3 = spherogram.Link([(23, 54, 24, 55), (44, 17, 45, 18), (18, 45, 19, 46), (48, 0, 49, 13), (12, 37, 13, 38), (8, 12, 9, 11), (10, 6, 11, 5), (7, 35, 8, 34), (33, 7, 34, 6), (38, 49, 39, 50), (46, 41, 47, 42), (40, 47, 41, 48), (43, 23, 44, 22), (29, 32, 30, 33), (35, 30, 36, 31), (31, 36, 32, 37), (53, 24, 54, 25), (52, 16, 53, 15), (16, 52, 17, 55), (27, 51, 28, 50), (4, 10, 5, 9), (28, 3, 29, 4), (21, 43, 22, 42), (51, 2, 40, 3), (25, 21, 26, 20), (14, 19, 15, 20), (26, 2, 27, 1), (39, 0, 14, 1)])


test(P3)

P4 = spherogram.Link([(33, 17, 34, 16), (8, 11, 9, 12), (23, 13, 24, 12), (10, 35, 11, 30), (34, 9, 35, 10), (29, 5, 0, 4), (3, 29, 4, 28), (38, 26, 39, 25), (19, 22, 20, 23), (21, 18, 22, 19), (17, 20, 18, 21), (5, 30, 6, 31), (39, 6, 36, 7), (24, 38, 25, 37), (7, 36, 8, 37), (15, 2, 16, 3), (13, 33, 14, 32), (26, 32, 27, 31), (14, 2, 15, 1), (27, 1, 28, 0)])

test(P4)


P5 = spherogram.Link([(30, 28, 31, 27), (18, 12, 19, 11), (21, 37, 22, 36), (24, 16, 25, 15),
           (10, 18, 11, 17), (9, 3, 10, 2), (23, 39, 24, 38), (12, 20, 13, 19),
           (41, 34, 42, 35), (43, 15, 32, 14), (35, 42, 36, 43), (16, 26, 17, 25),
           (8, 30, 9, 29), (33, 40, 34, 41), (13, 33, 14, 32), (39, 21, 40, 20),
           (28, 8, 29, 7), (37, 23, 38, 22), (5, 6, 0, 7), (26, 3, 27, 4), (1, 5, 2, 4), (31, 0, 6, 1)])

P5.simplify('global')


P6 = spherogram.Link([(7,5,8,6),(24,5,25,4),(6,4,1,3),(29,2,30,1),(16,10,17,9),(39,13,40,12),(22,14,23,13),(8,16,9,15),(10,18,11,17),(35,19,36,18),(33,21,34,20),(14,24,15,23),(28,26,29,25),(32,28,7,27),(2,31,3,30),(26,32,27,31),(19,33,20,44),(21,35,22,34),(41,36,42,37),(43,38,44,39),(11,41,12,40),(37,42,38,43)])

P6.simplify('global')


P7 = spherogram.Link([(83,5,84,4),(218,5,219,6),(270,3,271,4),(307,2,308,3),(344,2,345,1),(41,6,42,7),(63,12,64,13),(15,108,16,109),(122,7,123,8),(141,10,142,11),(171,9,172,8),(14,190,15,189),(238,10,239,9),(258,12,259,11),(13,357,14,356),(18,51,19,52),(24,99,25,100),(21,103,22,102),(19,160,20,161),(22,195,23,196),(25,199,26,198),(17,208,18,209),(16,254,17,253),(23,286,24,287),(20,322,21,321),(55,30,56,31),(59,35,60,34),(31,113,32,112),(39,120,40,121),(136,34,137,33),(173,38,174,39),(29,184,30,185),(28,212,29,211),(240,37,241,38),(249,33,250,32),(36,262,37,261),(35,299,36,298),(40,349,41,350),(42,364,43,363),(67,46,68,47),(105,51,106,50),(144,45,145,46),(169,45,170,44),(192,49,193,50),(48,205,49,206),(234,48,235,47),(291,53,292,52),(133,57,134,56),(54,185,55,186),(53,211,54,210),(58,116,59,115),(138,61,139,62),(66,236,67,235),(57,246,58,247),(64,258,65,257),(68,281,69,282),(60,298,61,297),(62,355,63,356),(65,359,66,358),(70,151,71,152),(69,224,70,225),(71,331,72,330),(147,75,148,74),(150,73,151,74),(331,73,332,72),(166,75,167,76),(79,275,80,274),(314,78,315,77),(337,78,338,79),(130,89,131,90),(180,88,181,87),(88,182,89,181),(85,268,86,269),(86,305,87,306),(311,80,312,81),(340,82,341,81),(84,348,85,347),(82,365,83,366),(95,202,96,203),(231,97,232,96),(156,98,157,97),(197,100,198,101),(325,98,326,99),(104,160,105,159),(101,289,102,288),(103,322,104,323),(110,187,111,188),(106,208,107,207),(107,254,108,255),(294,110,295,109),(250,111,251,112),(134,114,135,113),(174,119,175,120),(241,118,242,119),(247,115,248,114),(262,117,263,118),(116,300,117,299),(121,350,122,351),(123,363,124,362),(131,182,132,183),(132,214,133,213),(146,223,147,224),(143,237,144,236),(135,248,136,249),(139,261,140,260),(145,280,146,281),(137,297,138,296),(140,353,141,354),(142,360,143,359),(333,148,334,149),(149,332,150,333),(193,158,194,159),(155,200,156,201),(152,226,153,225),(229,155,230,154),(157,285,158,284),(290,162,291,161),(334,166,335,165),(167,223,168,222),(176,243,177,244),(178,246,179,245),(175,264,176,265),(168,280,169,279),(177,300,178,301),(172,352,173,351),(170,361,171,362),(179,214,180,215),(212,183,213,184),(251,187,252,186),(191,206,192,207),(190,256,191,255),(295,188,296,189),(196,287,197,288),(194,324,195,323),(230,201,231,202),(326,200,327,199),(232,204,233,203),(283,204,284,205),(292,210,293,209),(215,267,216,266),(216,304,217,303),(217,348,218,349),(219,365,220,364),(220,277,221,278),(328,227,329,228),(228,327,229,328),(242,263,243,264),(233,283,234,282),(244,301,245,302),(239,353,240,352),(237,360,238,361),(293,252,294,253),(265,302,266,303),(267,305,268,304),(259,355,260,354),(256,357,257,358),(310,274,311,273),(341,272,342,273),(269,346,270,347),(271,367,272,366),(313,276,314,277),(338,276,339,275),(324,285,325,286),(289,320,290,321),(342,309,343,310),(306,345,307,346),(308,0,309,367),(339,313,340,312),(336,315,337,316),(343,0,344,1),(162,320,163,319),(163,26,164,27),(164,92,165,91),(329,93,330,92),(226,93,227,94),(153,94,154,95),(317,90,318,91),(318,28,319,27),(43,125,44,124),(278,126,279,125),(221,127,222,126),(76,127,77,128),(335,128,336,129),(316,130,317,129)])


simplify.strand_pickup(P7, 'over')


P8 = spherogram.Link([(2, 6, 3, 5), (6, 4, 7, 3), (22, 8, 23, 7), (13, 8, 14, 9), (9, 14, 10, 15), (15, 10, 16, 11), (11, 18, 12, 19), (19, 12, 0, 13), (16, 22, 17, 21), (20, 18, 21, 17), (4, 2, 5, 1), (23, 0, 20, 1)])
P8.simplify('global')
