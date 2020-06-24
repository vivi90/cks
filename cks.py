import sys
from zipfile import ZipFile
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment

# Get filename
filename = sys.argv[1].split(".")[0]

# Extract Krita document
ZipFile(filename + ".kra").extractall(filename)

# Prepare
svg = Element("svg")
svg.set("xmlns", "http://www.w3.org/2000/svg")
svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
svg.set("xmlns:krita", "http://krita.org/namespaces/svg/krita")
svg.set("xmlns:sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")


# Save
ElementTree(svg).write(filename + ".svg")
