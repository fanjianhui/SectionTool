#!/usr/bin/env python
# -*- coding: GBK -*-
import wx
from wx.lib.floatcanvas import FloatCanvas
from section_params_defs_panel_base import SectionParamsDefsPanelBase
# from demo_panel_frame import DemoPanelFrame
from wxmplot import PlotPanel
from ABKSectionPoint import *
from DrawSection import DrawGeometry
from wxmplot import PlotApp
from numpy import linspace, sin, cos, random
import matplotlib.path as mpath

class SectoinParamsDefsPanel (SectionParamsDefsPanelBase):
    def __init__(self, parent):
        SectionParamsDefsPanelBase.__init__(self, parent)
        # 用于存放 solve之后的值
        self._args = dict()

        self.plotpanel = PlotPanel(self.m_panel_canvas, size=(300, 300), fontsize=5)
        self.plotpanel.BuildPanel()

        # 默认截面形状
        self._section_type = u'直角钢'

        # 截面参数第一列只读
        for irow in range(self.m_grid_params_defs.GetNumberRows()):
            self.m_grid_params_defs.SetReadOnly(irow, 0, True)

        self.grid_value = {
                           u'直角钢': ['边宽度1', '边宽度2', '边厚度1', '边厚度2', '内圆弧半径'],
                           u'工字钢': ['高度', '腿宽度', '腰厚度', '平均腿厚度', '内圆弧半径', '角端圆弧半径' ],
                           u'槽钢':   ['高度', '腿宽度', '腰厚度', '平均腿厚度', '内圆弧半径', '角端圆弧半径' ],
                           #u'C型钢':  ['高度', '边宽度1', '边厚度1', '腰厚度', '边厚度2', '边宽度2'],
                           u'T型钢':  ['高度', '边宽度1', '边宽度2', '边厚度1', '边厚度2'],
                           u'帽型钢': ['高度', '脚边宽度', '头边宽度', '腿倾角', '脚边厚度', '腿厚度', '头厚度'],
                           u'J型钢':  ['高度', '边宽度1', '边宽度2', '边宽度3', '边厚度1', '边厚度2', '边厚度3']
                          }

        for num in range(len(self.grid_value[self._section_type])):
            self.m_grid_params_defs.SetCellValue(num, 0, self.grid_value[self._section_type][num])

    def OnSelectSectionType(self, event):
        self._section_type = self.m_choice_section_type.GetStringSelection()
        section_parameter_name = self.grid_value[self._section_type]
        self.m_grid_params_defs.ClearGrid()
        for name_num in range(len(section_parameter_name)):
            self.m_grid_params_defs.SetCellValue(name_num, 0, section_parameter_name[name_num])

    def m_btn_calculationOnButtonClick( self, event ):
        # 点击btn之后，获得传入的参数。
        # 通过获得的参数生成出截面对象。
        # 通过截面计算，得到几何数值
        # 通过Draw对象画图，画出几何图像。
        _args = list()
        for num in range(len(self.grid_value[self._section_type])):
            _args.append(float(self.m_grid_params_defs.GetCellValue(num, 1)))

        sectionType = self._section_type

        if sectionType == u"工字钢":
            section = ISection(*_args)
        elif sectionType == u"直角钢":
            section = rightAngleSection(*_args)
        elif sectionType == u"槽钢":
            section = grooveSection(*_args)
        #elif sectionType == u"C型钢":
            #pass
        elif sectionType == u"T型钢":
            section = TshapeSection(*_args)
        elif sectionType == u"J型钢":
            section = JshapeSection(*_args)
        elif sectionType == u"帽型钢":
            section = NshapeSection(*_args)

        geo = GeoCalculator(section)
        geo.Solve()
        self._args = geo._args
        if "Area" in self._args:
            if self._args['Area'] < 0.0000001:
                res = 0
            else:
                res = self._args['Area']
            self.m_propertyGridItem2.SetValue(str(res))
        if "Sx" in self._args:
            if self._args['Sx'] < 0.0000001:
                res = 0
            else:
                res = self._args['Sx']
            self.m_propertyGridItem3.SetValue(str(res))
        if "Sy" in self._args:
            if self._args['Sy'] < 0.0000001:
                res = 0
            else:
                res = self._args['Sy']
            self.m_propertyGridItem42.SetValue(str(res))
        if "Ix" in self._args:
            if self._args['Ix'] < 0.0000001:
                res = 0
            else:
                res = self._args['Ix']
            self.m_propertyGridItem4.SetValue(str(res))
        if "Iy" in self._args:
            if self._args['Iy'] < 0.0000001:
                res = 0
            else:
                res = self._args['Iy']
            self.m_propertyGridItem5.SetValue(str(res))
        if "Ixy" in self._args:
            if self._args['Ixy'] < 0.0000001:
                res = 0
            else:
                res = self._args['Ixy']
            self.m_propertyGridItem7.SetValue(str(res))
        if "centroid" in self._args:
            res = self._args['centroid']

            if res[0] < 0.0000001:
                res = [0, res[1]]
            if res[1] < 0.0000001:
                res = [res[0], 0]

            self.m_propertyGridItem8.SetValue(str(res))
        if "tan_alfa" in self._args:
            if self._args['tan_alfa'] < 0.0000001:
                res = 0
            else:
                res = self._args['tan_alfa']

            self.m_propertyGridItem9.SetValue(str(res))
        if "ix" in self._args:
            if self._args['ix'] < 0.0000001:
                res = 0
            else:
                res = self._args['ix']
            self.m_propertyGridItem61.SetValue(str(res))
        if "iy" in self._args:
            if self._args['iy'] < 0.0000001:
                res = 0
            else:
                res = self._args['iy']
            self.m_propertyGridItem62.SetValue(str(res))

        Path = DrawGeometry(section)
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

    def m_btn_calculationOnSetFocus( self, event ):
        print "on btn_Set Focus!"

if __name__ == '__main__':
    app = wx.App(False)
    dlg = SectoinParamsDefsPanel(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()