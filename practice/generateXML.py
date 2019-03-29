import xml.etree.cElementTree as ET
import lxml.etree as etree

xml_file = "import_me.xml"
Processdata = ET.Element("Processdata")
Partners = ET.SubElement(Processdata, "Partners")

for i in range(1, 4):
	Partner = "Partner_" + str(i)
	partner = ET.SubElement(Partners, Partner)
	ET.SubElement(partner, "field1").text = "some value1"
	ET.SubElement(partner, "field2").text = "some value2"

tree = ET.ElementTree(Processdata)
tree.write(xml_file)

x = etree.parse(xml_file)
print(etree.tostring(x, pretty_print=True, encoding="unicode"))
