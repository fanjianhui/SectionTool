# -*- coding: utf-8 -*-

class ExcelOperator(object):
    def __init__(self):
        self.sheet_table_data_r = dict()
        self.sheet_table_data_w = dict()
        self.read_workbook = None
        self.op_sheet_name=None
        self.op_sheet=None

        self.write_workbook=None

        self.write_style = dict()
        #self.cor=dict()
        #self.font=dict()
        #self.merge=list()
        #self.styleList = dict()
