from sympy.geometry import *
import os
import datetime
p0 = Point(0,0)
p1 = Point(0,1)
p2 = Point(1,1)
p3 = Point(1,0)

p5 = Point(0,0.5)
p6 = Point(1, 0.5)
p7 = Point(1, 1.5)
p8 = Point(0, 1.5)

poly = Polygon(p0,p1,p2,p3)
poly1 = Polygon(p5,p6,p7,p8)

currenttime = datetime.datetime.now()
currenttime = str(currenttime.isoformat())
currenttime = currenttime[0:len(currenttime)-6]
for c in '-:.T': # "
    currenttime = currenttime.replace(c, '')
#res = poly.intersection(poly1)
print currenttime
print poly.encloses_point(Point(1, 0.5))
