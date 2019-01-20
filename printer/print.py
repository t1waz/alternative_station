import os
import barcode
from barcode.writer import ImageWriter
import cairosvg
import svgutils


# EAN = barcode.get_barcode_class('ean13')

# ean = EAN('5901234123457')
# ean.save('new_barcode')

# svg = svgutils.transform.fromfile('new_barcode.svg')
# originalSVG = svgutils.compose.SVG('new_barcode.svg')
# originalSVG.scale_xy(2,2)

# figure = svgutils.compose.Figure(svg.height, svg.width, originalSVG)
# figure.save('svgNew.svg')

cairosvg.svg2pdf(url='new_barcode.svg', write_to='bar.pdf')

os.system("lpr -P DYMO bar.pdf")