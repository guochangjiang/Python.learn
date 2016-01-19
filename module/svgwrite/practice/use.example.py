#!/usr/bin/env python3
# coding: utf-8

import svgwrite

dwg = svgwrite.Drawing("use.example.svg", (900, 900), debug=True)
symbol = dwg.symbol(id='symbol')
dwg.defs.add(symbol)
symbol.viewbox(0, 0, 10, 10)
symbol.add(dwg.circle((5,5), r=5))

dwg.add(dwg.use(symbol, insert=(100, 100), size=(10, 10), fill='green'))
dwg.add(dwg.use(symbol, insert=(200, 200), size=(20, 20), fill='red'))
dwg.add(dwg.use(symbol, insert=(300, 300), size=(30, 30), fill='blue'))
dwg.add(dwg.use(symbol, insert=(400, 400), size=(40, 40), fill='pink'))
dwg.add(dwg.use(symbol, insert=(500, 500), size=(50, 50), fill='yellow'))
dwg.add(dwg.use(symbol, insert=(600, 600), size=(60, 60), fill='brown'))
dwg.add(dwg.use(symbol, insert=(700, 700), size=(70, 70), fill='gray'))

text = dwg.add(dwg.g(id = "text.group", font_family="sans-serif", font_size=20, fill='black'))
lines = dwg.add(dwg.g(id = "line.group",stroke_width=10, stroke='green', fill='none'))
lines.add(dwg.polyline([(50, 100), (50, 300), (75, 250), (100, 300), (120, 250), (150, 250), (150, 300)]))
lines.add(dwg.line(start=(50, 100), end=(150, 100)))
dwg.add(dwg.use(lines, (20,100)))
dwg.save()