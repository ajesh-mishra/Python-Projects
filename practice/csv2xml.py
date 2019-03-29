import csv
import sys
import xml.etree.cElementTree as ET
import lxml.etree as etree

def get_file():
  '''Finds a file if passed as an argument or
  uses the defult CSV file'''
  try:
    csv_file = sys.argv[1]
  except IndexError:
    csv_file = "import_me.csv"
    print("No file was given, working with default file: import_me.csv")

  return csv_file

def add_xml(partner_info):
  '''Adds each row from CSV to the XML file'''
  Partner = ET.SubElement(Partners, "Partner")
  for key, value in partner_info.items():
    ET.SubElement(Partner, key).text = value

def render_xml(Processdata, xml_file):
  tree = ET.ElementTree(Processdata)
  tree.write(xml_file)

  x = etree.parse(xml_file)
  print("\n")
  print(etree.tostring(x, pretty_print=True, encoding="unicode"))

def read_csv(csv_file="import_me.csv"):
  '''Reads the CSV file and calls add_xml function'''
  rows = []
  with open(csv_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile, dialect='excel')
    fields = csvreader.__next__()
        
    for row in csvreader: 
      rows.append(row)

    print(f'Total no. of rows: {csvreader.line_num}', flush=True)
    print('Field names are: ' + ', '.join(field for field in fields))

    for row in rows:
      partner_info = {}
      for key, value in zip(fields, row):
        partner_info[key] = value

      add_xml(partner_info)

if __name__ == '__main__':
  xml_file = "import_me.xml"
  Processdata = ET.Element("Processdata")
  Partners = ET.SubElement(Processdata, "Partners")

  read_csv(get_file())
  render_xml(Processdata, xml_file)
