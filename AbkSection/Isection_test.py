from ABKSectionPoint import *
from DrawSection import DrawGeometry
from wxmplot import PlotApp

if __name__ == "__main__":
    Isec = ISection(100, 68, 4.5, 7.6, 6.5, 3.3)
    geo = GeoCalculator(Isec)
    geo.Solve()
    print geo.Area()
    p = geo.Centroid()
    alfa = geo.tan_alfa()
    print p
    print "a=" + str(alfa)

    app = PlotApp()
    Path = DrawGeometry(Isec)
    Path.Draw()

    #newIsec = Isec.moveCoor(-p[0], -p[1])
    #origin = Point(0,0)

    #newIsec = Isec.rotate(pi/4, p)
    #newIsec = Isec.transform(-p[0],-p[1],-alfa, origin)

    #geo1 = GeoCalculator(newIsec)
    #geo1.Solve()
    #print geo1.Area()
    #print geo1.Centroid()

    for i in Path._paths:
        m,n=zip(*i)
        app.oplot(m,n,title='Example PlotApp',  label='a',
       ylabel=r'$k^2\chi(k) $',
       xlabel=r'$  k \ (\AA^{-1}) $')

    app.write_message('Try Help->Quick Reference')
    app.run()