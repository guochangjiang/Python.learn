#!/usr/bin/python3
#--*-- utf8 --*--

import svgwrite

dwg = svgwrite.Drawing('test.svg', (700, 700), debug=True)
dwg.add(dwg.line((20, 10), (100, 10), stroke=svgwrite.rgb(10, 10, 16, '%')))
dwg.add(dwg.text('Test', insert=(0, 10+3), font_size = 10, fill='red'))
dwg.add(dwg.rect(insert = (20, 20), size = ("200px", "100px"), stroke_width = "1", stroke = "black", fill = "blue"))

width = 0.5
step = width
strokewith = width / 100

for i in range(500):
	if i < 100:
		dwg.add(dwg.rect(insert=(20+i, 200), size = (str(width) + "px", "30px"), stroke_width = strokewith, stroke = "blue", fill = "blue"))
		dwg.add(dwg.rect(insert=(20+i+step, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "blue", fill = "blue"))

	elif i < 200:
		dwg.add(dwg.rect(insert=(20+i, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "red", fill = "red"))
		dwg.add(dwg.rect(insert=(20+i+step, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "red", fill = "red"))
		
	elif i < 300:
		dwg.add(dwg.rect(insert=(20+i, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "green", fill = "green"))
		dwg.add(dwg.rect(insert=(20+i+step, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "green", fill = "green"))
		
	elif i < 400:
		dwg.add(dwg.rect(insert=(20+i, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "purple", fill = "purple"))
		dwg.add(dwg.rect(insert=(20+i+step, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "purple", fill = "purple"))
		
	else:
		dwg.add(dwg.rect(insert=(20+i, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "gray",fill = "gray"))
		dwg.add(dwg.rect(insert=(20+i+step, 200), size = (str(width) + "px", "30px"), stroke_width= strokewith, stroke = "gray", fill = "gray"))


#dwg.add(dwg.text('Hello World', insert=(210, 110))
#print(dwg.tostring())
dwg.save()


