#!/usr/bin/env python
# -*- coding: GBK -*-
import wx
from wx.lib.floatcanvas import FloatCanvas
from section_params_defs_panel_base import SectionParamsDefsPanelBase
# from demo_panel_frame import DemoPanelFrame
from wxmplot import PlotPanel
from numpy import linspace, sin, cos, random
import matplotlib.path as mpath

class SectoinParamsDefsPanel (SectionParamsDefsPanelBase):
    def __init__(self, parent):
        SectionParamsDefsPanelBase.__init__(self, parent)

        Path = mpath.Path
        path_data = [
                        (Path.MOVETO, (1.58, -2.57)),
                        (Path.CURVE4, (0.35, -1.1)),
                        (Path.CURVE4, (-1.75, 2.0)),
                        (Path.CURVE4, (0.375, 2.0)),
                        (Path.LINETO, (0.85, 1.15)),
                        (Path.CURVE4, (2.2, 3.2)),
                        (Path.CURVE4, (3, 0.05)),
                        (Path.CURVE4, (2.0, -0.5)),
                        (Path.CLOSEPOLY, (1.58, -2.57)),
                    ]
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)
        x, y = zip(*path.vertices)

        self.plotpanel = PlotPanel(self.m_panel_canvas, size=(300, 220),fontsize=5)
        self.plotpanel.BuildPanel()

        self.plotpanel.plot(x,y,title='section' ,fontsize=5,label='a')

        # 默认截面形状
        self._section_type = u'直角钢'

        # 截面参数第一列只读
        for irow in range(self.m_grid_params_defs.GetNumberRows()):
            self.m_grid_params_defs.SetReadOnly(irow, 0, True)

        self.grid_value = {
                           u'直角钢': ['边宽度1', '边宽度2', '边厚度1', '边厚度2', '内圆弧半径'],
                           u'工字钢': ['高度', '腿宽度', '腰厚度', '平均腿厚度', '内圆弧半径', '角端圆弧半径' ],
                           u'槽钢':   ['高度', '腿宽度', '腰厚度', '平均腿厚度', '内圆弧半径', '角端圆弧半径' ],
                           u'C型钢':  ['高度', '边宽度1', '边厚度1', '腰厚度', '边厚度2', '边宽度2'],
                           u'T型钢':  ['高度', '边厚度1', '边厚度2', '边宽度1', '边宽度2'],
                           u'帽型钢': ['高度', '脚边宽度', '脚边厚度', '腿厚度', '腿倾角', '头边宽度', '头厚度'],
                           u'J型钢':  ['高度', '边厚度1', '边厚度2', '边厚度3', '边宽度1', '边宽度2', '边宽度3']
                          }

        for num in range(len(self.grid_value[self._section_type])):
            self.m_grid_params_defs.SetCellValue(num, 0, self.grid_value[self._section_type][num])


    def OnSelectSectionType(self, event):
        self._section_type = self.m_choice_section_type.GetStringSelection()

        section_parameter_name = self.grid_value[self._section_type]
        self.m_grid_params_defs.ClearGrid()
        for name_num in range(len(section_parameter_name)):
            self.m_grid_params_defs.SetCellValue(name_num, 0, section_parameter_name[name_num])


if __name__ == '__main__':
    app = wx.App(False)
    dlg = SectoinParamsDefsPanel(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()