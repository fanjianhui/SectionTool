from sympy.geometry import *

from DrawSection import DrawGeometry
from wxmplot import PlotApp
from ABKSectionPoint import *

import math

# multiConnectPoly

if __name__ == "__main__":
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    # a1 = ABKArc(p1, pi/4, -pi/4, sqrt(2))
    # print a1.getAttribute()
    p3 = Point(1, 1)
    p4 = Point(0, 1)

    p = Polygon(p1,p2,p3,p4)
    print p.area
    print p.vertices

    p5 = Point(2,2)
    p6 = Point(-2, 2)
    p7 = Point(-2, -2)
    p8 = Point(0.5, 0.5)

    T = Polygon(p5,p6,p7,p8)

    print T.area
    print T.vertices

    p9 = Point(100,100)
    p10 = Point(-100,100)
    p11 = Point(0,-100)

    p12 = Point(4,4)
    p13 = Point(5,4)
    p14 = Point(5,5)
    p15 = Point(4,5)

    R = Polygon(p12,p13,p14,p15)

    Q = Polygon(p9,p10,p11)

    MP = MultiConnectPoly()
    #MP.setOuterLoop(p5,p6,p7,p8)
    MP.setOuterLoop(Q)
    #MP.addInnerLoop(p1,p2,p3,p4)
    MP.addInnerLoop(p5,p6,p7,p8)
    MP.addInnerLoop(p)
    MP.addInnerLoop(R)
    MP.addInnerLoop(p5,p6,p7,p8)

    print MP.getpolylist()

    geo = GeoCalculator(MP)
    geo.Solve()
    print geo.Area()
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

    app = PlotApp()
    Path = DrawGeometry(MP)
    Path.Draw()

    for i in Path._paths:
        m,n=zip(*i)
        app.oplot(m,n,title='Example PlotApp',  label='a',
       ylabel=r'$k^2\chi(k) $',
       xlabel=r'$  k \ (\AA^{-1}) $')

    app.write_message('Try Help->Quick Reference')
    app.run()