# -*- coding: utf-8 -*-
import xlrd
from datetime import date, datetime
import xlwt
from ABKExcel import ABKTable, ABKSheet

class ABKExcelOperator(object):
    def __init__(self):
        self.sheet_table_data=dict()
        self.read_workbook = None
        self.write_workbook=None
        self.op_sheet_name=None
        self.op_sheet=None
        self.write_style = dict()

    def __initData(self):
        self.sheet_table_data = dict()
        if self.read_workbook is not None:
            del self.read_workbook
            self.read_workbook = None
        if self.op_sheet is not None:
            del self.op_sheet
            self.op_sheet = None
        self.op_sheet_name = ''

    def openFile(self, path):
        self.__initData()
        self.read_workbook = xlrd.open_workbook(path)
        sheet_names = self.read_workbook.sheet_names()
        for sheetname in sheet_names:                       #把sheetname作为dict的key了
            self.sheet_table_data[sheetname] = None
        return True

    def getSheetName(self):
        return self.sheet_table_data.keys()

    def readSheet(self,sheetname=''):
        # 返回值是ABKSheet
        self.op_sheet_name=sheetname

        self.op_sheet = self.read_workbook.sheet_by_name(self.op_sheet_name)

        table_list = self.__getTableList()

        self.addReadData(table_list)
        #return table_list (table_list is type of ABKExcel)

    def __getTableList(self):#要考虑多表的情况...
        merge = self.op_sheet.merged_cells
        merge_cell_dict = dict()
        for rlow, rhigh, clow, chigh in merge:#这里遍历所有的merge
            for irow in xrange(rlow, rhigh):
                for icol in xrange(clow, chigh):
                    #把第一个合并格的东西标记上，用以区分就可以...
                    if irow == rlow and icol == clow :
                        merge_cell_dict[(irow,icol)]=True
                    else:
                        merge_cell_dict[(irow, icol)] = False
        merge_size = len(merge_cell_dict)

        rows = self.op_sheet.nrows
        cols = self.op_sheet.ncols

        tablelist=ABKSheet()
        isNoneRow=list()
        # 记录空行
        for irow in xrange(rows):
            None_count=0
            frist_col=0
            for icol in xrange(cols):
                value=self.__getCellvalue(irow,icol)
                if value is not None:
                    frist_col=icol
                    break
                else:
                    None_count += 1
                if None_count==cols:
                    isNoneRow.append([irow,0])
                else:
                    #如果行有内容，那么记录第一的的列数
                    isNoneRow.append([irow,frist_col])
        # 初始化各个table
        row_span = 0
        table_row = 0
        if isNoneRow[0][1]==0:#第一行为空...
            for irow in range(1,len(isNoneRow)):
                if isNoneRow[irow-1][1] == 0 and isNoneRow[irow][1]>0:# True or False
                    # 说明这是一个新表，然后把创建表并初始化...
                    # 新表开始要记录col_span
                    col_span = isNoneRow[irow][1]
                    table_col = cols - col_span
                    myTable = ABKTable(row_span,col_span,table_row,table_col)
                    #然后把table放到sheet里
                    tablelist.addTable(myTable)
                    del myTable
                    row_span = 0
                    table_row = 0

                else:#说明这不是一个新表
                    if isNoneRow[irow-1][1] == 0:#是空行
                        row_span += 1
                    else:
                        table_row += 1

        else:
            #第一行不为空...
            pass





        '''
        tablelist=list()
        table=list()

        for irow in xrange(rows):
            none_count=0#新的一行，none_count=0
            for icol in xrange(cols):
                value=self.__getCellvalue(irow,icol)
                if value is None:
                    none_count+=1 #若为空，none_count++
                else:#不为空，就把东西加进去
                    if merge_size == 0:
                        table.append([(irow, icol),value])#把单个的key,value以list的形式放入table中
                        # table.setCellData(irow,icol,value)
                    else:#判断是否在merge
                        if (irow, icol) in merge_cell_dict:
                            if merge_cell_dict[(irow,icol)]==True:
                                table.append([(irow, icol),value])
                                # table.setCellData(irow,icol,value)
                        else:
                            table.append([(irow, icol),value])
                            # table.setCellData(irow,icol,value)
                if none_count==cols:#(并且下一行不为空)计数达到cols,说明该行全为none.添加一个新的table
                    tablelist.append(table)
                    table=[]
        #说明是最后一行了：要把最后一个table也压进去
        tablelist.append(table)
        #还要把多余的空table去掉：
        while [] in tablelist:
            tablelist.remove([])
        '''

    def __getCellvalue(self,row,col):#返回指定row ,col 的value
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

    def getRowandcol(self):
        return  self.op_sheet.nrows,self.op_sheet.ncols

    def getTableData(self,sheetname,tableindex):
        tableList = self.sheet_table_data[sheetname]
        if tableindex > len(tableList):
            assert False
        else:
            table=tableList[tableindex]
        return table

    def addReadData(self, table_list):#把读到的数据放到dict里面
        if self.sheet_table_data[self.op_sheet_name] is None:
            self.sheet_table_data[self.op_sheet_name] = list()
        self.sheet_table_data[self.op_sheet_name] = table_list

    def findValueByIndex(self,x,y,sheetname):
        if sheetname not in self.sheet_table_data:
            assert False
        else:#修改内存数据,而不是直接write的地方
            tableList=self.sheet_table_data[sheetname]
            index={(x,y):''}
            #以下的写法可能效率不高...,既遍历所有的数据，与目标index匹配。
            for i in range(0,len(tableList)):
                table = tableList[i]
                for j in range(1,len(table)):
                    cell_list=table[j]
                    cellindex=cell_list[0]
                    if cellindex in index:#匹配成功之后，
                        return cell_list[1]

#~~~~~~~~~~~~~~~~~~~~~~~write~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def addSheetData(self,sheetname,tableList):
        if sheetname.strip() == '':
            assert False
        if sheetname not in self.sheet_table_data:#  有可能就会出现tbaleList是一样的，然后sheetname是不一样的，不过这样不影响。
            self.sheet_table_data[sheetname] =tableList
            self.op_sheet_name = sheetname

    def writeSheet(self, sheet):
        if not isinstance(sheet, ABKSheet):
            return
        # 写 sheet 数据 .......
        if self.op_sheet_name.strip() == '':
            assert False
        if self.write_workbook is None:
            self.write_workbook = xlwt.Workbook() # create a excel book,
        # write data
        if self.op_sheet_name not in self.sheet_table_data:
            assert False
        sheet_table_list = self.sheet_table_data[self.op_sheet_name]

        self.op_sheet = self.write_workbook.add_sheet(self.op_sheet_name, cell_overwrite_ok=True)

        self.__writeByCellMode(sheet_table_list)

    def __writeByCellMode(self, tables):#这个函数的目的是什么？op_sheet.write()
        tableList=tables
        cellcor = dict()
        cellmeger = list()
        cellfont = dict()
        merged = list()
        sheetname=self.op_sheet_name  #既当前要被写的sheet的名字，也就是sheetname

        if len(self.write_style) > 0:
            if sheetname in self.write_style:
                tablestyle = self.write_style[sheetname]
                if 'ccor' in tablestyle:
                    cellcor = tablestyle['ccor']
                if 'merge' in tablestyle:
                    cellmeger = tablestyle['merge']
                if 'label' in tablestyle:
                    cellfont = tablestyle['label']
        if len(cellmeger) > 0:
            for rlow, rhigh, clow, chigh in cellmeger:
                if rlow == rhigh and clow != chigh:#列合并
                    for c in range(clow+1,chigh+1):
                        merged.append((rlow,c))
                    self.op_sheet.write_merge(rlow, rhigh, clow, chigh)#,self.findValueByIndex(rlow,clow,sheetname),self.__cellstyle('white','Meiryo'))
                elif clow == chigh and rlow != rhigh:#列合并
                    for r in range(rlow+1,rhigh+1):
                        merged.append((r,clow))
                    self.op_sheet.write_merge(rlow, rhigh, clow, chigh)#,self.findValueByIndex(rlow,clow,sheetname),self.__cellstyle('white','Meiryo'))
                else:
                    self.op_sheet.write_merge(rlow, rhigh, clow, chigh)#,self.findValueByIndex(rlow,clow,sheetname),self.__cellstyle('white','Meiryo'))
                    for r in range(rlow,rhigh+1):
                        for c in range(clow,chigh+1):
                            if r==rlow and c==clow:
                                continue
                            else:
                                merged.append((r,c))
        for i in range(0,len(tableList)):
                table = tableList[i]
                #应该是除了0之后的
                for j in range(0,len(table)):
                    cell_list = table[j]
                    cellindex = cell_list[0]
                    cellvalue = cell_list[1]
                    cor = None
                    fon = None
                    if cellvalue is None:
                        continue
                    if cellindex in cellcor:
                        cor = cellcor[cellindex]
                    if cellindex in cellfont:
                        fon = cellfont[cellindex]
                    if cor is not None and fon is not None:
                        self.op_sheet.write(cellindex[0], cellindex[1], cellvalue, self.__cellstyle(cor, fon))
                    elif cor is not None:
                        self.op_sheet.write(cellindex[0], cellindex[1], cellvalue, self.__cellstyle(cor))
                    elif fon is not None:
                        self.op_sheet.write(cellindex[0], cellindex[1], cellvalue, self.__cellstyle('white', fon))
                    else:
                        self.op_sheet.write(cellindex[0], cellindex[1], cellvalue, self.__cellstyle('white','Times New Roman'))
                for x,y in merged:
                    self.op_sheet.write(x, y, '', self.__cellstyle('white', 'Times New Roman'))

    def __cellstyle(self,fore_cor_name='', fontname=''):
        """
        note: set cell style
        :param fore_cor_name: cell color
        :param fontname: font name
        :param bold: is boldden
        :return:
        """
        style = xlwt.XFStyle() # style
        font = xlwt.Font() # font
        font.name = fontname
        font.bold = False
        font.color_index = 2  # xlwt.Style.colour_map['rose']  # 0:black, 1: white, 2: red, 3:light green, 4:blue 好像是无效的...?????

        borders = xlwt.Borders()
        borders.left = xlwt.Borders.THIN    # may be NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED
        borders.right = xlwt.Borders.THIN
        borders.top = xlwt.Borders.THIN
        borders.bottom = xlwt.Borders.THIN
        style.font = font
        style.borders = borders

        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = xlwt.Style.colour_map[fore_cor_name]
        #pattern.pattern_back_colour = xlwt.Style.colour_map[fore_cor_name] #有没有这句话的效果是一样的.
        style.pattern = pattern

        return style

    def writeExcel(self, excelname):
        """
        note: form excel,to be implement on subclass
        :param excelname: excel name
        :return: True or False
        """
        if excelname.strip() != '':
            if self.write_workbook is not None:
                self.write_workbook.save(excelname)
                return True
        return False

    def setStyle(self, sheet_name):
        """
        note: writestyle set up
        :param stylelist: writestyle
        :return:
        """
        styleList = dict()
        styleList['ccor'] = dict()
        styleList['label'] = dict()
        styleList['merge'] = list()
        self.write_style[sheet_name] = styleList

    def setBG(self,x,y,cor='white',name=''):
        self.write_style[name]['ccor'][(x,y)] = cor

    def setMerge(self,r1,r2,c1,c2,name=''):
        #后面所以得self.style。都是要从write_style那里出发的...
        self.write_style[name]['merge'].append((r1,r2,c1,c2))

    def setFont(self,x,y,font,name=''):
        self.write_style[name]['label'][(x,y)]=font

    def updateCellValue(self,x,y,new_value,sheetname):#功能：修改指定每一个单元的内容.
        if sheetname not in self.sheet_table_data:
            assert False
        else:#修改内存数据,而不是直接write的地方
            tableList=self.sheet_table_data[sheetname]
            index={(x,y):new_value}
            #以下的写法可能效率不高...,既遍历所有的数据，与目标index匹配。
            for i in range(0,len(tableList)):
                table = tableList[i]
                for j in range(1,len(table)):
                    cell_list=table[j]
                    cellindex=cell_list[0]
                    if cellindex in index:#匹配成功之后，把原来的值改掉
                        cell_list[1]=new_value

    def delSheet(self, sheetname):
        if sheetname.strip():
            return
        if sheetname in self.sheet_table_data:
            del self.sheet_table_data[sheetname]
            if cmp(sheetname, self.op_sheet_name) == 0:
                self.op_sheet_name = ''
