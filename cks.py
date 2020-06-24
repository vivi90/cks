from sys import argv as argument
from zipfile import ZipFile
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment
from shutil import rmtree as delete

class Application:
    NAMESPACE_KRITA = "http://www.calligra.org/DTD/krita"

    def __init__(self, filename):
        self.filename = filename
        self.prepare()

    def prepare(self):
        self.svg = Element("svg")
        self.svg.set("xmlns", "http://www.w3.org/2000/svg")
        self.svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        self.svg.set("xmlns:krita", "http://krita.org/namespaces/svg/krita")
        self.svg.set("xmlns:sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

    def extractKritaDocument(self):
        ZipFile(self.filename + ".kra").extractall(self.filename)

    def cleanup(self):
        delete(self.filename)

    def save(self):
        ElementTree(self.svg).write(self.filename + ".svg")

    def mergeLayers(self):
        namespace = {"krita": self.NAMESPACE_KRITA}
        root = ElementTree(ElementTree().parse(self.filename + "/maindoc.xml")).getroot()
        imageName = root.find("./krita:IMAGE", namespace).get("name")
        layers = root.find("./krita:IMAGE/krita:layers", namespace)
        def walkRecursive(layer):
            if layer.get("visible") == "1":
                if layer.get("nodetype") == "grouplayer":
                    # Sublayers
                    for subLayer in layer.find("./krita:layers", namespace):
                        walkRecursive(subLayer)
                else:
                    if layer.get("nodetype") == "shapelayer":
                        self.addLayer(self.filename + "/" + imageName + "/layers/" + layer.get("filename") + "." + layer.get("nodetype") + "/content.svg")
            return
        for layer in layers:
            if layer.get("visible") == "1":
                walkRecursive(layer)

    def addLayer(self, path):
        print(path)

export = Application(argument[1].split(".")[0])
export.extractKritaDocument()
export.mergeLayers()
export.save()
#export.cleanup()
del export
