from sys import argv as argument
from zipfile import ZipFile
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment
from shutil import rmtree as delete
import xml.etree.ElementTree as et

class Application:
    def __init__(self, filename):
        self.filename = filename

    def extractKritaDocument(self):
        ZipFile(self.filename + ".kra").extractall(self.filename)

    def cleanup(self):
        delete(self.filename)

    def save(self):
        svg = Element("svg")
        svg.set("xmlns", "http://www.w3.org/2000/svg")
        svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        svg.set("xmlns:krita", "http://krita.org/namespaces/svg/krita")
        svg.set("xmlns:sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
        ElementTree(svg).write(self.filename + ".svg")

    def findLayers(self):
        structure = et.parse(self.filename + "/maindoc.xml")
        root = structure.getroot()
        namespace = {"krita": "http://www.calligra.org/DTD/krita"}
        layers = root.find("./krita:IMAGE/krita:layers", namespace)
        def recur(layer):
            if layer.get("visible") == "1":
                if layer.get("nodetype") == "grouplayer":
                    # Sublayers
                    for subLayer in layer.find("./krita:layers", namespace):
                        recur(subLayer)
                else:
                    if layer.get("nodetype") == "shapelayer":
                        print(layer.get("name"))
            return
        recur(layers)
        for layer in layers:
            if layer.get("visible") == "1":
                recur(layer)
        #print([elem.tag for elem in root.iter()])


export = Application(argument[1].split(".")[0])
export.extractKritaDocument()
export.findLayers()
#export.save()
#export.cleanup()
del export
