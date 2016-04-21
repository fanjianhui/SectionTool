from openpyxl import load_workbook

wb2 = load_workbook('balances.xlsx')

sheetname = wb2.get_sheet_names()

ws = wb2.get_sheet_by_name(sheetname[0])


wb2.save('new_balances.xlsx')