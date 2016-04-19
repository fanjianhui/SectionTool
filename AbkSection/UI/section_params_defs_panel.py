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
        # ���ڴ�� solve֮���ֵ
        self._args = dict()

        self.plotpanel = PlotPanel(self.m_panel_canvas, size=(300, 300), fontsize=5)
        self.plotpanel.BuildPanel()

        # Ĭ�Ͻ�����״
        self._section_type = u'ֱ�Ǹ�'

        # ���������һ��ֻ��
        for irow in range(self.m_grid_params_defs.GetNumberRows()):
            self.m_grid_params_defs.SetReadOnly(irow, 0, True)

        self.grid_value = {
                           u'ֱ�Ǹ�': ['�߿��1', '�߿��2', '�ߺ��1', '�ߺ��2', '��Բ���뾶'],
                           u'���ָ�': ['�߶�', '�ȿ��', '�����', 'ƽ���Ⱥ��', '��Բ���뾶', '�Ƕ�Բ���뾶' ],
                           u'�۸�':   ['�߶�', '�ȿ��', '�����', 'ƽ���Ⱥ��', '��Բ���뾶', '�Ƕ�Բ���뾶' ],
                           #u'C�͸�':  ['�߶�', '�߿��1', '�ߺ��1', '�����', '�ߺ��2', '�߿��2'],
                           u'T�͸�':  ['�߶�', '�߿��1', '�߿��2', '�ߺ��1', '�ߺ��2'],
                           u'ñ�͸�': ['�߶�', '�ű߿��', 'ͷ�߿��', '�����', '�űߺ��', '�Ⱥ��', 'ͷ���'],
                           u'J�͸�':  ['�߶�', '�߿��1', '�߿��2', '�߿��3', '�ߺ��1', '�ߺ��2', '�ߺ��3']
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
        # ���btn֮�󣬻�ô���Ĳ�����
        # ͨ����õĲ������ɳ��������
        # ͨ��������㣬�õ�������ֵ
        # ͨ��Draw����ͼ����������ͼ��
        _args = list()
        for num in range(len(self.grid_value[self._section_type])):
            _args.append(float(self.m_grid_params_defs.GetCellValue(num, 1)))

        sectionType = self._section_type

        if sectionType == u"���ָ�":
            section = ISection(*_args)
        elif sectionType == u"ֱ�Ǹ�":
            section = rightAngleSection(*_args)
        elif sectionType == u"�۸�":
            section = grooveSection(*_args)
        #elif sectionType == u"C�͸�":
            #pass
        elif sectionType == u"T�͸�":
            section = TshapeSection(*_args)
        elif sectionType == u"J�͸�":
            section = JshapeSection(*_args)
        elif sectionType == u"ñ�͸�":
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
        # �����ֵ䣬���ϱ�ע
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