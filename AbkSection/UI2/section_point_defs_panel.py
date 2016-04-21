#!/usr/bin/env python
# -*- coding: GBK -*-
import wx
import os
import xlsxwriter
import datetime
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
        # ���ڴ�� solve֮���ֵ
        self._args = dict()
        self.point_list = list()

        # ����һ������ͨ��ȫ�ֱ���
        self.MP = MultiConnectPoly()
        # ����һ�����Ͻ����ȫ�ֱ���
        self.Comp = compoundSection()

        # ����ֻ�ǳ�ʼ���˻���
        self.plotpanel = PlotPanel(self.m_panel1, size=(300, 300), fontsize=5)
        self.plotpanel.BuildPanel()

    def m_btn_InsertOnButtonClick( self, event ):
        # ��input�����ĵ����븴��ͨ������,������buffet������
        x = self.m_textCtrl8.Value
        y = self.m_textCtrl9.Value

        p = Point(x, y)
        self.point_list.append(p)

        string = '(' + x + ',' + y + ')'
        self.m_listBox2.Append(string)

    def btn_addMultiPropOnButtonClick( self, event ):
        # Ĭ�ϵ�һ���ǷŽ�Outer�ģ��������ľͷ���inner��
        if len(self.MP.outerLoop) == 0 :
            _args = self.point_list
            self.MP.setOuterLoop(*_args)
        else:
            _args = self.point_list
            self.MP.addInnerLoop(*_args)

        # procedure -- remove all items of list��as well as the data of point list
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
        # �����ֵ䣬���ϱ�ע
        for key, value in Path._text.items():
            x = key[0]
            y = key[1]
            self.plotpanel.add_text(str(value), x, y, size=4)

    def btn_genCompOnButtonClick( self, event ):
        # �����2������ͨ�Ļ��Ͱ�����ͬʱ��������Ȼ��ֱ�Ӽ��㣬���������һ��������յ�btn

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
        # �����ֵ䣬���ϱ�ע
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
        # �����ֵ䣬���ϱ�ע
        for key, value in Path._text.items():
            x = key[0]
            y = key[1]
            self.plotpanel.add_text(str(value), x, y, size=4)

    def btn_genMultiPropOnButtonClick( self, event ):
        # ��MP�Ž�����Ȼ����գ�ͼ��Ҳ���
        self.Comp.addToSections(self.MP)
        n = len(self.Comp.dataResource)
        string = '��' + str(n) + '������'
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
        # ��Ҫ��listpoint���ȥ��

    def btn_PrintDataOnclick( self, event ):
        # procedure 1:����UI2.png,2:
        path = os.path.abspath(os.curdir)+'//section.png'
        if hasattr(self, 'fig'):
            self.plotpanel.fig.savefig(path, transparent=False, dpi=300)
        else:
            self.plotpanel.canvas.print_figure(path, transparent=False, dpi=300)
        if (path.find(self.plotpanel.launch_dir) ==  0):
            path = path[len(self.plotpanel.launch_dir)+1:]
        self.plotpanel.write_message('Saved plot to %s' % path)

        self.filePrint()

    def filePrint(self):
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook('reportData.xlsx')
        worksheet = workbook.add_worksheet()

        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)

        ID = self.__getcurrentTimeID()

        worksheet.write('A2', 'ID:')
        worksheet.write('B2', ID)

        worksheet.write('A3', 'Area:')
        worksheet.write('B3', self._args['Area'])

        worksheet.write('A4', 'Sx')
        worksheet.write('B4', self._args['Sx'])

        worksheet.write('A5', 'Sy')
        worksheet.write('B5', self._args['Sy'])

        worksheet.write('A6', 'Ix')
        worksheet.write('B6', self._args['Ix'])

        worksheet.write('A7', 'Iy')
        worksheet.write('B7', self._args['Iy'])

        worksheet.write('A8', 'Ixy')
        worksheet.write('B8', self._args['Ixy'])

        worksheet.write('A9', 'centroid')
        worksheet.write('B9', str(self._args['centroid']))

        worksheet.write('A10', 'tan_alfa')
        worksheet.write('B10', str(self._args['tan_alfa']))

        worksheet.write('A11', 'ix')
        worksheet.write('B11', self._args['ix'])

        worksheet.write('A12', 'iy')
        worksheet.write('B12', self._args['iy'])

        worksheet.insert_image('F2', 'section.png')

        workbook.close()

    def __getcurrentTimeID(self):
        currenttime = datetime.datetime.now()
        currenttime = str(currenttime.isoformat())
        currenttime = currenttime[0:len(currenttime)-6]
        for c in '-:.T': # "
            currenttime = currenttime.replace(c, '')

        return currenttime

    def btn_insertToLibOnButtonClick( self, event ):
        # ������Ϣ��ŵ����ļ��С�
        # workbook = xlsxwriter.Workbook('Library.xlsx')
        # �������裺1��section��ͼƬsave��lib�У�������ΪID.png
        # �������ݿ⡣ֻ�д�ӡ��ʱ������ļ���һ���Դ�ӡ������

        ID = self.__getcurrentTimeID()

        ImageURL = ID+'.png'

        lib = SectionLibrary()

        lib.addSection(ID,ImageURL,self._args)

        # Ȼ���ٰ�ͼƬ�浽ImageLIB��
        shutil.copy('section.png',"..\\ImageLib\\"+ImageURL)

        # Ȼ����updateһ�´�������е���Ϣ���ļ���
        self.__updateLibFile(lib)

    def __updateLibFile(self,lib):
        workbook = xlsxwriter.Workbook('LibInfo.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)

        # ��Ҫ��ȡinfo
        info = lib.selectAllSection()

        self.__worksheet_write(worksheet,info)

        workbook.close()

    def __worksheet_write(self,ws,info):
        count = 0
        for singleSec in info:
            # ����
            ws.write('A'+ str(count*15+1), 'ID')
            ws.write('B'+ str(count*15+1), singleSec[0])

            ws.insert_image('F'+str(count*15+1), "..\\ImageLib\\" + singleSec[1])

            ws.write('A'+ str(count*15+2), 'Area')
            ws.write('B'+ str(count*15+2), singleSec[2])

            ws.write('A'+ str(count*15+3), 'Sx')
            ws.write('B'+ str(count*15+3), singleSec[3])

            ws.write('A'+ str(count*15+4), 'Sy')
            ws.write('B'+ str(count*15+4),singleSec[4])

            ws.write('A'+ str(count*15+5), 'Iy')
            ws.write('B'+ str(count*15+5),singleSec[5])

            ws.write('A'+ str(count*15+6), 'Ix')
            ws.write('B'+ str(count*15+6),singleSec[6])

            ws.write('A'+ str(count*15+7), 'Ixy')
            ws.write('B'+ str(count*15+7),singleSec[7])

            ws.write('A'+ str(count*15+8), 'Centroid')
            ws.write('B'+ str(count*15+8),singleSec[8])

            ws.write('A'+ str(count*15+9), 'Angle')
            ws.write('B'+ str(count*15+9),singleSec[9])

            ws.write('A'+ str(count*15+10), 'ix')
            ws.write('B'+ str(count*15+10),singleSec[10])

            ws.write('A'+ str(count*15+11), 'iy')
            ws.write('B'+ str(count*15+11), singleSec[11])

            count = count+1

    def checkLibOnButtonClick( self, event ):
        lib = SectionLibrary()
        self.__updateLibFile(lib)
        os.system("LibInfo.xlsx")


if __name__ == '__main__':
    app = wx.App(False)
    dlg = SectoinPointDefsPanel(None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()
