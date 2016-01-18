from ABKSectionPoint import *
from DrawSection import DrawGeometry
from wxmplot import PlotApp


if __name__ == "__main__":
    #Isec = grooveSection(50, 37, 4.5, 7, 7.0, 3.5)

    #Isec = grooveSection(200, 75, 9, 11, 11, 5.5)
    #Isec = grooveSection(200, 73, 7, 11, 11, 5.5)
    Isec = grooveSection(400, 104, 14.5, 18, 18.0, 9.0)
    geo = GeoCalculator(Isec)
    geo.Solve()
    print geo.Area()
    p = geo.Centroid()
    print p

    app = PlotApp()
    Path = DrawGeometry(Isec)
    Path.Draw()

    newGsec=Isec.moveCoor(-p[0],0)
    geo1 = GeoCalculator(newGsec)
    geo1.Solve()
    print geo.Area()
    print geo1.Ix()
    print geo1.Iy()
    print geo1.ix()
    print geo1.iy()
    print geo1.Centroid()

    for i in Path._paths:
        m,n=zip(*i)
        app.oplot(m,n,title='Example PlotApp',  label='a',
       ylabel=r'$k^2\chi(k) $',
       xlabel=r'$  k \ (\AA^{-1}) $')

    app.write_message('Try Help->Quick Reference')
    app.run()