from sys import argv as argument
from os.path import getsize
from zipfile import ZipFile
from xml.etree.ElementTree import ElementTree, Element
from shutil import rmtree as delete

class Application:
    NAMESPACE_KRITA = "http://www.calligra.org/DTD/krita"
    NAMESPACE_SVG = "http://www.w3.org/2000/svg"

    def __init__(self, filename):
        self.filename = filename
        self.prepare()

    def prepare(self):
        self.svg = Element("svg")
        self.svg.set("xmlns", self.NAMESPACE_SVG)
        self.svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        self.svg.set("xmlns:krita", "http://krita.org/namespaces/svg/krita")
        self.svg.set("xmlns:sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

    def extractKritaDocument(self):
        ZipFile(self.filename + ".kra").extractall(self.filename)

    def cleanup(self):
        delete(self.filename)

    def save(self):
        ElementTree(self.svg).write(self.filename + ".svg")

    def findLayers(self):
        self.layers = []
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
                        self.layers.append([layer.get("filename"), self.filename + "/" + imageName + "/layers/" + layer.get("filename") + "." + layer.get("nodetype") + "/content.svg"])
                        #self.addLayer(self.filename + "/" + imageName + "/layers/" + layer.get("filename") + "." + layer.get("nodetype") + "/content.svg")
            return
        for layer in layers:
            if layer.get("visible") == "1":
                walkRecursive(layer)

    def addLayers(self):
        self.layers.reverse()
        for layer in self.layers:
            if getsize(layer[1]) > 0:
                namespace = {"svg": self.NAMESPACE_SVG}
                root = ElementTree(ElementTree().parse(layer[1])).getroot()
                self.svg.set("width", root.get("width"))
                self.svg.set("height", root.get("height"))
                self.svg.set("viewBox", root.get("viewBox"))
                group = Element("g")
                group.set("id", layer[0])
                for child in root:
                    group.append(child)
                self.svg.append(group)

export = Application(argument[1].split(".")[0])
export.extractKritaDocument()
export.findLayers()
export.addLayers()
export.save()
export.cleanup()
del export
