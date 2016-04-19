#!/usr/bin/env python
# -*- coding: GBK -*-
import wx
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
        # 仅仅只是初始化了画布
        self.plotpanel = PlotPanel(self.m_panel1, size=(300, 300), fontsize=5)
        self.plotpanel.BuildPanel()

    def m_btn_InsertOnButtonClick( self, event ):
        # 将input进来的点填入复连通截面中
        x = self.m_textCtrl8.Value
        y = self.m_textCtrl9.Value
        string = '(' + x + ',' + y + ')'
        self.m_listBox2.Append(string)

    def btn_genMultiPropOnButtonClick( self, event ):
        pass

    def btn_genCompOnButtonClick( self, event ):
        pass

    def btn_caculationOnButtonClick( self, event ):
        pass

if __name__ == '__main__':
    app = wx.App(False)
    dlg = SectoinPointDefsPanel(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
