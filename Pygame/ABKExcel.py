# -*- coding: utf-8 -*-
import xlrd
from datetime import date, datetime
import xlwt
import types
import os
import wx

#-----------------------------------------------------对话框------------------------------------------------------#
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
#-----------------------------------------------excel文件操作对象-------------------------------------------------#

# 可用颜色名称表
abkExcelColor = {
    'black':8,
    'white':9,
    'red':10,
    'bright_green':11,
    'blue':12,
    'yellow':13,
    'pink':14,
    'cyan_ega':15,
    'dark_red':16,
    'green':17,
    'dark_blue':18,
    'dark_yellow':19,
    'purple_ega':20,
    'teal':21,
    'gray25':22,
    'gray_ega':23,
    'periwinkle':24,
    'ivory':25,
    'violet':27,
    'dark_purple':28,
    'coral':29,
    'ocean_blue':30,
    'ice_blue':31,
    'teal_ega':32,
    'silver_ega':33,
    'olive_ega':34,
    'magenta_ega':35,
    'dark_red_ega':36,
    '_violet':37,
    'turquoise':38,
    '_olive_ega':39,
    'sky_blue':40,
    'light_turquoise':41,
    'light_green':42,
    'light_yellow':43,
    'pale_blue':44,
    'rose':45,
    'lavender':46,
    'tan':47,
    'light_blue':48,
    'aqua':49,
    'lime':50,
    'gold':51,
    'light_orange':52,
    'orange':53,
    'blue_gray':54,
    'gray40':55,
    'dark_teal':56,
    'sea_green':57,
    'dark_green':58,
    'olive_green':59,
    'brown':60,
    'plum':61,
    'indigo':62,
    'gray80':63
    }
abkExcelFont = {
    'Arial':1,
    'Arial Unicode MS':2,
    'Batang':3,
    'Bell MT':4,
    'Calibri':5,
    'David':6,
    'Edwardian Script ITC':7,
    'MS Reference Specialty':8,
    'Microsoft Uighur':9,
    'Segoe Marker':10,
    'Times New Roman':11,
    'Wingdings 3':12
    }
# 可用字体名称表

class ABKExcelOperator(object):
    def __init__(self):
        self.sheet_table_data = dict()
        self.read_workbook = None
        self.write_workbook = None
        self.op_sheet_name = None
        self.op_sheet = None
        self.write_style = dict()

    # 初始化数据
    def __initData(self):
        '''
        初始化内存数据
        :return:
        '''
        self.sheet_table_data = dict()
        if self.read_workbook is not None:
            del self.read_workbook
            self.read_workbook = None
        if self.op_sheet is not None:
            del self.op_sheet
            self.op_sheet = None
        self.op_sheet_name = ''

    def openFile(self, path):

        '''
        打开一个xls,文件
        :param path:
        :return:
        '''
        self.__initData()
        if os.path.exists(path):
            self.read_workbook = xlrd.open_workbook(path,formatting_info=True)
        else:# new a empty file,and do the same work.
            file = xlwt.Workbook()
            self.write_workbook = file
            # we set a default sheet ,named 'Sheet1'
            file.add_sheet('Sheet1')
            file.save(path)
            return True
        sheet_names = self.read_workbook.sheet_names()
        for sheetname in sheet_names:                       #把sheetname作为dict的key了
            self.sheet_table_data[sheetname] = None
        return True

    def getSheetName(self):
        return self.sheet_table_data.keys()

    def readSheet(self,sheetname=''):
        '''
        :param sheetname: 可以是一个list,也可以是单个sheetname
        :return:返回值是ABKSheet
        '''
        if sheetname in self.sheet_table_data:
            self.op_sheet_name=sheetname
            self.op_sheet = self.read_workbook.sheet_by_name(self.op_sheet_name)
            table_list = self.__getSheet()
            return table_list
        else:
            return None

    def __getIsNoneRow(self):
        '''
        遍历每一行，以[sheet_row,table_row,first_col]的内存形式标记是否为空行..
        first_col为0则表示改行为空行..
        :return:
        note: 写算法文档
        '''
        rows = self.op_sheet.nrows
        cols = self.op_sheet.ncols
        isNoneRow = list()
        table_row = 0
        for irow in xrange(rows):
            None_count=0
            for icol in xrange(cols):
                value = self.__getCellvalue(irow,icol)
                if value is not None:
                    first_col = icol
                    #如果行有内容，那么记录第一的的列数
                    table_row += 1
                    isNoneRow.append([irow,table_row,first_col])
                    break
                else:
                    None_count += 1
                    if None_count == cols:
                        isNoneRow.append([irow,0,0])
                        table_row = 0
        return isNoneRow

    # 初始化一个Table,index为0 表示数据从第一行开始 ，返回的是一个赋了属性的，不带数据内容的空table
    def __initialSheet(self,index=1,isNoneRow=list()):
        '''
        :param index: index=0 :表名数据从第0行开始...
        :param isNoneRow:  标记是否为空行的list
        procedure:
            判断是否为为新表，如果是，则new ABKTable，并设置table的基本属性，返回的是一个没存放数据的table
        :return:
        note：写算法文档
        '''
        sheet = ABKSheet(self.op_sheet_name)

        rows = self.op_sheet.nrows
        cols = self.op_sheet.ncols
        old_col_pos = 0
        row_span = 0
        table_row = 0
        if index==0:
            row_num = len(isNoneRow)-1
        else:
            row_num = len(isNoneRow)
        for irow in range(1,row_num):
                if isNoneRow[irow-1][1] == 0 and isNoneRow[irow][1]>0:# True or False
                    # 说明这是一个新表，然后把创建表并初始化...
                    # 新表开始要记录col_span
                    if index == 0:
                        # 数据从第一行开始
                        isNoneRow.remove([-1,0,0])
                        index = 1
                        irow -= 1
                        row_span -= 1

                    if old_col_pos == 0:
                        # 第一个表
                        col_span = isNoneRow[irow][2]
                    else:
                        col_span = isNoneRow[irow][2] - old_col_pos
                    # cols ==这个sheet中最大的列数
                    table_col = cols

                    # 数Table 的row:
                    startrow = irow
                    while isNoneRow[startrow][1]:
                        startrow += 1
                        if startrow == rows:  # it is the end of the index
                            break
                    table_row = startrow-irow
                    # 表格下标从0开始计数
                    myTable = ABKTable(row_span+1,col_span,table_row-1,table_col,irow)
                    myTable.absout_col = isNoneRow[irow][2]
                    #然后把table放到sheet里
                    sheet.addTable(myTable)
                    old_col_pos = myTable.absout_col
                    row_span = 0
                    table_row = 0
                else:#说明这不是一个新表
                    if isNoneRow[irow-1][1] == 0:#是空行
                        row_span += 1
                    else:
                        table_row += 1
        return sheet

    # 将数据填充到ABKTable的数据对象中，获得一个tableList(ABKSheet对象)
    def __getSheet(self):#要考虑多表的情况...
        """
        step1:记录空行IsNoneRow
        step2:获取空数据的tables
        step3:给为一个table赋值，并设置他们的样式...
        step4:返回tables
        :return:
        note：写算法文档
        """
        merge = self.op_sheet.merged_cells
        # 记录空行
        isNoneRow = self.__getIsNoneRow()
        # 初始化各个table
        if isNoneRow[0][1]==0:#第一行为空...
            sheet = self.__initialSheet(1,isNoneRow)
        else:
            #第一行不为空,添加一个空行
            isNoneRow.insert(0,[-1,0,0])
            sheet = self.__initialSheet(0,isNoneRow)

        tables = sheet.getTables()
        for table in tables:
            index = table.table_index
            rows = table.table_row
            cols = table.table_col
            abs_col = table.absout_col
            col_max = 0
            table.initStyleOn()
            # 设置title
            table.setTitle(self.__getCellvalue(index,abs_col))
            table.write_style[table.getTitle()]['merge'] = list()
            for irow in xrange(1, rows+1):
                for icol in xrange(0, cols):
                    value = self.__getCellvalue(irow+index, icol)
                    #font = self.__getFontStyle(irow+index,icol)
                    bgcolor = self.__getBGColor(irow+index,icol)
                    font = self.__getFontStyle(irow+index,icol)  # 返回元组..
                    if value is None:
                        continue
                    else:
                        if icol > col_max:
                            col_max = icol
                        # 差了index的距离...
                        table.setCellData(irow, icol-abs_col+1, value)
                        # 判断背景色是否白色(空白)
                        if not bgcolor == 9:
                            table.setColor(irow, icol-abs_col+1, bgcolor)
                        if font is not None:
                            table.setFont(irow, icol-abs_col+1, font)
            table.table_col = col_max - table.absout_col+1
            table.write_style[table.getTitle()]['merge'].append([0,0,0,table.table_col-1])

            # 记录样式.

            for rlow, rhigh, clow, chigh in merge:
                if rlow>index and rhigh-1<=index+rows:
                    # 判断合并格是否在该表中...
                    table.setMerge(rlow-index,rhigh-index-1,clow-abs_col+1,chigh-abs_col);
            table.table_col = col_max - table.absout_col

        return sheet

    def __getCellvalue(self,row,col):
        '''
        返回指定row ,col 的value
        获得单个cell的值
        :param row: 行值
        :param col:列值
        :return:
        '''

        ctype = self.op_sheet.cell(row, col).ctype
        if ctype == 0:
            cell_var = None
        elif ctype == 1:
            cell_var = self.op_sheet.cell(row, col).value
        elif ctype == 2:
            cell_var = self.op_sheet.cell_value(row, col)
        elif ctype == 3:
            date_value = xlrd.xldate_as_tuple(self.op_sheet.cell_value(row, col), self.read_workbook.datemode)
            cell_var = date(*date_value[:3]).strftime('%Y/%m/%d')
        elif ctype == 4:
            cell_var = self.op_sheet.cell_value(row, col)
        elif ctype == 5:
            raise TypeError, "%s is not a valid value" % self.op_sheet.cell_value(row, col)
        else:
            cell_var = ''
        return cell_var

    def __getBGColor(self,row,col):
        '''
        获取cell的背景色
        :param row:
        :param col:
        :return:
        '''
        sheet = self.op_sheet
        book = self.read_workbook
        xfx = sheet.cell_xf_index(row, col)
        xf = book.xf_list[xfx]
        bgx = xf.background.pattern_colour_index

        return bgx

    def __getFontStyle(self,row,col):
        '''
        获取字体的样式
        :param row:
        :param col:
        :return:
        '''
        sheet = self.op_sheet
        book = self.read_workbook
        xfx = sheet.cell_xf_index(row, col)
        xf = book.xf_list[xfx]
        font = book.font_list[xf.font_index]
        if font.bold == 0 and font.colour_index == 32767 and font.height == 200:
            return None
        return [font.name, font.bold, font.colour_index, font.height]

    def writeSheet(self, sheet):
        '''
        写指定名的Sheet
        :param sheet:ABKSheet
        :return:
        '''

        if not isinstance(sheet, ABKSheet):
            return
        # 写 sheet 数据 .......
        self.op_sheet_name = sheet.getName()
        self.sheet_table_data[self.op_sheet_name] = sheet
        if self.write_workbook is None:
            self.write_workbook = xlwt.Workbook()

        self.op_sheet = self.write_workbook.add_sheet(self.op_sheet_name, cell_overwrite_ok=True)

        self.__writeByCellMode(sheet)

    # 给单个cell内容填充
    def __writeByCellMode(self, sheet):
        '''
        遍历威哥cell并写入数据
        :param sheet:
        :return:
        note：写算法文档
        '''
        tableList = sheet.getTables()
        style1 = self.style('bottom')
        for table in tableList:
            cellcor = dict()
            cellmeger = list()
            cellfont = dict()
            merged = list()

            index = table.table_index
            abs_col = table.absout_col

            style = table.getStyle()
            if table.hasTitle:
                tablestyle = style[table.getTitle()]
            else:
                tablestyle = style['default_style']
            if len(tablestyle) > 0:
                if 'ccor' in tablestyle:
                    cellcor = tablestyle['ccor']
                if 'merge' in tablestyle:
                    cellmeger = tablestyle['merge']
                if 'label' in tablestyle:
                    cellfont = tablestyle['label']

            if len(cellmeger) > 0:
                for rlow, rhigh, clow, chigh in cellmeger:
                    if rlow == rhigh and clow != chigh:#列合并
                        for c in range(clow,chigh+1):
                            merged.append((rlow,c))
                        # merged.append()
                        self.op_sheet.write_merge(rlow+index, rhigh+index, clow+abs_col, chigh+abs_col,'',style1)
                    elif clow == chigh and rlow != rhigh:#列合并
                        for r in range(rlow,rhigh+1):
                            merged.append((r,clow))
                        self.op_sheet.write_merge(rlow+index, rhigh+index, clow+abs_col, chigh+abs_col,'',style1)#,self.findValueByIndex(rlow,clow,sheetname),self.__cellstyle('white','Meiryo'))
                    else:
                        # 否则就是任意合并，
                        self.op_sheet.write_merge(rlow+index, rhigh+index, clow+abs_col, chigh+abs_col,'',style1)#,self.findValueByIndex(rlow,clow,sheetname),self.__cellstyle('white','Meiryo'))
                        for r in range(rlow,rhigh+1):
                            for c in range(clow, chigh+1):
                               merged.append((r, c))

            cell_list = table.table_data
            # whether the table has the title...
            if table.hasTitle():
                self.op_sheet.write(index, abs_col, table.getTitle(),self.__cellstyle('white'))
            for j in range(0, len(cell_list)):
                cell = cell_list[j]
                cellindex = cell[0]
                cellvalue = cell[1]
                cor = None
                fon = None
                if cellvalue is None:
                    continue
                if cellindex in cellcor:
                    cor = cellcor[cellindex]
                if cellindex in cellfont:
                    fon = cellfont[cellindex]

                cell_x = index+cellindex[0]
                cell_y = abs_col+cellindex[1]

                # 如果cellindex  在merged里面：那么给一个style1
                flag = True
                if cellindex in merged:
                    if cellindex[0]==0:
                        flag = True
                    else:
                        flag = False
                    #self.op_sheet.write(cell_x, cell_y, cellvalue, style1)

                if flag:
                    if cor is not None and fon is not None:
                        self.op_sheet.write(cell_x, cell_y, cellvalue, self.__cellstyle(cor, fon))
                    elif cor is not None:
                        self.op_sheet.write(cell_x, cell_y, cellvalue, self.__cellstyle(cor))
                    elif fon is not None:
                        self.op_sheet.write(cell_x, cell_y, cellvalue, self.__cellstyle('white', fon))
                    else:
                        self.op_sheet.write(cell_x, cell_y, cellvalue, self.__cellstyle('white'))

            for x, y in merged:
                #x,y 传进来判断下他的上 下 右 是否有合并格，如果有合并个就
                if x == 0 and y != 0:
                    self.op_sheet.write(x+index, y+abs_col, '',self.__cellstyle('white'))


    # 设置cell的样式
    def __cellstyle(self,fore_cor_name='', _font=None, BoderStyle = None):
        """
        note: set cell style
        :param fore_cor_name: cell color
        :param fontname: font name
        :param bold: is boldden
        :return:
        """
        colourDict={
            8:'black',9:'white',10:'red',11:'bright_green',12:'blue',13:'yellow',14:'pink',15:'cyan_ega',16:'dark_red',17:'green',18:'dark_blue',19:'dark_yellow',20:'purple_ega',
	        21:'teal',22:'gray25',23:'gray_ega',24:'periwinkle',26:'ivory',27:'violet',28:'dark_purple',29:'coral',
	        30:'ocean_blue',31:'ice_blue',32:'teal_ega',33:'silver_ega',34:'olive_ega',35:'magenta_ega',36:'dark_red_ega',37:'violet',38:'turquoise',39:'olive_ega',40:'sky_blue',
	        41:'light_turquoise',42:'light_green',43:'light_yellow',44:'pale_blue',45:'rose',46:'lavender',47:'tan',48:'light_blue',49:'aqua',
	        50:'lime',51:'gold',52:'light_orange',53:'orange',54:'blue_gray',55:'gray40',56:'dark_teal',57:'sea_green',
	        58:'dark_green',59:'olive_green',60:'brown',61:'plum',62:'indigo',63:'gray80'
        }

        style = xlwt.XFStyle() # style
        font = xlwt.Font()
        if _font is None:
            # font
            font.height = 200
            font.bold = False
            font.colour_index = 32767  # xlwt.Style.colour_map['rose']  # 0:black, 1: white, 2: red, 3:light green, 4:blue 好像是无效的...?????
            font.name = 'Times New Roman'
        else:
            font.name = _font[0]
            font.bold = _font[1]
            font.colour_index = _font[2]
            font.height = _font[3]

        borders = xlwt.Borders()
        if BoderStyle == 'bottom':
            borders.bottom = xlwt.Borders.NO_LINE
        else:
            borders.bottom = xlwt.Borders.THIN

        borders.left = xlwt.Borders.THIN    # may be NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN

        style.font = font
        style.borders = borders

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        if type(fore_cor_name) == type(10):
            if fore_cor_name in colourDict:
                fore_cor_name=colourDict[fore_cor_name]
            else:
                fore_cor_name = 'white'
        pattern.pattern_fore_colour = xlwt.Style.colour_map[fore_cor_name]
        #pattern.pattern_back_colour = xlwt.Style.colour_map[fore_cor_name] #有没有这句话的效果是一样的.
        style.pattern = pattern

        return style

    def style(self,boder):
        style = xlwt.XFStyle() # style
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.height = 200
        font.bold = False
        font.colour_index = 32767

        borders = xlwt.Borders()

        borders.bottom = xlwt.Borders.NO_LINE
        borders.left = xlwt.Borders.NO_LINE    # may be NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED
        borders.right = xlwt.Borders.NO_LINE
        borders.top = xlwt.Borders.NO_LINE

        style.font = font
        style.borders = borders

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        fore_cor_name = 'white'
        pattern.pattern_fore_colour = xlwt.Style.colour_map[fore_cor_name]
        style.pattern = pattern

        return style

    def writeExcel(self, excelname):
        """
        note: form excel,to be implement on subclass
        :param excelname: excel name
        :return: True or False
        """
        # before we save the file ,we change the extension from xlxs to xls...
        start = excelname.find('.')
        extension = excelname[start:len(excelname)]
        if extension=='.xlsx':
            extension='.xls'
            excelname = excelname[0:start]+extension
        print excelname
        if excelname.strip() != '':
            if self.write_workbook is not None:
                self.write_workbook.save(excelname)
                return True
        return False
#-----------------------------------------------excel文件操作对象-------------------------------------------------#


#-----------------------------------------------表格数据对象------------------------------------------------------#
class ABKTable(object):
    def __init__(self, row_span=0, col_span=0, rows=0, cols=0, index=0,title=""):
        """
        note：写算法文档
        """
        self.title = title
        self.row_span = row_span
        self.col_span = col_span

        self.table_row = rows  #初始化的时候先确定表格的大小...

        self.table_col = cols

        if index == 0:
            self.table_index = row_span
            self.absout_col = col_span
        else:
            self.table_index = index
            self.absout_col = 0

        # 包括ccor,font, merge
        self.write_style = dict()
        # 用来存放数据
        self.table_data = list()

    # 表格模式
    def initStyleOn(self):
        # initial the style mode...
        styleList = dict()
        styleList['ccor'] = dict()
        styleList['label'] = dict()
        styleList['merge'] = list()
        styleList['merge'].append([0,0,0,self.table_col-1])
        if self.title == '':
            self.write_style['default_style'] = styleList
        else:
            self.write_style[self.title] = styleList

    # 设置表名
    def setTitle(self, _name):
        self.title = _name
        self.write_style[_name] = self.write_style['default_style']

    def getTitle(self):
        return self.title

    def hasTitle(self):
        if self.title != "":
            return True
        else:
            return False

    def setCellData(self, irow, icol, value):#通过这个data创建这个表格...
        # 把内存用户数据写入内存表格对象
        # 检查 value合理性
        if not self._check_cell_data(value):
            return
        # irow, icol 范围检查
        if not self._check_cell_index(irow, icol):
            return
        (irow,icol) = self._cell_position_transform(irow,icol)
        # 赋值
        self.table_data.append([(irow,icol),value])

    def getCellData(self, irow, icol):#返回tabkeData
        # note：写算法文档
        # irow，icol 范围检查
        # 下标从1开始计数
        cell_position = self._cell_position_transform(irow, icol)
        # 用从0开始的来确定是否在table里面...
        if not self._check_cell_index(irow, cell_position[1]):
            return None
        # 获取值并返回[(x,y),value]
        for cell in self.table_data:
            if (cell_position[0],cell_position[1]) in cell:
                return cell
        return None

    def setFont(self, irow, icol, _font_name):
        '''
        设置字体样式
        :param irow:
        :param icol:
        :param _font_name:
        :return:
        '''
        # 可以设置
        if not self._check_cell_index(irow, icol):
            return
        (irow, icol) = self._cell_position_transform(irow,icol)
        if type(_font_name[2]) == type('str'):
            if _font_name[2] in abkExcelColor:
                name = _font_name[2]
                _font_name[2] = abkExcelColor[name]
            else:
                _font_name[2] = 9

        if self.hasTitle():
            self.write_style[self.title]['label'][(irow,icol)] = _font_name
            if 'default_style' in self.write_style:
                del self.write_style['default_style']
        else:
            self.write_style['default_style']['label'][(irow,icol)] = _font_name

    def setMerge(self, rlow,rhigh, clow, chigh):
        '''
        设置合并格
        :param rlow: 行最小
        :param rhigh: 行最大
        :param clow:列最小
        :param chigh: 列最大
        :return:
        '''

        # 可以设置
        if not self._check_cell_index(rlow, clow) or not self._check_cell_index(rhigh, chigh):
            return
        (rlow,clow) = self._cell_position_transform(rlow,clow)
        (rhigh,chigh) = self._cell_position_transform(rhigh,chigh)

        if self.hasTitle():
            self.write_style[self.title]['merge'].append((rlow,rhigh,clow,chigh))
            if 'default_style' in self.write_style:
                del self.write_style['default_style']
        else:
            self.write_style['default_style']['merge'].append((rlow,rhigh,clow,chigh))

        return True

    def setMergeBy(self,merge_list):
        # 将合并按两部分来合并
        for i in merge_list:
            self.setMerge(i)


    def setColor(self, irow, icol, _color_name):
        '''
        设置指定cell的颜色
        :param irow:
        :param icol:
        :param _color_name:
        :return:
        '''

        # 可以设置
        if not self._check_cell_index(irow, icol):
            return
        (irow, icol) = self._cell_position_transform(irow,icol)
        if self.hasTitle():
            self.write_style[self.title]['ccor'][(irow,icol)] = _color_name
            if 'default_style' in self.write_style:
                del self.write_style['default_style']
        else:
            self.write_style['default_style']['ccor'][(irow,icol)] = _color_name

        return True

    # 返回这个表格的样式...
    def getStyle(self):
        return self.write_style

    # 判断行列是否在cell中
    def _check_cell_index(self, irow, icol):
        # 检查单元格下标是否合理
        if irow > self.table_row or icol > self.table_col:
            return False
        return True

    # 判断value是否合理
    def _check_cell_data(self, value):
        # 检查单元格数据类型是否合理 True False
        if isinstance(value, (str, int, float, unicode)):
            return True
        else:
            return False

    # 单元格坐标转换
    def _cell_position_transform(self, irow, icol):
        if self.hasTitle():
            # 内存列值= 用户输入列值-1
            return (irow, icol-1)
        else:
            return (irow-1, icol-1)
#-----------------------------------------------表格数据对象------------------------------------------------------#

#-----------------------------------------------sheet数据对象-----------------------------------------------------#
class ABKSheet(object):
    def __init__(self, _name=''):
        self.name = _name
        self.TableList_data = list()
        self.mode = False

    def getName(self):
        return self.name

    # 添加表格
    def addTable(self, _abkt):
        # 判断_abkt类型 isinstance(_abkt, abkt)
        # 添加到；列表
        if isinstance(_abkt,ABKTable):
            self.TableList_data.append(_abkt)
            return True
        else:
            assert False

    # 获取表格
    def getTableByName(self, _name):
        # 判断是否存在
        # 返回
        for table in self.TableList_data:
            name = table.getTitle()
            if name == '':
                return None
            else:
                if _name == name:
                    return table
        return None

    def getTableByindex(self, _index):
        # 判断是否存在
        # 返回
        if _index > len(self.TableList_data) or _index < 0:
            return None
        else:
            return self.TableList_data[_index]

    # 删除表格
    def delTable(self, _name):
        for table in self.TableList_data:
            name = table.getTitle()
            if name == '':
                return False
            else:
                if _name == name:
                    del table
                    return True

    # 插入表格
    def insertTable(self, _abkt, index=None):
        # 判断_abkt类型 isinstance(_abkt, abkt)
        # 重写index以后的所以table,把每个row加上_abkt的长度...
        # 然后在写上该_abkt
        # note：写算法文档
        if not isinstance(_abkt,ABKTable):
            return
        else:
            tableList = self.getTables()
            if index == None or index >= len(tableList):
                lenth=len(tableList)
                table = tableList[lenth-1]
                _abkt.table_index = table.table_index + table.table_row+1 + _abkt.row_span
                _abkt.absout_col = table.absout_col + _abkt.col_span
                tableList.append(_abkt)
                # 插入的时候table的属性没有改掉...
            elif index <= 0:
                # update value from the star.
                row_move = _abkt.row_span+_abkt.table_row+1
                for table in tableList:
                    table.table_index += row_move
                tableList.insert(0, _abkt)
            else:
                row_move = _abkt.row_span+_abkt.table_row+1
                lasttable = tableList[index-1]
                _abkt.table_index = lasttable.table_index + lasttable.table_row+1 + _abkt.row_span
                _abkt.absout_col = lasttable.absout_col + _abkt.col_span

                for i in xrange(index, len(tableList)):
                    table = tableList[i]
                    table.table_index += row_move
                tableList.insert(index, _abkt)
        return True
    # 获取所有表格

    def getTables(self):
        return self.TableList_data
#-----------------------------------------------sheet数据对象-----------------------------------------------------#

#-----------------------------------------------excel数据对象-----------------------------------------------------#
class ABKExcel(ABKExcelOperator):
    def __init__(self):
        super(ABKExcel, self).__init__()
        self.name = ""
        self.sheets = dict()
        self.mode = False

    # 文件操作 记录文件名，文件下的sheetname..
    def open(self, _name):
        self.name = _name #name is equal to the path of the file.

        self.openFile(_name)

        sheetnames=self.getSheetName()
        for name in sheetnames:
            self.sheets[name] = None
        return True

    def close(self):
        self.name = ""
        self.sheets.clear()

    def save(self, _name=''):
        if self._isMode():
            if _name == '' and self.name != '': #save what we open first.
                # 提示用户原有文件会被覆盖
                app = App()
                if app.falg:
                    if not self._write(self.name):
                        return False
                else:
                    print app.falg
                    return False
            elif _name == self.name:
                # 提示用户原有文件会被覆盖
                app = App()
                if app.falg:
                    if not self._write(self.name):
                        return False
                else:
                    print app.falg
                    return False
            else:
                self.name = _name
                if not self._write(self.name):
                    return False
        else:
            return False
        return True

    def WriteOn(self):
        self.mode = True

    def ReadOn(self):
        self.mode = False

    def _isMode(self):
        return self.mode

    def readsheets(self, sheet_names):
        if self._isMode():
            return
        # 读取文件中的sheet数据

        if type(sheet_names) is types.ListType:
            for _name in sheet_names:
                # 读取

                sheet = self.readSheet(_name)
        else:
            sheet = self.readSheet(sheet_names)

        if sheet is not None:
            self.WriteOn()
            self.addsheet(sheet)

    # 将内存数据写入Excel中
    def _write(self, _name):
        # 判断文件_name 是否被打开,如果被打开。注意要拷贝临时文件，等写入成功后删除临时文件
        # 如果写入失败，则把临时文件恢复，并删除临时文件

        # 把内存sheet数据写入excel文件内存操作对象中

        # 保存文件
        for sheet_name, sheet in self.sheets.iteritems():
            self.writeSheet(sheet)
        self.writeExcel(_name)
        return True

    def getSheets(self):
        return self.sheets

    def getSheetByName(self,_name):
        if _name not in self.sheets.keys():
            return
        else:
            return self.sheets[_name]

    def addsheet(self, sheet):
        if self._isMode():
            if not isinstance(sheet, ABKSheet):
                return
            if sheet.getName() in self.sheets.keys():
                self.sheets.pop(sheet.getName())
            self.sheets[sheet.getName()] = sheet
        else:
            return False
        return True
        # Excepted the self.sheets,we should set the data to the memory.
        # it is a type of write.

    def delSheet(self, sheetname):
        if not self._isMode():
            return False
        if sheetname in self.sheets:
            del self.sheets[sheetname]
            return True
        return False

    def get_sheet_names(self):
        if len(self.sheets) > 0:
            return self.sheets.keys()
#-----------------------------------------------excel数据对象-----------------------------------------------------#
