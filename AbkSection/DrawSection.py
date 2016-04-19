## -*- coding: utf-8 -*-
import math
from matplotlib.path import Path
from ABKSectionPoint import *
import numpy as np
from wxmplot import PlotApp

class DrawGeometry(object):
    def __init__(self,section=None):
        # the some handles as the calculation
        self.section = section
        # 用于存放输出的
        self._paths = list()
        self._dimen = list()
        self._text = dict()

    # 预处理得出点集和圆弧集
    def __preProcess(self,section):
        points_list = section.vertices
        if isinstance(section,ABKSectionByParameter):
            ArcPoint_list = section.cen_ArcPoint
        else:
            ArcPoint_list = dict()
        return points_list, ArcPoint_list

    # 求解poly
    def Draw(self):
        # 判断是不是polygon
        if isinstance(self.section, Polygon):
            if isinstance(self.section, MultiConnectPoly):
                self.__mpDraw(self.section)
            # 就是真正的Polygon
            else:
                pass
        if isinstance(self.section,compoundSection):
            self.__comDraw(self.section)

    # 复连通的截面path
    def __mpDraw(self,sections):
        if sections.outerLoop !=[]:
            for i in sections.outerLoop:
                self._paths.append(self.singleDraw(i))
            if sections.innerLoop !=[]:
                for i in sections.innerLoop:
                    self._paths.append(self.singleDraw(i))
            # 说明内环为空的
            else:
                pass
        else:
            # 复连通外环为空，就是空集或是参数化截面
            if isinstance(sections, ABKSectionByParameter):
                self._paths.append(self.singleDraw(sections))
                for i in sections._dimen:
                    self._dimen.append(i)
                self._text = sections._text
            else:
                assert False

    # 组合截面的path,
    def __comDraw(self,section):
        for i in section.dataResource:
            self.__mpDraw(i)

    # 画的是单连通的path
    def singleDraw(self,section):
        # 处理圆弧边和回程线段就可以了
        para = self.__preProcess(section)

        points = para[0]
        flag = para[1]

        arc_type = True
        _path = list()
        # 在进行遍历之前就把第一个点添加进来
        _path.append([points[0].x,points[0].y])
        for i in range(0, len(points)):
            # 默认不倒序
            order_tag = False
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
                if xi==xi1 and yi==yi1:
                    # start point and end point coincide ,we defined it as a circle.
                    a=0
                    b=2*np.pi
                else:
                    a = self.getAngle(x0,y0,xi,yi)
                    b = self.getAngle(x0,y0,xi1,yi1)
                    if arc_type:
                        if a==0:
                            if abs(a-b)>= np.pi:
                                a = 2*np.pi
                        if b==0:
                            if abs(a-b)>= np.pi:
                                b = 2*np.pi
                    else:
                        if a==0:
                            if abs(a-b) <= np.pi:
                                a = 2*np.pi
                        if b==0:
                            if abs(a-b) <= np.pi:
                                b = 2*np.pi

                    # 至此仅仅只是把角度的范围变成了[0.2pi]

                    if arc_type:
                        if abs(a-b)<np.pi:
                            if a>b:
                                t = b
                                b = a
                                a = t
                                order_tag = True

                        if abs(a-b)>=np.pi:
                            if a<b:
                                t = b
                                b = a
                                a = t
                                order_tag = True
                    else:
                        if abs(a-b)<np.pi:
                            if a<b:
                                t = b
                                b = a
                                a = t
                                order_tag = True
                        if abs(a-b)>=np.pi:
                            if a>b:
                                t = b
                                b = a
                                a = t
                                order_tag = True

                    v = self.arc_path(a,b,[x0,y0],r)

                    if order_tag:
                        temp = list()
                        for i in v:
                            temp.append(i)
                        temp.reverse()
                        for i in temp:
                            _path.append(i)
                    else:
                        for i in v:
                            _path.append(i)
            else:
                # 如果不是圆弧的话直接就是把点放进去就可以了
                v=[xi1,yi1]
                _path.append(v)

        return _path

    def arc_path(self,theta1,theta2,center,r):
        if abs((theta2 - theta1) - 2*np.pi) <= 1e-12:
            theta1, theta2 = 0, 2*np.pi

        arc = self.__arc(theta1, theta2)

        v = np.vstack([arc.vertices])

        v *= r
        v += np.asarray(center)

        return v

    def __arc(self, theta1, theta2,n=None):
        # degrees to radians
        # theta1 *= np.pi / 180.0
        # theta2 *= np.pi / 180.0

        twopi = np.pi * 2.0
        halfpi = np.pi * 0.5

        eta1 = np.arctan2(np.sin(theta1), np.cos(theta1))
        eta2 = np.arctan2(np.sin(theta2), np.cos(theta2))
        eta2 -= twopi * np.floor((eta2 - eta1) / twopi)

        # number of curve segments to make
        if n is None:
            n = int(2 ** np.ceil((eta2 - eta1) / halfpi)+10)
        if n < 1:
            raise ValueError("n must be >= 1 or None")

        deta = (eta2 - eta1) / n
        t = np.tan(0.5 * deta)
        alpha = np.sin(deta) * (np.sqrt(4.0 + 3.0 * t * t) - 1) / 3.0

        steps = np.linspace(eta1, eta2, n + 1, True)
        cos_eta = np.cos(steps)
        sin_eta = np.sin(steps)

        xA = cos_eta[:-1]
        yA = sin_eta[:-1]
        xA_dot = -yA
        yA_dot = xA

        xB = cos_eta[1:]
        yB = sin_eta[1:]
        xB_dot = -yB
        yB_dot = xB

        length = n * 3 + 1
        vertices = np.empty((length, 2), np.float_)
        codes = Path.CURVE4 * np.ones((length, ), Path.code_type)
        vertices[0] = [xA[0], yA[0]]
        codes[0] = Path.MOVETO
        vertex_offset = 1
        end = length

        vertices[vertex_offset:end:3, 0] = xA + alpha * xA_dot
        vertices[vertex_offset:end:3, 1] = yA + alpha * yA_dot
        vertices[vertex_offset+1:end:3, 0] = xB - alpha * xB_dot
        vertices[vertex_offset+1:end:3, 1] = yB - alpha * yB_dot
        vertices[vertex_offset+2:end:3, 0] = xB
        vertices[vertex_offset+2:end:3, 1] = yB

        return Path(vertices, codes, readonly=True)

    # 这里或的角度是[0,2pi）
    def getAngle(self,x0, y0, x1, y1):
        if x0 != x1:
            k = (y1 - y0) / (x1 - x0)
        else:
            k = 'inf'
        if k == 'inf':
            # xi=xi1
            if y1 > y0:
                theate = np.pi / 2.
            if y1 < y0:
                theate = (3 * np.pi) / 2.
            # The tow points coincide
            if y1 == y0:
                assert False
        else:
            theate = math.atan(k)
            if x1 < x0:
                theate = theate + np.pi

        while theate > 2 * np.pi:
            theate = theate - 2 * np.pi
        while theate < 0:
            theate =theate + 2 * np.pi

        return theate
