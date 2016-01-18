## -*- coding: utf-8 -*-
from DrawSection import DrawGeometry
from wxmplot import PlotApp
from ABKSectionPoint import *

if __name__ == "__main__":


    rightAngle = rightAngleSection(25, 25, 4, 4, 3.5)
    # a = rightAngle.cen_ArcPoint
    geo = GeoCalculator(rightAngle)
    geo.Solve()
    print geo.Area()
    p = geo.Centroid()
    alfa = geo.tan_alfa()
    app = PlotApp()
    Path = DrawGeometry(rightAngle)

    Path.Draw()

    # 不应许修改的，那就新生产一个对象
    #newrightAngle = rightAngle.moveCoor(-p[0], -p[1])
    origin = Point(0,0)

    #newrightAngle = rightAngle.rotate(pi/4, p)
    newrightAngle = rightAngle.transform(-p[0],-p[1],-alfa, origin)

    geo1 = GeoCalculator(newrightAngle)
    geo1.Solve()
    print geo1.Area()
    print geo1.Centroid()

    #print 'asdf'
    #geo.Solve()
    #geo.Area()

    for i in Path._paths:
        m,n=zip(*i)
        app.oplot(m,n,title='Example PlotApp',  label='a',
       ylabel=r'$k^2\chi(k) $',
       xlabel=r'$  k \ (\AA^{-1}) $')

    app.write_message('Try Help->Quick Reference')
    app.run()




