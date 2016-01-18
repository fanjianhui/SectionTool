from ABKSectionPoint import *
from DrawSection import DrawGeometry
from wxmplot import PlotApp

if __name__ == "__main__":
    comSec = compoundSection()

    p1 = Point(0, 0)
    p2 = Point(1, 0)
    p3 = Point(1, 1)
    p4 = Point(0, 1)
    p = Polygon(p1,p2,p3,p4)
    Mp = MultiConnectPoly()
    Mp.setOuterLoop(p)

    p5 = Point(0, 1)
    p6 = Point(1, 1)
    p7 = Point(1, 2)
    p8 = Point(0, 2)

    T = Polygon(p5,p6,p7,p8)
    Mpt = MultiConnectPoly()
    Mpt.setOuterLoop(T)

    comSec.addToSections(Mp)
    comSec.addToSections(Mpt)

    geo = GeoCalculator(comSec)

    geo.Solve()

    print geo.Area()

    print "a"

    app = PlotApp()
    Path = DrawGeometry(comSec)
    Path.Draw()
    for i in Path._paths:
        m,n=zip(*i)
        app.oplot(m,n,title='Example PlotApp',  label='a',
       ylabel=r'$k^2\chi(k) $',
       xlabel=r'$  k \ (\AA^{-1}) $')

    app.write_message('Try Help->Quick Reference')
    app.run()