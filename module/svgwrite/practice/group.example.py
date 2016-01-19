#!/usr/bin/env python3
# coding: utf-8

import svgwrite

dwg = svgwrite.Drawing("group.example.svg", (900, 900), debug=True)
text = dwg.add(dwg.g(id = "text.group", font_family="sans-serif", font_size=20, fill='black'))
lines = dwg.add(dwg.g(id = "line.group",stroke_width=10, stroke='green', fill='none'))
text.add(dwg.text("title1", insert=(0, 25)))
text.add(dwg.text("title2", font_size=30, insert=(0, 50)))
lines.add(dwg.line(start=(50, 100), end=(150, 100)))
lines.add(dwg.polyline([(50, 250), (50, 300), (75, 250), (100, 300), (120, 250), (150, 250), (150, 300)]))
dwg.save()