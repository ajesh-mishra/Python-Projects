import sys
import xlrd
import xml.etree.cElementTree as ET
import lxml.etree as etree

def add_xml(partner_info):
  Partner = ET.SubElement(Partners, "Partner")
  for key, value in partner_info.items():
    ET.SubElement(Partner, key).text = value

def render_xml(Processdata, xml_file):
  tree = ET.ElementTree(Processdata)
  tree.write(xml_file)

  x = etree.parse(xml_file)
  print("\n")
  print(etree.tostring(x, pretty_print=True, encoding="unicode"))

def read_excel(csv_file="import_me.csv"):
  with xlrd.open_workbook(excel_file) as wb:
    sheet = wb.sheet_by_index(0) 

  # total_column = sheet.ncols
  total_row = sheet.nrows
  fields = sheet.row_values(0)
  # print(sheet.cell_value(0, 0))

  for i in range(1, total_row):
    partner_info = {}
    for key, value in zip(fields, sheet.row_values(i)):
      partner_info[key] = value
    
    add_xml(partner_info)

if __name__ == '__main__':
  excel_file = 'import_me.xlsx' if (len(sys.argv) == 1) else sys.argv[1]
  print(f'\nWorking with file: {excel_file}')
  
  xml_file = "import_me.xml"
  Processdata = ET.Element("Processdata")
  Partners = ET.SubElement(Processdata, "Partners")
  
  read_excel(excel_file)
  render_xml(Processdata, xml_file)
