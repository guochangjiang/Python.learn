#!/usr/bin/python3
#--*-- coding: utf8 --*--

import svgwrite

dwg = svgwrite.Drawing('coordinate.test.svg', (700, 700), debug=True)
dwg.add(dwg.line(
    (5, 5), 
    (500, 5),
    stroke_width = 10,
    stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(
    (5, 5), 
    (5, 500),
    stroke_width = 10,
    stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.line(
    (0, 5), 
    (5, 5),
    stroke="red"))
dwg.add(dwg.text(
    'Test', 
    insert=(5, 10),
    font_size = 10, 
    fill='red'))
dwg.add(dwg.rect(
    insert=(10, 10), 
    size = ("10px", "10px"), 
    stroke = "blue", fill = "blue"))
dwg.add(dwg.circle(
    center=(20, 20), r='10px', fill = "red"))
dwg.add(dwg.ellipse(
    center=(20, 30), r=('10px', '20px'), fill = "green",opacity=0.5))
dwg.save()