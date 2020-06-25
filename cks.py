#!/usr/bin/python
"""This script exports all vector layers from a given Krita document into a single SVG file.

*Usage:* cks [KRITA_FILE]

:Author: Vivien Richter
:Version: 1.1.0
:License: `GNU General Public License v3.0 <https://www.gnu.org/licenses>`_
:Repository: `GitHub <https://github.com/vivi90/cks.git>`_
"""

from sys import argv as arguments
from os.path import getsize, isfile
from zipfile import ZipFile
from xml.etree.ElementTree import ElementTree, Element
from shutil import rmtree as delete

class Application:
    '''This class wraps all necessary functionality'''

    NAMESPACE_KRITA = {"krita": "http://www.calligra.org/DTD/krita"}
    NAMESPACE_SVG = {"svg": "http://www.w3.org/2000/svg"}

    def __init__(self, file: str) -> None:
        """Constructor.

        :param file: The Krita document file path.
        """

        self.filename = file.split(".")[0]
        self.prepare()

    def prepare(self) -> None:
        '''Prepares SVG export structure.'''

        self.svg = Element("svg")
        self.svg.set("xmlns", "http://www.w3.org/2000/svg")
        self.svg.set("xmlns:xlink", "http://www.w3.org/1999/xlink")
        self.svg.set("xmlns:krita", "http://krita.org/namespaces/svg/krita")
        self.svg.set("xmlns:sodipodi", "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")
        self.svg.append(Element("defs"))

    def extractKritaDocument(self) -> None:
        '''Extracts all content of the ZIP compressed Krita document.'''

        ZipFile(self.filename + ".kra").extractall(self.filename)

    def cleanup(self) -> None:
        '''Removes all extracted content.'''

        delete(self.filename)

    def save(self) -> None:
        '''Saves the final SVG file.'''

        ElementTree(self.svg).write(self.filename + ".svg")

    def findLayers(self) -> None:
        '''Detects all vector layers inside the extracted Krita document.'''

        self.layers = []
        root = ElementTree(ElementTree().parse(self.filename + "/maindoc.xml")).getroot()
        imageName = root.find("./krita:IMAGE", self.NAMESPACE_KRITA).get("name")
        layers = root.find("./krita:IMAGE/krita:layers", self.NAMESPACE_KRITA)
        def walkRecursive(layer):
            if layer.get("visible") == "1":
                if layer.get("nodetype") == "grouplayer":
                    # Sublayers
                    for subLayer in layer.find("./krita:layers", self.NAMESPACE_KRITA):
                        walkRecursive(subLayer)
                else:
                    if layer.get("nodetype") == "shapelayer":
                        self.layers.append([layer.get("filename"), self.filename + "/" + imageName + "/layers/" + layer.get("filename") + "." + layer.get("nodetype") + "/content.svg"])
                        #self.addLayer(self.filename + "/" + imageName + "/layers/" + layer.get("filename") + "." + layer.get("nodetype") + "/content.svg")
            return
        for layer in layers:
            if layer.get("visible") == "1":
                walkRecursive(layer)

    def addLayers(self) -> None:
        '''Adds detected vector layers to the prepared SVG export structure.'''

        defs = self.svg.find("./defs")
        self.layers.reverse()
        for layer in self.layers:
            if getsize(layer[1]) > 0:
                defMap = []
                root = ElementTree(ElementTree().parse(layer[1])).getroot()
                self.svg.set("width", root.get("width"))
                self.svg.set("height", root.get("height"))
                self.svg.set("viewBox", root.get("viewBox"))
                for defElement in root.find("./svg:defs", self.NAMESPACE_SVG):
                    newId = layer[0] + "-" + defElement.get("id")
                    defMap.append([defElement.get("id"), newId])
                    defElement.set("id", newId)
                    defs.append(defElement)
                group = Element("g")
                group.set("id", layer[0])
                for child in root:
                    if child.tag != "{" + self.NAMESPACE_SVG["svg"] + "}defs":
                        for attribute in child.attrib:
                            for defMapEntry in defMap:
                                child.set(attribute, child.get(attribute).replace(defMapEntry[0], defMapEntry[1]))
                        group.append(child)
                self.svg.append(group)

# Running all steps:
if len(arguments) > 1:
    file = arguments[1]
    if isfile(file):
        export = Application(file)
        export.extractKritaDocument()
        export.findLayers()
        export.addLayers()
        export.save()
        export.cleanup()
        del export
    else:
        print("File not found, aborting.")
else:
    print(__doc__)
