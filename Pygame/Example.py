# -*- coding: utf-8 -*-
from ABKExcel import *
import wx


class App(wx.App):
    def OnInit(self):
        self.falg=False
        dlg=wx.MessageDialog(None,"Is this the coolest thing ever!",
        "MessageDialog",wx.YES_NO|wx.ICON_QUESTION)
        result=dlg.ShowModal()
        if result==wx.ID_YES:
            self.falg=True
        dlg.Destroy()
        return result


def test1():
    table_col = 9
    table_row = 9
    col_span = 2
    row_span = 2
    abs_col = 2

    table = ABKTable(row_span,col_span,table_row,table_col)

    table.absout_col = abs_col  # index,absoult_col默认为 0

    table.initStyleOn()

    table.setTitle('Multiple')  #设置标题

    table.setColor(2,2,'yellow')		#设置颜色

    table.setMerge(3,3,2,8)			#设置合并格
    table.setMerge(4,4,3,6)
    table.setMerge(5,8,6,6)
    table.setMerge(5,8,3,5)
    #现在有一个问题就是这个数字变成字符串就ok。。。

    fontstyle=['Bell MT',1,'blue',880]

    table.setFont(8,8,fontstyle) #设置字体

    for irow in xrange(1,table_row+1):
        for icol in xrange(1,table_col+1):
            value = irow*icol
            table.setCellData(irow,icol,value)

    sheet = ABKSheet('Book')

    sheet.addTable(table)   #将table添加到sheet中

    myExcel = ABKExcel()

    myExcel.WriteOn()        # 设置可写

    myExcel.open('Multi1.xls')  # 打开文件，如果没有就新建一个文件

    myExcel.addsheet(sheet) #添加sheet到excel中

    myExcel.save()			#保存文件

    myExcel.close()			#关闭文件

def test2():
    table_col = 9
    table_row = 9
    col_span = 2
    row_span = 2

    table = ABKTable(row_span,col_span,table_row,table_col)
    table.initStyleOn()
    table.table_index = row_span

    table.absout_col = col_span

    table.setTitle('Multiple')

    table.setColor(2,2,'rose')		#设置颜色

    table.setMerge(3,5,9,9)			#设置合并格

    #现在有一个问题就是这个数字变成字符串就ok。。。

    fontstyle=['Batang',1,'blue',880]
    table.setFont(8,8,fontstyle) #设置字体

    for irow in xrange(1,table_row+1):
        for icol in xrange(1,table_col+1):
            value = irow*icol
            table.setCellData(irow,icol,value)

    myExcel = ABKExcel() #create a object

    myExcel.open(r'C:\Users\hp\Desktop\ABKTt.xls') #open a Excel File

    name = 'Sheet1'

    myExcel.ReadOn()

    myExcel.readsheets(name)

    sheet = myExcel.getSheetByName(name)

    sheet.insertTable(table,0)

    myExcel.WriteOn()  # 是否允许对这个文件的修改

    # 如果名字重了，就提示是否保存...
    myExcel.save()

    myExcel.close()

def test3():
    myExcel = ABKExcel() #create a object
    myExcel.open(r'C:\Users\hp\Desktop\ABKTt.xls') #open a Excel File
    sheet_name_list = myExcel.get_sheet_names()

    for name in sheet_name_list:
        myExcel.ReadOn()
        myExcel.readsheets(name)
        sheet = myExcel.getSheetByName(name)
        Tables = sheet.getTables()


def test5():
    book = xlrd.open_workbook("Multi1.xls", formatting_info=True)
    sheets = book.sheet_names()
    print "sheets are:", sheets
    for index, sh in enumerate(sheets):
        sheet = book.sheet_by_index(index)
        print "Sheet:", sheet.name
        rows, cols = sheet.nrows, sheet.ncols
        print "Number of rows: %s Number of cols: %s" % (rows, cols)
        for row in range(rows):
            for col in range(cols):
                print "row, col is:", row+1, col+1
                thecell = sheet.cell(row, col)  # could get 'dump','value', 'xf_index'
                print "value= ",thecell.value

                xfx = sheet.cell_xf_index(row, col)
                xf = book.xf_list[xfx]
                font = book.font_list[xf.font_index]

                color = book.colour_map[font.colour_index]

                bgx = xf.background.pattern_colour_index
                #cl=xf.font.color_index
                # fmt = xf.format
                print "bgx= ",bgx
                print "cl=",color


if __name__ == '__main__':
    test1()


