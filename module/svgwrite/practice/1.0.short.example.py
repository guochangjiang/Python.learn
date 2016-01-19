#!/usr/bin/env python3
# coding: utf-8

import svgwrite
dwg = svgwrite.Drawing("1.0.svg", height = 1e+2, width = 100)
link = dwg.add(dwg.a("http://www.bioinfotools.cn"))
square = link.add(dwg.rect((0, 0), (50, 50), fill='blue'))
dwg.save()

#profile
dwg = svgwrite.Drawing('1.0.test1.svg', profile='tiny') #svg 1.2
dwg.add(dwg.line((0, 0), (100, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 0.2)))
dwg.save()
dwg = svgwrite.Drawing('1.0.test2.svg', profile='full') #svg 1.1
dwg.add(dwg.line((0, 0), (100, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 0.2)))
dwg.save()
dwg.saveas("1.0.test3.saveas.svg")
print("get_xml:\n", dwg.get_xml())
print("\ntostring:\n", dwg.tostring())

#marker
dwg = svgwrite.Drawing("2.0.marker.svg")
# create a new marker object
marker = dwg.marker(insert=(5,5), size=(10,10))
#marker.viewbox(minx=-5, miny=-5, width=10, height=10)
# red point as marker
marker.add(dwg.circle((5, 5), r=5, fill='red', opacity = 0.5))
# add marker to defs section of the drawing
dwg.defs.add(marker)
marker0 = dwg.marker(insert=(4,4), size=(8,8))
marker0.add(dwg.circle((4, 4), r=4, fill='blue', opacity = 0.5))
dwg.defs.add(marker0)

marker2 = dwg.marker(insert=(6,6), size=(12,12))
marker2.add(dwg.circle((6, 6), r=6, fill='green', opacity = 0.5))
dwg.defs.add(marker2)
# create a new line object
line = dwg.add(dwg.polyline(
[(10, 10), (50, 20), (70, 50), (100, 30)],
stroke='black', fill='none'))
# set marker (start, mid and end markers are the same)
line.set_markers((marker0,marker,marker2))
# or set markers direct as SVG Attributes 'marker-start', 'marker-mid',
# 'marker-end' or 'marker' if all markers are the same.
#line['marker'] = marker.get_funciri()
dwg.save()