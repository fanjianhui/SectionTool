#!/usr/bin/env python
# -*- coding: GBK -*-
import wx
import os
from wx.lib.floatcanvas import FloatCanvas
from section_point_defs_panel_base import SectionPointDefsPanelBase
# from demo_panel_frame import DemoPanelFrame
from wxmplot import PlotPanel
from ABKSectionPoint import *
from DrawSection import DrawGeometry
from wxmplot import PlotApp
from numpy import linspace, sin, cos, random
import matplotlib.path as mpath

class SectoinPointDefsPanel (SectionPointDefsPanelBase):
    def __init__(self, parent):
        SectionPointDefsPanelBase.__init__(self, parent)
        # 用于存放 solve之后的值
        self._args = dict()
        self.point_list = list()

        # 这是一个复连通的全局变量
        self.MP = MultiConnectPoly()
        # 再来一个复合截面的全局变量
        self.Comp = compoundSection()

        # 仅仅只是初始化了画布
        self.plotpanel = PlotPanel(self.m_panel1, size=(300, 300), fontsize=5)
        self.plotpanel.BuildPanel()

    def m_btn_InsertOnButtonClick( self, event ):
        # 将input进来的点填入复连通截面中,并填入buffet数据中
        x = self.m_textCtrl8.Value
        y = self.m_textCtrl9.Value

        p = Point(x, y)
        self.point_list.append(p)

        string = '(' + x + ',' + y + ')'
        self.m_listBox2.Append(string)

    def btn_addMultiPropOnButtonClick( self, event ):
        # 默认第一个是放进Outer的，后面来的就放在inner里
        if len(self.MP.outerLoop) == 0 :
            _args = self.point_list
            self.MP.setOuterLoop(*_args)
        else:
            _args = self.point_list
            self.MP.addInnerLoop(*_args)

        # procedure -- remove all items of list，as well as the data of point list
        self.m_listBox2.Clear()
        self.point_list = []

        Path = DrawGeometry(self.MP)
        Path.Draw()

        self.plotpanel.clear()
        for i in Path._paths:
                m,n=zip(*i)
                self.plotpanel.oplot(m,n,fullbox=False,axes_style='open')
        for i in Path._dimen:
            m, n = zip(*i)
            self.plotpanel.oplot(m,n,fullbox=False,axes_style='open', linewidth=1, color='green')
        # 遍历字典，画上标注
        for key, value in Path._text.items():
            x = key[0]
            y = key[1]
            self.plotpanel.add_text(str(value), x, y, size=4)

    def btn_genCompOnButtonClick( self, event ):
        # 如果有2个复连通的话就把他们同时画出来。然后直接计算，边上再添加一个数据清空的btn

        self.ShowResult(self.Comp)

        Comp_Path = DrawGeometry(self.Comp)
        Comp_Path.Draw()

        self.plotpanel.clear()
        for i in Comp_Path._paths:
                m,n=zip(*i)
                self.plotpanel.oplot(m,n,fullbox=False,axes_style='open')
        for i in Comp_Path._dimen:
            m, n = zip(*i)
            self.plotpanel.oplot(m,n,fullbox=False,axes_style='open', linewidth=1, color='green')
        # 遍历字典，画上标注
        for key, value in Comp_Path._text.items():
            x = key[0]
            y = key[1]
            self.plotpanel.add_text(str(value), x, y, size=4)

    def ShowResult(self, section):
        geo = GeoCalculator(section)
        geo.Solve()
        self._args = geo._args
        if "Area" in self._args:
            if abs(self._args['Area']) < 0.0000001:
                res = 0
            else:
                res = self._args['Area']
            self.m_propertyGridItem2.SetValue(str(res))
        if "Sx" in self._args:
            #if abs(self._args['Sx']) < 0.0000001:
               # res = 0
            #else:
            res = self._args['Sx']
            self.m_propertyGridItem3.SetValue(str(res))
        if "Sy" in self._args:
            #if abs(self._args['Sy']) < 0.0000001:
                #res = 0
            #else:
            res = self._args['Sy']
            self.m_propertyGridItem42.SetValue(str(res))
        if "Ix" in self._args:
            if abs(self._args['Ix']) < 0.0000001:
                res = 0
            else:
                res = self._args['Ix']
            self.m_propertyGridItem4.SetValue(str(res))
        if "Iy" in self._args:
            if abs(self._args['Iy']) < 0.0000001:
                res = 0
            else:
                res = self._args['Iy']
            self.m_propertyGridItem5.SetValue(str(res))
        if "Ixy" in self._args:
            #if abs(self._args['Ixy']) < 0.0000001:
                #res = 0
            #else:
            res = self._args['Ixy']
            self.m_propertyGridItem7.SetValue(str(res))
        if "centroid" in self._args:
            res = self._args['centroid']

            #if abs(res[0]) < 0.0000001:
                #res = [0, res[1]]
            #if abs(res[1]) < 0.0000001:
                #res = [res[0], 0]
            self.m_propertyGridItem8.SetValue(str(res))
        if "tan_alfa" in self._args:
            #if abs(self._args['tan_alfa']) < 0.0000001:
                #res = 0
            #else:
            res = self._args['tan_alfa']

            self.m_propertyGridItem9.SetValue(str(res))
        if "ix" in self._args:
            if abs(self._args['ix']) < 0.0000001:
                res = 0
            else:
                res = self._args['ix']
            self.m_propertyGridItem61.SetValue(str(res))
        if "iy" in self._args:
            if abs(self._args['iy']) < 0.0000001:
                res = 0
            else:
                res = self._args['iy']
            self.m_propertyGridItem62.SetValue(str(res))

    def showItemOnDClick( self, event ):
        print 'double _click'
        n = self.m_listBox3.GetSelection()
        multisection = self.Comp.dataResource[n]

        self.ShowResult(multisection)

        Path = DrawGeometry(multisection)
        Path.Draw()

        self.plotpanel.clear()
        for i in Path._paths:
                m,n=zip(*i)
                self.plotpanel.oplot(m,n,fullbox=False,axes_style='open')
        for i in Path._dimen:
            m, n = zip(*i)
            self.plotpanel.oplot(m,n,fullbox=False,axes_style='open', linewidth=1, color='green')
        # 遍历字典，画上标注
        for key, value in Path._text.items():
            x = key[0]
            y = key[1]
            self.plotpanel.add_text(str(value), x, y, size=4)

    def btn_genMultiPropOnButtonClick( self, event ):
        # 将MP放进来，然后清空，图像也清空
        self.Comp.addToSections(self.MP)
        n = len(self.Comp.dataResource)
        string = '第' + str(n) + '个截面'
        self.m_listBox3.Append(string)
        self.plotpanel.clear()
        self.MP = MultiConnectPoly()

    def btn_DataClearOnClickButton( self, event ):
        self.MP = MultiConnectPoly()
        self.Comp = compoundSection()
        self.m_listBox3.Clear()
        self.plotpanel.BuildPanel()
        self.m_textCtrl8.SetValue("")
        self.m_textCtrl9.SetValue("")
        self.m_propertyGridItem2.SetValue('0')
        self.m_propertyGridItem3.SetValue('0')
        self.m_propertyGridItem42.SetValue('0')
        self.m_propertyGridItem4.SetValue('0')
        self.m_propertyGridItem5.SetValue('0')
        self.m_propertyGridItem7.SetValue('0')
        self.m_propertyGridItem8.SetValue('[0,0]')
        self.m_propertyGridItem9.SetValue('0')
        self.m_propertyGridItem61.SetValue('0')
        self.m_propertyGridItem62.SetValue('0')

    def del_OnRightClick( self, event ):
        n = self.m_listBox2.GetSelection()
        self.m_listBox2.Delete(n)
        self.point_list.pop(n)
        # 还要把listpoint里的去掉

    def btn_PrintDataOnclick( self, event ):
        self.plotpanel.save_figure(os.path.abspath(os.curdir),transparent=False,dpi=300)


if __name__ == '__main__':
    app = wx.App(False)
    dlg = SectoinPointDefsPanel(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
