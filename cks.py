from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment

# Prepare
svg = Element("svg")
svg.set("xmlns", "http://www.w3.org/2000/svg")
svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
svg.set("xmlns:krita", "http://krita.org/namespaces/svg/krita")
svg.set("xmlns:sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

# Save
ElementTree(svg).write("merged.svg")
