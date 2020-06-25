# CKS

## About
This [Python](https://www.python.org) script exports all vector layers from a given [Krita](https://krita.org) document (`*.kra` file) into a single [SVG](https://www.w3.org/TR/SVG11) file.

## Usage
This script requires the path of the Krita file as the first parameter:

`cks.py example.kra`

It will finally create a SVG file in the same directory, including all vector layers of the Krita file.

## Known bugs
Some gradients with transparent parts might not rendered properly.
Maybe it will become improved with the development of Krita.

## Contribution
* Souce code documentation: [reStructuredText](https://docutils.sourceforge.io/rst.html)
* XML parsing: [xml.etree.ElementTree](https://docs.python.org/3/library/xml.etree.elementtree.html) implementation of the ElementTree API

## License
This script is free software under the terms of the GNU General Public License v3 as published by the Free Software Foundation.
It is distributed WITHOUT ANY WARRANTY (without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE).
For more details please see the LICENSE file or: http://www.gnu.org/licenses

## Credits
* 2020 by Vivien Richter <vivien-richter@outlook.de>
* Git repository: https://github.com/vivi90/cks.git
