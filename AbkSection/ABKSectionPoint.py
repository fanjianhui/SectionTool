## -*- coding: utf-8 -*-
from sympy.geometry import point, line, polygon,entity
from sympy import *
import math
# 圆弧对象：
class ABKArc(object):
    # 提供2中方式建立实体
    def __init__(self, *args):
        self.start = None
        self.end = None
        self.centroid = None
        # 1:圆心+2:起点+t3:theta(逆时针为正)
        if len(args) == 3:
            # 判断是否是点对象
            if isinstance(args[0], Point) and isinstance(args[1], Point):
                # 附上圆心
                self.centroid = args[0]
                # 附上起点
                self.start = args[1]
                # 计算出终点
                R = self.centroid.distance(self.start)
                theta = args[2]
                alfa = acos((self.start.x - self.centroid.x) / R)
                dx = cos(alfa + theta) * R
                dy = sin(alfa + theta) * R
                x_var = self.centroid.x + dx
                y_var = self.centroid.y + dy
                self.end = Point(x_var, y_var)
        # 圆心+起始角度+终止角度+半径
        if len(args) == 4:
            # 判断是否正确的数据类型
            if isinstance(args[0], Point):
                self.centroid = args[0]
                alfa = args[1]
                beta = args[2]
                R = args[3]
                xs = self.centroid.x + cos(alfa) * R
                ys = self.centroid.y + sin(alfa) * R
                xe = self.centroid.x + cos(beta) * R
                ye = self.centroid.y + sin(beta) * R
                self.start = Point(xs, ys)
                self.end = Point(xe, ye)

    # 圆弧对象要实现的方法
    # 返回圆弧的属性值
    def getAttribute(self):
        return self.start, self.end, self.centroid

# 复连通的poly..(不过数据点的保存形式不同)
class MultiConnectPoly(polygon.Polygon):
    # 求一系列未知的polygon组成 p=MultiConnectPoly(polygon1,polygon12,polygon13)
    def __init__(self, *args):
        self.outerLoop = list()
        self.innerLoop = list()

    # 返回所有的点,遍历list,然后get vertices
    def setOuterLoop(self, *args):
        if len(args) > 2:
            flag = True
            for i in args:
                if not isinstance(i, Point):
                    flag = false
                    break
            if flag:
                p = Polygon(*args)
                self.outerLoop.append(p)

        elif len(args) == 2:
            pass

        elif len(args) == 1:
            if isinstance(args[0], Polygon):
                self.outerLoop.append(args[0])

    # 另提供当个的点输入或polygon
    def addInnerLoop(self, *args):
        # 为点集
        if len(args) > 2:
            flag = True
            for i in args:
                if not isinstance(i, Point):
                    flag = false
                    break

            if flag:
                tag = True
                p = Polygon(*args)
                # 是否在outer里
                if not self.__isEnclose(p, self.outerLoop[0]):
                    tag = False
                # 是否有交集
                if self.__isintersection(p, 1):
                    tag = False
                # 是否有子包围
                for i in self.innerLoop:
                    if not self.__isAllout(p, i):
                        tag = False
                    if not self.__isAllout(i, p):
                        tag = False
                # 符合条件加入inner
                if tag:
                    self.innerLoop.append(p)

        elif len(args) == 2:
            pass
        elif len(args) == 1:
            if isinstance(args[0], Polygon):
                p = args[0]
                tag = True
                # 是否在outer里  return False 表示存在点在外环外面，既不能加入
                if not self.__isEnclose(p, self.outerLoop[0]):
                    tag = False
                # 是否有交集,rutern false 表示无交集
                if self.__isintersection(p, 1):
                    tag = False
                # 是否有子包围
                for i in self.innerLoop:
                    if not self.__isAllout(p, i):
                        tag = False
                    if not self.__isAllout(i, p):
                        tag = False
                # 符合条件加入inner
                if tag:
                    self.innerLoop.append(p)
            else:
                # 提示不符合要求
                pass

    # 判断是否有交集，type=0,于outer比较，=1与inner  True 表示有交点
    def __isintersection(self, polygon, type):
        flag = False
        # 不是Polygon就为False,不进行一下的验算了
        if not isinstance(polygon, Polygon):
            assert False

        if type == 0:
            for i in self.outerLoop:
                res = polygon.intersection(i)
                if res != []:
                    flag = True
                    # break
        if type == 1:
            if self.innerLoop == []:
                flag = False
            else:
                for i in self.innerLoop:
                    res = polygon.intersection(i)
                    if res != []:
                        flag = True
                    # break
        return flag

    # 判断加入的inner的否都在outer的里面 True 表示quan包围
    def __isEnclose(self, subpoly, poly):
        if poly is None:
            # Alert()警告无外环
            assert False

        # 并且 2个几何集无交集
        if self.__isintersection(subpoly, 0):
            return False

        if isinstance(subpoly, Polygon) and isinstance(poly, Polygon):
            p_list = subpoly.vertices
            for i in p_list:
                # 如果子几何体存在一个i点不在环内，既子几何不全被包围
                if not poly.encloses_point(i):

                    return False

        return True

    def __isAllout(self,subpoly, poly):
        if poly is None:
            # Alert()警告无外环
            assert False

        if isinstance(subpoly, Polygon) and isinstance(poly, Polygon):
            p_list = subpoly.vertices
            for i in p_list:
                # 如果子几何体存在一个i点不在环内，既子几何不全被包围
                if poly.encloses_point(i):
                    return False
        return True

    # 去除内部环
    def deleInnerloop(self, ID):
        pass

    def getpolylist(self):
        return self.outerLoop, self.innerLoop


# 参数化的截面对象,是各种特殊梁的基类
class ABKSectionByParameter(MultiConnectPoly):
    def __new__(cls, *args, **kwargs):
        cls._shape = None
        cls.Points = list()
        return Polygon.__new__(cls, *args, **kwargs)
    '''
    def __init__(self):
        super(ABKSectionByParameter, self).__init__(None)
        self.cen_Points = dict()
        self._shape = None
    '''
    def getShape(self):
        return self._shape

    # 坐标点的移动，生产新的截面
    def moveCoor(self, x_var, y_var):
        '''
        if self._args is None:
            # Alert
            assert False
        # 将每一个点移动x，y
        for i in range(0,len(self._args)):
            self._args[i].translate(x_var,y_var)
            #i.x = i.x + x_var
            #i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:#{1:(a,b,c)}
            for key,value in self.cen_Points.items():
                self.cen_Points[key]=(value[0]+x_var,value[1]+y_var,value[2])
        '''
        pass

    def getPoints(self):
        return self.Points

    # 画圆弧标注
    def dieArc(self,key,value,theta):
        # 圆心指向末点
            ps = [value[0], value[1]]
            r = value[2]
            theta *= pi / 180.0
            pe = [ps[0]+r*cos(theta),ps[1]+r*cos(theta)]
            # pe = [self._args[key].x, self._args[key].y]
            path = [ps, pe]
            p = ((ps[0]+pe[0])/2.,(ps[1]+pe[1])/2.)

            self._dimen.append(path)
            self._text[p] = 'R'+str(value[2])

    # 画直线的标注
    def dieLine(self, p0, p1, offsetting, direction):
        # 看是水平标注，还是垂直标注。
        if p0.y == p1.y:
            # 水平的
            if direction:
                path = [[p0.x,p0.y],[p0.x,p0.y-1.2*offsetting],[p0.x, p0.y-offsetting], [p1.x, p1.y-offsetting],[p1.x,p1.y-1.2*offsetting],[p1.x,p1.y]]
            else:
                path = [[p0.x,p0.y],[p0.x,p0.y+1.2*offsetting],[p0.x, p0.y+offsetting], [p1.x, p1.y+offsetting],[p1.x,p1.y+1.2*offsetting],[p1.x,p1.y]]
        if p0.x == p1.x:
            # 垂直的
            if direction:
                path = [[p0.x,p0.y],[p0.x-1.2*offsetting,p0.y],[p0.x-offsetting, p0.y], [p1.x-offsetting, p1.y],[p1.x-1.2*offsetting,p1.y],[p1.x,p1.y]]
            else:
                path = [[p0.x,p0.y],[p0.x+1.2*offsetting,p0.y],[p0.x+offsetting, p0.y], [p1.x+offsetting, p1.y],[p1.x+1.2*offsetting,p1.y],[p1.x,p1.y]]

        m = path[2]
        n = path[3]
        if p0.x == p1.x:
            if direction:
                p = ((m[0]+n[0])/2.-offsetting, (m[1]+n[1])/2.)
            else:
                p = ((m[0]+n[0])/2.+offsetting*0.5, (m[1]+n[1])/2.)
        if p0.y == p1.y:
            # 垂直的
            if direction:
                p = ((m[0]+n[0])/2., (m[1]+n[1])/2.-offsetting)
            else:
                p = ((m[0]+n[0])/2., (m[1]+n[1])/2.+offsetting*0.5)
        distance = p0.distance(p1)
        self._text[p] = distance
        self._dimen.append(path)

# 直角钢
class rightAngleSection(ABKSectionByParameter):
    # 根据给的尺寸构造出数据结构

    # 把尺寸的计算放到参数类里面来。

    def __new__(cls, *args):  # b1, b2, d1, d2, r
        cls.cen_Points = dict()

        cls._dimen = list()
        cls._text = dict()

        Check = True
        for i in args:
            if isinstance(i, Point):
                Check = False
                break

        if Check:
            if args[0] > 0 and args[1] > 0 and args[2] > 0 and args[3] > 0 and args[4] > 0:
                if args[2] + args[4] <= args[1] and args[3] + args[4] <= args[0]:
                    p0 = Point(0, 0)
                    p1 = Point(args[0], 0)
                    #p2 = Point(args[0]-0.2*args[2], 0.6*args[2])
                    #p3 = Point(args[0]-args[2], args[2])

                    p2 = Point(args[0], args[2])
                    p3 = Point(args[3] + args[4], args[2])
                    p4 = Point(args[3], args[2] + args[4])
                    #p6 = Point(args[3], args[1] - args[3])
                    #p7 = Point(0.6*args[3], args[1] - 0.2*args[3])

                    p5 = Point(args[3], args[1])
                    p6 = Point(0, args[1])

                    cls.cen_Points[3] = (args[3] + args[4], args[2] + args[4], args[4], True)

                    return Polygon.__new__(cls, p0, p1,p2, p3, p4, p5, p6)
            else:
                # Alert
                assert False
        else:
            return Polygon.__new__(cls, *args)

    def __init__(self, *args):
        super(rightAngleSection, self).__init__(*args)
        self.getDimension(*args)

    @property
    def cen_ArcPoint(self):
        return self.cen_Points

    # 获取尺寸
    def getDimension(self,*args):
        offsetting = args[0]*2/25
        points = self._args
        arcs = self.cen_ArcPoint
        #把２　变成比例
        self.dieLine(points[0], points[1], offsetting, True)
        self.dieLine(points[1], points[2], offsetting, False)
        self.dieLine(points[5], points[6], offsetting, False)
        self.dieLine(points[6], points[0], offsetting, True)
        for key,value in arcs.items():
            if key == 3:
                self.dieArc(key,value,225)

    # 坐标点的移动，生产新的截面
    def moveCoor(self, x_var, y_var):
        newPoint = list()
        newArcPoint = dict()
        if self._args is None:
            # Alert
            assert False
        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            x = self._args[i].x + x_var
            y = self._args[i].y + y_var
            p = Point(x, y)
            newPoint.append(p)
        print newPoint
        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                newArcPoint[key] = (value[0] + x_var, value[1] + y_var, value[2], value[3])
        print newArcPoint
        res = rightAngleSection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 旋转之后，产生新的截面
    def rotate(self, angle, pt=None):
        '''
        绕点按angle逆旋转之后，产生新的截面
        :param angle: 旋转的角度
        :param pt: 所绕的点
        :return: 返回旋转之后的新截面
        '''
        newPoint = list()
        newArcPoint = dict()
        if self._args is None:
            # Alert
            assert False
        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            p = self._args[i].rotate(angle,pt)
            newPoint.append(p)

        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                p = Point(value[0],value[1]).rotate(angle,pt)
                newArcPoint[key] = (p.x, p.y, value[2], value[3])

        res = rightAngleSection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 输入一个3x3的矩阵，可以对空间内的截面进行平移和旋转
    def transform(self,x_var,y_var,angle,pt=None):
        '''
        绕pt旋转angle后，平移（x_var,y_var)
        :param matrix:输入一个3x3的矩阵，可以对空间内的截面进行平移和旋转
        :return:
        '''
        newPoint = list()
        newArcPoint = dict()

        if self._args is None:
            # Alert
            assert False

        # 计算出变换矩阵
        m = self.__getMatrix(x_var,y_var,angle,pt)

        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            p = self._args[i].transform(m)
            newPoint.append(p)

        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                p = Point(value[0],value[1]).transform(m)
                newArcPoint[key] = (p.x, p.y, value[2], value[3])

        res = rightAngleSection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 获取变换的矩阵
    def __getMatrix(self,x_var,y_var,angle,pt):

        m0 = Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ x_var, y_var, 1]])

        m1= Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ -pt.x, -pt.y, 1]])

        m2=Matrix([
        [ cos(angle), sin(angle), 0],
        [-sin(angle), cos(angle), 0],
        [ 0, 0, 1]])

        #xuanz
        m3 = Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ pt.x, pt.y, 1]])

        m=m0*m1*m2*m3

        return m

    # 计算出数据结构
    def __getDataResource(self, b1, b2, d1, d2, r):
        pass


# 工型钢
class ISection(ABKSectionByParameter):
    # 根据给的尺寸构造出数据结构
    def __new__(cls, *args):  # h=args[0], b=args[1], d=args[2], r=args[3], r1=args[4]
        cls.cen_Points = dict()
        cls._dimen = list()
        cls._text = dict()

        h = args[0]
        b = args[1]
        d = args[2]
        t = args[3]
        r = args[4]
        r1 = args[5]

        Check = True
        for i in args:
            if isinstance(i, Point):
                Check = False
                break

        if Check:
            alfa = atan(6)
            if h > 0 and b > 0 and d > 0 and r > 0 and r1 > 0:
                if h / 2. > r * sin(alfa) + b / 12. and d / 2 + r < b / 2. - r1:
                    # ~~~~~~~~~~~~~~~~~~ generate some points ~~~~~~~~~~~~~~
                    Points = list()
                    list1 = _calculatePoint(h, b, d, t, r, r1,6., 4)
                    # p0,c0
                    Points.append(list1[0])
                    cls.cen_Points[0] = (list1[5].x, list1[5].y, r1,True)
                    # p1
                    Points.append(list1[1])
                    # p2
                    Points.append(list1[2])
                    # p3 c1
                    Points.append(list1[3])
                    cls.cen_Points[3] = (list1[6].x, list1[6].y, r,True)
                    # p4
                    Points.append(list1[4])

                    list1 = _calculatePoint(h, b, d,t, r, r1,6., 1)
                    # p5
                    Points.append(list1[4])
                    cls.cen_Points[5] = (list1[6].x, list1[6].y, r,True)

                    # p6
                    Points.append(list1[3])
                    #cls.cen_Points[5] = (list1[5].x, list1[5].y, r)

                    # p7
                    Points.append(list1[2])
                    # p8
                    Points.append(list1[1])
                    cls.cen_Points[8] = (list1[5].x, list1[5].y, r1,True)
                    # p9
                    Points.append(list1[0])
                    #cls.cen_Points[9] = (list1[5].x, list1[5].y, r1)

                    list1 = _calculatePoint(h, b, d,t, r, r1,6., 2)
                    # p10
                    Points.append(list1[0])
                    cls.cen_Points[10] = (list1[5].x, list1[5].y, r1,True)
                    # p11
                    Points.append(list1[1])
                    # p12
                    Points.append(list1[2])
                    # p13
                    Points.append(list1[3])
                    # cls.cen_Points[10] = (list1[5].x, list1[5].y, r)
                    cls.cen_Points[13] = (list1[6].x, list1[6].y, r,True)
                    # p14
                    Points.append(list1[4])

                    list1 = _calculatePoint(h, b, d,t, r, r1,6., 3)
                    # p15
                    Points.append(list1[4])
                    cls.cen_Points[15] = (list1[6].x, list1[6].y, r,True)

                    # p16
                    Points.append(list1[3])
                    #cls.cen_Points[13] = (list1[5].x, list1[5].y, r)
                    # p17
                    Points.append(list1[2])
                    # p18
                    Points.append(list1[1])
                    cls.cen_Points[18] = (list1[5].x, list1[5].y, r1,True)
                    # p19
                    Points.append(list1[0])
                    #cls.cen_Points[19] = (list1[5].x, list1[5].y, r1)

                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ end ~~~~~~~~~~~~~~~~~~~~~~~
                    return entity.GeometryEntity.__new__(cls, *Points)
            else:
                # Alert
                assert False
        else:
            return entity.GeometryEntity.__new__(cls, *args)

    def __init__(self, *args):
        super(ISection, self).__init__(*args)
        self.getDimension(*args)

    @property
    def cen_ArcPoint(self):
        return self.cen_Points

    # 获取尺寸
    def getDimension(self,*args):
        h = args[0]
        b = args[1]
        d = args[2]
        t = args[3]
        r = args[4]
        r1 = args[5]

        offsetting = h*2/50
        points = self._args
        arcs = self.cen_ArcPoint

        self.dieLine(points[10], points[19], offsetting, True)
        self.dieLine(points[19],points[0],offsetting,True)
        point1 = Point(d/2,-h/5)
        point2 = Point(-d/2,-h/5)
        self.dieLine(point1, point2,offsetting, True)
        point3 = Point((b-d)/4, h/2)
        point4 = Point((b-d)/4, h/2-t)
        self.dieLine(point3, point4, 4*offsetting, False)

        #self.__dieLine(points[6], points[0], 2, True)
        for key ,value in arcs.items():
            if key == 0:
                self.dieArc(key,value,45)
            if key == 3:
                self.dieArc(key,value,225)

    # 坐标点的移动，生产新的截面
    def moveCoor(self, x_var, y_var):
        newPoint = list()
        newArcPoint = dict()
        if self._args is None:
            # Alert
            assert False
        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            x = self._args[i].x + x_var
            y = self._args[i].y + y_var
            p = Point(x, y)
            newPoint.append(p)
        # print newPoint
        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                newArcPoint[key] = (value[0] + x_var, value[1] + y_var, value[2], value[3])
        # print newArcPoint
        res = ISection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 旋转之后，产生新的截面
    def rotate(self, angle, pt=None):
        '''
        绕点按angle逆旋转之后，产生新的截面
        :param angle: 旋转的角度
        :param pt: 所绕的点
        :return: 返回旋转之后的新截面
        '''
        newPoint = list()
        newArcPoint = dict()
        if self._args is None:
            # Alert
            assert False
        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            p = self._args[i].rotate(angle,pt)
            newPoint.append(p)

        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                p = Point(value[0],value[1]).rotate(angle,pt)
                newArcPoint[key] = (p.x, p.y, value[2], value[3])

        res = ISection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 输入一个3x3的矩阵，可以对空间内的截面进行平移和旋转
    def transform(self,x_var,y_var,angle,pt=None):
        '''
        绕pt旋转angle后，平移（x_var,y_var)
        :param matrix:输入一个3x3的矩阵，可以对空间内的截面进行平移和旋转
        :return:
        '''
        newPoint = list()
        newArcPoint = dict()

        if self._args is None:
            # Alert
            assert False

        # 计算出变换矩阵
        m = self.__getMatrix(x_var,y_var,angle,pt)

        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            p = self._args[i].transform(m)
            newPoint.append(p)

        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                p = Point(value[0],value[1]).transform(m)
                newArcPoint[key] = (p.x, p.y, value[2], value[3])

        res = ISection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 获取变换的矩阵
    def __getMatrix(self,x_var,y_var,angle,pt):

        m0 = Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ x_var, y_var, 1]])

        m1= Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ -pt.x, -pt.y, 1]])

        m2=Matrix([
        [ cos(angle), sin(angle), 0],
        [-sin(angle), cos(angle), 0],
        [ 0, 0, 1]])

        #xuanz
        m3 = Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ pt.x, pt.y, 1]])

        m=m0*m1*m2*m3

        return m

    # 计算出数据结构
    def __getDataResource(self, h, b, d, t, r, r1):
        pass


# 槽钢
class grooveSection(ABKSectionByParameter):
     # 根据给的尺寸构造出数据结构
    def __new__(cls, *args):  # h=args[0], b=args[1], d=args[2], r=args[3], r1=args[4]
        cls.cen_Points = dict()
        cls._dimen = list()
        cls._text = dict()
        h = args[0]
        b = args[1]
        d = args[2]
        t = args[3]
        r = args[4]
        r1 = args[5]

        Check = True
        for i in args:
            if isinstance(i, Point):
                Check = False
                break

        if Check:
            alfa = atan(10)
            if h > 0 and b > 0 and d > 0 and r > 0 and r1 > 0:
                if h / 2. > r * sin(alfa) + b / 10. and d + r < b - r1:
                    # ~~~~~~~~~~~~~~~~~~ generate some points ~~~~~~~~~~~~~~
                    Points = list()
                    list1 = _calculatePoint(h, 2*b, 2*d, t, r, r1, 10., 4)
                    # p0,c0
                    Points.append(list1[0])
                    # cls.cen_Points[0] = (list1[5].x, list1[5].y, r1, True)
                    # p1
                    Points.append(list1[1])
                    # p2
                    Points.append(list1[2])
                    # p3 c1
                    Points.append(list1[3])
                    cls.cen_Points[3] = (list1[6].x, list1[6].y, r, True)
                    # p4
                    Points.append(list1[4])

                    list1 = _calculatePoint(h, 2*b, 2*d, t, r, r1, 10., 1)
                    # p5
                    Points.append(list1[4])
                    cls.cen_Points[5] = (list1[6].x, list1[6].y, r, True)

                    # p6
                    Points.append(list1[3])
                    # cls.cen_Points[5] = (list1[5].x, list1[5].y, r)

                    # p7
                    Points.append(list1[2])
                    # p8
                    Points.append(list1[1])
                    # cls.cen_Points[8] = (list1[5].x, list1[5].y, r1, True)
                    # p9
                    Points.append(list1[0])
                    # cls.cen_Points[9] = (list1[5].x, list1[5].y, r1)
                    Points.append(Point(0, h / 2.))
                    Points.append(Point(0, - h / 2))
                    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ end ~~~~~~~~~~~~~~~~~~~~~~~
                    return entity.GeometryEntity.__new__(cls, *Points)
            else:
                # Alert
                assert False
        else:
            return entity.GeometryEntity.__new__(cls, *args)

    def __init__(self, *args):
        super(grooveSection, self).__init__(*args)
        self.getDimension(*args)

    @property
    def cen_ArcPoint(self):
        return self.cen_Points

    def getDimension(self,*args):
        h = args[0]
        b = args[1]
        d = args[2]
        t = args[3]
        r = args[4]
        r1 = args[5]

        offsetting = h*2/50
        points = self._args
        arcs = self.cen_ArcPoint

        self.dieLine(points[10], points[11], offsetting, True)
        self.dieLine(points[11], points[0], offsetting, True)
        point1 = Point(d, -h/5)
        point2 = Point(0, -h/5)
        self.dieLine(point1, point2,offsetting, True)
        point3 = Point((b-d)/2, h/2)
        point4 = Point((b-d)/2, h/2-t)
        self.dieLine(point3, point4, 4*offsetting, False)

        #self.__dieLine(points[6], points[0], 2, True)
        for key ,value in arcs.items():
            if key == 0:
                self.dieArc(key,value,45)
            if key == 3:
                self.dieArc(key,value,225)

    # 坐标点的移动，生产新的截面
    def moveCoor(self, x_var, y_var):
        newPoint = list()
        newArcPoint = dict()
        if self._args is None:
            # Alert
            assert False
        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            x = self._args[i].x + x_var
            y = self._args[i].y + y_var
            p = Point(x, y)
            newPoint.append(p)
        # print newPoint
        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                newArcPoint[key] = (value[0] + x_var, value[1] + y_var, value[2], value[3])
        # print newArcPoint
        res = grooveSection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 旋转之后，产生新的截面
    def rotate(self, angle, pt=None):
        '''
        绕点按angle逆旋转之后，产生新的截面
        :param angle: 旋转的角度
        :param pt: 所绕的点
        :return: 返回旋转之后的新截面
        '''
        newPoint = list()
        newArcPoint = dict()
        if self._args is None:
            # Alert
            assert False
        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            p = self._args[i].rotate(angle,pt)
            newPoint.append(p)

        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                p = Point(value[0],value[1]).rotate(angle,pt)
                newArcPoint[key] = (p.x, p.y, value[2], value[3])

        res = grooveSection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 输入一个3x3的矩阵，可以对空间内的截面进行平移和旋转
    def transform(self,x_var,y_var,angle,pt=None):
        '''
        绕pt旋转angle后，平移（x_var,y_var)
        :param matrix:输入一个3x3的矩阵，可以对空间内的截面进行平移和旋转
        :return:
        '''
        newPoint = list()
        newArcPoint = dict()

        if self._args is None:
            # Alert
            assert False

        # 计算出变换矩阵
        m = self.__getMatrix(x_var,y_var,angle,pt)

        # 将每一个点移动x，y
        for i in range(0, len(self._args)):
            # 不知道怎样是否可以真正的修改值
            p = self._args[i].transform(m)
            newPoint.append(p)

        # i.x = i.x + x_var
        # i.y = i.y + y_var
        # 如果有圆心，圆心的值也修改掉
        if self.cen_Points is not None:  # {1:(a,b,c)}
            for key, value in self.cen_Points.items():
                p = Point(value[0],value[1]).transform(m)
                newArcPoint[key] = (p.x, p.y, value[2], value[3])

        res = grooveSection(*newPoint)
        res.cen_Points = newArcPoint
        return res

    # 获取变换的矩阵
    def __getMatrix(self,x_var,y_var,angle,pt):

        m0 = Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ x_var, y_var, 1]])

        m1= Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ -pt.x, -pt.y, 1]])

        m2=Matrix([
        [ cos(angle), sin(angle), 0],
        [-sin(angle), cos(angle), 0],
        [ 0, 0, 1]])

        #xuanz
        m3 = Matrix([
        [ 1, 0, 0],
        [0, 1, 0],
        [ pt.x, pt.y, 1]])

        m=m0*m1*m2*m3

        return m

    # 计算出数据结构
    def __getDataResource(self, h, b, d, t, r, r1):
        pass


# 组合截面
class compoundSection(object):
    def __init__(self):
        self.dataResource = list()

    # 加入截面
    def addToSections(self, sections):
        # 判断sections是否为复连通
        if not isinstance(sections, MultiConnectPoly):
            return False
        # 是否存在交点
        # outerloop 只有一个
        # poly = sections.outerLoop[0]
        # for i in self.dataResource:
        #    res = poly.intersection(i.outerLoop)
        #    if res != []:
        #        return False
        # appendlist
        self.dataResource.append(sections)
        return True

    # 去除截面
    def deleSectionByNum(self, ID):
        if ID < len(self.dataResource):
            self.dataResource.pop(ID)

    # 获取组合之后的新截面
    def getSections(self):
        return self.dataResource


# 截面库
class SectionLibrary:
    def __init__(self):
        self.count = 0
        self.libSection = list()

    # 获取当前的count
    def __getcount(self):
        return self.count

    # 添加截面
    def addSection(self, sections):
        i = self.__getcount() + 1
        list1 = [i, sections]
        self.count += 1

    # 删除截面
    def deleteSectionByID(self, ID):
        if ID > 0 and ID < len(self.libSection):
            self.libSection.pop(ID)

    # 查看截面
    def selectSection(self, ID):
        # 与界面相关
        pass

    # 生成文件,包含截面库中的信息
    def genFile(self):
        pass


# 计算对象，专门用于计算截面的各种几何特征
class GeoCalculator(object):
    def __init__(self, section):

        self.section = section

        self._args = dict()

    # 预处理得出点集和圆弧集
    def __preProcess(self,section):
        points_list = section.vertices
        if isinstance(section,ABKSectionByParameter):
            ArcPoint_list = section.cen_Points
        else:
            ArcPoint_list = dict()
        return points_list, ArcPoint_list

    # 求解poly
    def Solve(self):
        # 判断是不是polygon
        if isinstance(self.section, Polygon):
            if isinstance(self.section, MultiConnectPoly):
                self._args = self.__MpSolve(self.section)
            # 就是真正的Polygon
            else:
                pass
        if isinstance(self.section,compoundSection):
            self._args = self.__comSolve(self.section)

    # 求解组合截面的poly
    def __comSolve(self,section):
        temp_dict = dict()
        for i in section.dataResource:
            temp_dict = self.__sumValue(temp_dict, self.__MpSolve(i),0)
        return temp_dict

    # 求解复联通的poly
    def __MpSolve(self,sections):
        temp_dict = dict()
        if sections.outerLoop !=[]:
            for i in sections.outerLoop:
                temp_dict = self.__sumValue(temp_dict,self.__SolveSingleSection(i),0)
            if sections.innerLoop !=[]:
                for i in self.section.innerLoop:
                    temp_dict = self.__sumValue(temp_dict,self.__SolveSingleSection(i),1)
            # 说明内环为空的
            else:
                pass
        else:
            # 复连通外环为空，就是空集或是参数化截面
            if isinstance(sections,ABKSectionByParameter):
                temp_dict = self.__SolveSingleSection(sections)
            else:
                assert False

        return temp_dict

    # 对所有单连通值进行求和
    def __sumValue(self,_argsDict,valueDict,type):
        for key,value in valueDict.items():
            if isinstance(value,float):
                if key in _argsDict:
                    if type == 0:
                        _argsDict[key] += value
                    if type == 1:
                        _argsDict[key] -= value
                else:
                    _argsDict[key] = value
            # 是一个[x_var,y_var]
            if isinstance(value, list):
                if key in _argsDict:
                    if type == 0:
                        _argsDict[key] = [_argsDict[key][0]+value[0], _argsDict[key][1]+value[1]]
                    if type == 1:
                        _argsDict[key] = [_argsDict[key][0]-value[0], _argsDict[key][1]-value[1]]
                else:
                    _argsDict[key] = [value[0],value[1]]

        return _argsDict

    # 求解单连通的几何性质：
    def __SolveSingleSection(self,section):
        # 预处理
        para = self.__preProcess(section)
        a = para[0]
        point = para[1]
        # 求出来的值放到一个字典中：
        singleSectionDict=dict()
        singleSectionDict['Area'] = float(self.__getGeoAttribute(a, point, 0))
        singleSectionDict['Sx'] = float(self.__getGeoAttribute(a, point, 1))
        singleSectionDict['Sy'] = float(self.__getGeoAttribute(a, point, 1, 'y'))
        singleSectionDict['Ix'] = float(self.__getGeoAttribute(a, point, 2))
        singleSectionDict['Iy'] = float(self.__getGeoAttribute(a, point, 2, 'y'))
        singleSectionDict['Ixy'] = float(self.__getGeoAttribute(a, point, 3))
        singleSectionDict['centroid'] = self.__getcentroid(a, point)
        singleSectionDict['tan_alfa'] = float(self.__getalfa(a, point))
        singleSectionDict['ix'] = float(self.__geti(a, point))
        singleSectionDict['iy'] = float(self.__geti(a, point, 'y'))

        return singleSectionDict

    # 求面积
    def Area(self):
        if 'Area' in self._args:
            return self._args['Area']
        else:
            return None

    # 求中心
    def Centroid(self):
        if 'centroid' in self._args:
            return self._args['centroid']
        else:
            return None

    # 求静矩
    def Sx(self):
        if 'Sx' in self._args:
            return self._args['Sx']
        else:
            return None

    # 求惯性矩
    def Ix(self):
        if 'Ix' in self._args:
            return self._args['Ix']
        else:
            return None

    # 求静矩
    def Sy(self):
        if 'Sy' in self._args:
            return self._args['Sy']
        else:
            return None

    # 求惯性矩
    def Iy(self):
        if 'Iy' in self._args:
            return self._args['Iy']
        else:
            return None

    #
    def Ixy(self):
        if 'Ixy' in self._args:
            return self._args['Ixy']
        else:
            return None

    def tan_alfa(self):
        if 'tan_alfa' in self._args:
            return self._args['tan_alfa']
        else:
            return None

    # 求惯性半径
    def ix(self):
        if 'ix' in self._args:
            return self._args['ix']
        else:
            return None

    def iy(self):
        if 'iy' in self._args:
            return self._args['iy']
        else:
            return None

    # 求a
    def __getalfa(self, a, point):
        if 'Ixy' in self._args:
            if self._args['Ixy'] is not None:
                Ixy = self._args['Ixy']
        else:
            Ixy = self.__getGeoAttribute(a, point, 3)

        if 'Ix' in self._args:
            if self._args['Ix'] is not None:
                Ix = self._args['Ix']
        else:
            Ix = self.__getGeoAttribute(a, point, 2)

        if 'Iy' in self._args:
            if self._args['Iy'] is not None:
                Iy = self._args['Iy']
        else:
            Iy = self.__getGeoAttribute(a, point, 2, 'y')

        if Iy - Ix == 0:
            alfa = pi / 4
        else:
            res = 2 * Ixy / (Iy - Ix)
            res = atan(res)
            alfa = (res) / 2.
        return alfa

    def __getcentroid(self, a, point):
        if 'Sx' in self._args:
            if self._args['Sx'] is not None:
                Sx = self._args['Sx']
        else:
            Sx = self.__getGeoAttribute(a, point, 1)

        if 'Sy' in self._args:
            if self._args['Sy'] is not None:
                Sy = self._args['Sy']
        else:
            Sy = self.__getGeoAttribute(a, point, 1, 'y')

        if 'Area' in self._args:
            if self._args['Area'] is not None:
                Area = self._args['Area']
        else:
            Area = self.__getGeoAttribute(a, point, 0)
        x_ave = Sy / Area
        y_ave = Sx / Area
        return [x_ave, y_ave]

    def __geti(self, a, point, axis='x'):
        if 'Ix' in self._args:
            if self._args['Ix'] is not None:
                Ix = self._args['Ix']
        else:
            Ix = self.__getGeoAttribute(a, point, 2)

        if 'Iy' in self._args:
            if self._args['Iy'] is not None:
                Iy = self._args['Iy']
        else:
            Iy = self.__getGeoAttribute(a, point, 2, 'y')

        if 'Area' in self._args:
            if self._args['Area'] is not None:
                Area = self._args['Area']
        else:
            Area = self.__getGeoAttribute(a, point, 0)
        if axis == 'x':
            ix = sqrt(Ix / Area)
            return ix
        elif axis == 'y':
            iy = sqrt(Iy / Area)
            return iy
        else:
            assert False

    # 求各种几何量
    def __getGeoAttribute(self, points, flag, type, axis='x',arc_type=True):
        sum1 = 0.0
        res = 0.0
        tag = 0
        x0 = 0.0
        y0 = 0.0
        r = 0.0
        a = 0.0
        b = 0.0
        for i in range(0, len(points)):
            if i < len(points) - 1:
                p0 = points[i]
                p1 = points[i + 1]
            else:
                p0 = points[len(points) - 1]
                p1 = points[0]
            xi = float(p0.x)
            yi = float(p0.y)
            xi1 = float(p1.x)
            yi1 = float(p1.y)
            if i in flag:  # is arc
                tuple1 = flag.get(i)
                x0 = tuple1[0]
                y0 = tuple1[1]
                r = tuple1[2]
                # 默认为TRUE
                if tuple1[3] is not None:
                    arc_type = tuple1[3]

                if xi == xi1 and yi == yi1:
                    a = 0
                    b = 2 * math.pi
                else:
                    a = self.__getAngle(x0, y0, xi, yi)
                    b = self.__getAngle(x0, y0, xi1, yi1)

                if arc_type:
                    if a==0:
                        if abs(a-b)>= math.pi:
                            a = 2*math.pi
                    if b==0:
                        if abs(a-b)>= math.pi:
                            b = 2*math.pi
                else:
                    assert False

                tag = 1
            if type == 0:
                if (tag == 1):
                    res = self.__CurvePA(xi, yi, xi1, yi1, x0, y0, r, a, b)
                    tag = 0
                else:
                    res = self.__LinePA(xi, yi, xi1, yi1)
            elif type == 1:
                if axis == 'x':
                    if (tag == 1):
                        res = self.__CurvePSx(xi, yi, xi1, yi1, x0, y0, r, a, b)
                        tag = 0
                    else:
                        res = self.__LinePSx(xi, yi, xi1, yi1)
                if axis == 'y':
                    if (tag == 1):
                        res = self.__CurvePSy(xi, yi, xi1, yi1, x0, y0, r, a, b)
                        tag = 0
                    else:
                        res = self.__LinePSy(xi, yi, xi1, yi1)
            elif type == 2:
                if axis == 'x':
                    if (tag == 1):
                        res = self.__CurvePIx(xi, yi, xi1, yi1, x0, y0, r, a, b)
                        tag = 0
                    else:
                        res = self.__LinePIx(xi, yi, xi1, yi1)
                if axis == 'y':
                    if (tag == 1):
                        res = self.__CurvePIy(xi, yi, xi1, yi1, x0, y0, r, a, b)
                        tag = 0
                    else:
                        res = self.__LinePIy(xi, yi, xi1, yi1)
            elif type == 3:
                if (tag == 1):
                    res = self.__CurvePIxy(xi, yi, xi1, yi1, x0, y0, r, a, b)
                    tag = 0
                else:
                    res = self.__LinePIxy(xi, yi, xi1, yi1)
            sum1 = sum1 + res
        return sum1

    def __LinePIxy(self, xi, yi, xi1, yi1):  # ,x0=0.0,y0=0.0,a=0.0,b=0.0
        res = ((xi - xi1) * (
            3 * xi * yi ** 2 + xi * yi1 ** 2 + xi1 * yi ** 2 + 3 * xi1 * yi1 ** 2 + 2 * xi * yi * yi1 + 2 * xi1 * yi * yi1)) / 24.  # Ixy
        return res

    def __LinePIx(self, xi, yi, xi1, yi1):
        res = ((yi ** 2 + yi1 ** 2) * (yi + yi1) * (xi - xi1)) / 12.
        return res

    def __LinePIy(self, xi, yi, xi1, yi1):
        res = ((xi ** 2 + xi1 ** 2) * (xi + xi1) * (yi1 - yi)) / 12.
        return res

    def __LinePSx(self, xi, yi, xi1, yi1):
        res = ((xi - xi1) * (yi * yi + yi * yi1 + yi1 * yi1)) / 6.
        return res

    def __LinePSy(self, xi, yi, xi1, yi1):
        res = ((yi1 - yi) * (xi * xi + xi * xi1 + xi1 * xi1)) / 6.
        return res

    def __LinePA(self, xi, yi, xi1, yi1):
        res = ((yi + yi1) * (xi - xi1)) / 2
        return res

    def __CurvePA(self, xi, yi, xi1, yi1, x0, y0, r, a, b):
        res = (r * r * (b - a)) / 2
        res = res + (yi - y0) * (xi - x0) / 2 - (yi1 - y0) * (xi1 - x0) / 2 + y0 * (xi - xi1)
        return res

    def __CurvePSx(self, xi, yi, xi1, yi1, x0, y0, r, a, b):
        res = (r * r / 2.) * (xi - xi1) + ((xi1 - x0) ** 3) / 6. - ((xi - x0) ** 3) / 6. + (y0 * y0 * (xi - xi1)) / 2.
        res = res + (r * r / 2.) * y0 * (b - a) - (y0 * (yi1 - y0) * (xi1 - x0)) / 2. + (y0 * (yi - y0) * (xi - x0))/2.
        return res

    def __CurvePSy(self, xi, yi, xi1, yi1, x0, y0, r, a, b):
        res = (r * r / 2.) * (yi - yi1) + ((yi1 - y0) ** 3) / 6. - ((yi - y0) ** 3) / 6. + (x0 * x0 * (yi - yi1)) / 2.
        res = res + (r * r / 2.) * x0 * (a - b) - (x0 * (xi1 - x0) * (yi1 - y0)) / 2. + (x0 * (xi - x0) * (yi - y0))/2.
        res = res * (-1)
        return res

    def __CurvePIx(self, xi, yi, xi1, yi1, x0, y0, r, a, b):
        res = ((yi - y0) * (xi - x0) ** 3) / 8. - ((yi - y0) ** 3 * (xi - x0)) / 8. - ((yi1 - y0) * (
            xi1 - x0) ** 3) / 8. + ((yi1 - y0) ** 3 * (xi1 - x0)) / 8.
        res = res + (r ** 2 * (yi1 - y0) * (xi1 - x0)) / 2. - (r ** 2 * (yi - y0) * (xi - x0)) / 2.
        res = res + ((3. / 8.) * r ** 4 + (3. / 2.) * r ** 2 * y0 ** 2) * (a - b) + (y0 ** 2 + (
            9. / 4.) * r ** 2) * y0 * (xi1 - xi)
        res = res + 1.5 * y0 ** 2 * (yi1 - y0) * (xi1 - x0) - 1.5 * y0 ** 2 * (yi - y0) * (xi - x0)
        res = res + y0 * (xi - x0) ** 3 - 0.75 * r ** 2 * y0 * (xi - x0) - y0 * (xi1 - x0) ** 3 + 0.75 * r ** 2 * y0 * (
            xi1 - x0)
        res = res * (-1. / 3.)
        return res

    def __CurvePIy(self, xi, yi, xi1, yi1, x0, y0, r, a, b):
        res = ((xi - x0) * (yi - y0) ** 3) / 8. - ((xi - x0) ** 3 * (yi - y0)) / 8. - ((xi1 - x0) * (
            yi1 - y0) ** 3) / 8. + ((xi1 - x0) ** 3 * (yi1 - y0)) / 8.
        res = res + (r ** 2 * (xi1 - x0) * (yi1 - y0)) / 2. - (r ** 2 * (xi - x0) * (yi - y0)) / 2.
        res = res + ((3. / 8.) * r ** 4 + (3. / 2.) * r ** 2 * x0 ** 2) * (b - a) + (x0 ** 2 + (
            9. / 4.) * r ** 2) * x0 * (yi1 - yi)
        res = res + 1.5 * x0 ** 2 * (xi1 - x0) * (yi1 - y0) - 1.5 * x0 ** 2 * (xi - x0) * (yi - y0)
        res = res + x0 * (yi - y0) ** 3 - 0.75 * r ** 2 * x0 * (yi - y0) - x0 * (yi1 - y0) ** 3 + 0.75 * r ** 2 * x0 * (
            yi1 - y0)
        res = res * (1. / 3.)
        return res

    def __CurvePIxy(self, xi, yi, xi1, yi1, x0, y0, r, a, b):
        res = ((yi - y0) ** 2 * (3 * (yi - y0) ** 2 + 6 * y0 ** 2 + 8 * y0 * (yi - y0))) / (-12.) + ((yi1 - y0) ** 2 * (
            3 * (yi1 - y0) ** 2 + 6 * y0 ** 2 + 8 * y0 * (yi1 - y0))) / 12.

        res = res + ((xi - x0) ** 3 / (3 * r) - (xi1 - x0) ** 3 / (3 * r) + (r + y0 ** 2 / r) * (xi1 - xi) + r * y0 * (a - b) - (y0 / r) * (xi - x0) * (yi - y0) + (y0 / r) * (xi1 - x0) * (yi1 - y0)) * (- r * x0)

        res = 0.5 * res

        return res

    def __getAngle(self, x0, y0, x1, y1):
        if x0 != x1:
            k = (y1 - y0) / (x1 - x0)
        else:
            k = 'inf'
        if k == 'inf':
            # xi=xi1
            if y1 > y0:
                theate = math.pi / 2.
            if y1 < y0:
                theate = (3 * math.pi) / 2.
            if y1 == y0:
                assert False
        else:
            theate = math.atan(k)
            if x1 < x0:
                theate = theate + math.pi

        # 把范围控制在（0，2pi）之间
        while theate > 2 * math.pi:
            theate = theate - 2 * math.pi
        while theate < 0:
            theate =theate + 2 * math.pi

        return theate


def _calculatePoint(h, b, d,t, r,r1,k,type):
        p0 = Point(b / 2., -h / 2.)

        res = _getcp(h, b, d, t, r, r1,k)
        c0 = res[0]
        p1 = res[1]

        alfa = atan(k)
        #c0 = Point(b / 2. - r1, -h / 2.)
        #p1 = Point(c0.x + r1 * cos(alfa), c0.y + r1 * sin(alfa))

        p2 = Point(b/4+d/4, -h/2 + t)

        p3 = _getPoint(d, r, p2.x, p2.y, k,alfa)

        c1 = Point(p3.x + r * cos(alfa), p3.y + r * sin(alfa))

        p4 = Point(d / 2, c1.y)

        list1 = [p0, p1, p2, p3, p4, c0, c1]
        newlist = list()
        if type == 1:
            for i in list1:
                # y变负号，x不变
                #i.y = -i.y
                p = i.scale(1,-1)
                newlist.append(p)
        elif type == 2:
            for i in list1:
                # x,y变负号
                p = i.scale(-1,-1)
                newlist.append(p)
        elif type == 3:
            for i in list1:
                # x变负号，y不变
                p = i.scale(-1,1)
                newlist.append(p)
        elif type == 4:
            newlist = list1
        else:
            # Alert
            assert False
        return newlist

# 获取特殊点的坐标
def _getPoint(d, r, px, py, k,alfa):
    b = py + px / k
    x0 = d/2. + r - r * cos(alfa)
    y0 = x0 / (-k) + b

    return Point(x0, y0)

def _getcp(h, b, d,t, r,r1,k):
    if k == 6.:
        x0 = (73*b)/148 + d/148 + (6*t)/37 - 3*(((d - b + 24*t)*(b - d - 24*t + 296*r1*cos(6)))/5476)**(1/2)
        y0 = (3*d)/74 - (3*b)/74 - h/2 + (36*t)/37 + (((d - b + 24*t)*(b - d - 24*t + 296*r1*cos(6)))/5476)**(1/2)/2
        c0 = -(b**2 + h**2 - 24*h*x0 + 4*h*y0 - 4*x0**2 - 48*x0*y0 + 4*y0**2)/(4*(6*h - b + 2*x0 + 12*y0))
        c1 = -(3*b**2 - 12*b*x0 + 2*b*y0 + 3*h**2 + 12*x0**2 - 4*x0*y0 - 12*y0**2)/(2*(6*h - b + 2*x0 + 12*y0))
    if k == 10.:
        x0 = (201*b)/404 + d/404 + (10*t)/101 - 5*(((d - b + 40*t)*(b - d - 40*t + 808*r*cos(10)))/40804)**(1/2)
        y0 = (5*d)/202 - (5*b)/202 - h/2 + (100*t)/101 + (((d - b + 40*t)*(b - d - 40*t + 808*r*cos(10)))/40804)**(1/2)/2
        c0 = -(b**2 + h**2 - 40*h*x0 + 4*h*y0 - 4*x0**2 - 80*x0*y0 + 4*y0**2)/(4*(10*h - b + 2*x0 + 20*y0))
        c1 = -(5*b**2 - 20*b*x0 + 2*b*y0 + 5*h**2 + 20*x0**2 - 4*x0*y0 - 20*y0**2)/(2*(10*h - b + 2*x0 + 20*y0))
        # y = ((0.16-0.045)/(-350))*h+0.165
        # x0 = x0*(1+y)

    return Point(c0, c1), Point(x0, y0)