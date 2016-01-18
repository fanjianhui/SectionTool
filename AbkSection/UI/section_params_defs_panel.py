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

        # Ĭ�Ͻ�����״
        self._section_type = u'ֱ�Ǹ�'

        # ���������һ��ֻ��
        for irow in range(self.m_grid_params_defs.GetNumberRows()):
            self.m_grid_params_defs.SetReadOnly(irow, 0, True)

        self.grid_value = {
                           u'ֱ�Ǹ�': ['�߿��1', '�߿��2', '�ߺ��1', '�ߺ��2', '��Բ���뾶'],
                           u'���ָ�': ['�߶�', '�ȿ��', '�����', 'ƽ���Ⱥ��', '��Բ���뾶', '�Ƕ�Բ���뾶' ],
                           u'�۸�':   ['�߶�', '�ȿ��', '�����', 'ƽ���Ⱥ��', '��Բ���뾶', '�Ƕ�Բ���뾶' ],
                           u'C�͸�':  ['�߶�', '�߿��1', '�ߺ��1', '�����', '�ߺ��2', '�߿��2'],
                           u'T�͸�':  ['�߶�', '�ߺ��1', '�ߺ��2', '�߿��1', '�߿��2'],
                           u'ñ�͸�': ['�߶�', '�ű߿��', '�űߺ��', '�Ⱥ��', '�����', 'ͷ�߿��', 'ͷ���'],
                           u'J�͸�':  ['�߶�', '�ߺ��1', '�ߺ��2', '�ߺ��3', '�߿��1', '�߿��2', '�߿��3']
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