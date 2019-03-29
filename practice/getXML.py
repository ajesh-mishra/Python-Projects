import xml.etree.cElementTree as ET

Processdata = ET.Element("Processdata")
Partners = ET.SubElement(Processdata, "Partners")

for i in range(1, 4):
	Partner = "Partner_" + str(i)
	partner = ET.SubElement(Partners, Partner)
	ET.SubElement(partner, "field1").text = "some value1"
	ET.SubElement(partner, "field2").text = "some value2"

tree = ET.ElementTree(Processdata)

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")




tree.write("filename.xml")


with open("filename.xml", 'r') as f:
	xml_data = f.read()
	
print(xml_data)
