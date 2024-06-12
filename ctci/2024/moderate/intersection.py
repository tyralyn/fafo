'''
given two straight line segments each repr by a starting and ending point, compute the point of intersection, if any

input: tuples for each coord of the line segment, repr as a tuple. i think it would be best to represent it as a namedtupkle
'''

from collections import namedtuple

Point = namedtuple('Point', ['x','y'])
# p = Point(x=4,y=-5)
# print (p.x, p.y)


'''
so this is some real math shit, lets look at the hints
hint 465: think about what im going to design for
	..... ??? dfq
hint 472: will all lines intercept? how is this determined?
hint 497: infinite lines always intersect unless theyre parallel. wot does this mean for line segments?
hint 517: "How can we find the intersection between two lines? If two line segments intercept, then this must be at the same point as their "infinite" extensions. Is this intersection point within both lines?"
hint 527: "Think carefully about how to handle the case of line segments that have the same slope and y-intercept."

this is a lot of math....

i feel like i wont get asked this question bc it is a lot of math that ppl have probably forgotten
'''
def intersection (p1: Point, p2: Point):
