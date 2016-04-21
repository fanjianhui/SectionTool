from openpyxl import Workbook
from openpyxl.drawing.image import Image


wb = Workbook()

ws = wb.active

ws['A4'] = 7

img = Image('section.png')

ws.add_image(img, 'F1')

wb.save('newbalances.xlsx')
