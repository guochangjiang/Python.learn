#!/usr/bin/env python3
# coding: utf-8

import svgwrite

dwg = svgwrite.Drawing("text.example.svg", (1000, 1800), debug=True)
paragraph = dwg.add(dwg.g(font_size=14))
paragraph.add(dwg.text("This is a Test!", (10,20)))

#横向位置
paragraph.add(dwg.text("Test!", insert=(450, 20),
        text_anchor='middle', font_family="sans-serif", font_size='25px', fill='black'))
paragraph.add(dwg.text("Test!", insert=(450, 20),
        text_anchor='start', font_family="sans-serif", font_size='25px', fill='red'))
paragraph.add(dwg.text("Test!", insert=(450, 20),
        text_anchor='end', font_family="sans-serif", font_size='25px', fill='green'))
paragraph.add(dwg.text("Test!", insert=(450, 20),
        text_anchor='inherit', font_family="sans-serif", font_size='25px', fill='blue'))
dwg.add(dwg.line((0,20),(1000,20),stroke="red"))

#纵向位置
poslist=["auto", "use-script", "no-change", "reset-size", "ideographic", "alphabetic", "hanging", "mathematical", "central", "middle", "text-after-edge", "text-before-edge", "inherit"]
allpos = "\t##abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
y = 100
for db in poslist:
    paragraph.add(dwg.text(db+allpos, insert=(0, y),
        dominant_baseline=db, font_family="sans-serif", font_size='25px', fill='blue'))
    dwg.add(dwg.line((0,y),(1000,y),stroke="red"))
    y = y + 50

#字符纵向位移
paragraph.add(dwg.text("This is a Test", x=[10], y=[y, y+5,y+10, y+15, y+20]))
#字符横向位置
paragraph.add(dwg.text("This is a Test", x=[5, 10, 20, 25, 30, 100], y=[y+50]))
#字符串内部格式变化
atext = dwg.text("A", font_size='1.0em', insert=(10, y+80))
atext.add(dwg.tspan(' Word', font_size='1.5em', fill='red'))
atext.add(dwg.tspan(' is a Word!', font_size='0.7em', fill='green'))
paragraph.add(atext)

#字符串位移
paragraph.add(dwg.text("This is a Test", (10, y+120)))
paragraph.add(dwg.text("ThisisaTest", (10, y+140), dx=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], fill = "brown"))
paragraph.add(dwg.text("ThisisaTest", (10, y+160), dy=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], fill = "blue"))
paragraph.add(dwg.text("ThisisaTest", (10, y+180), dx=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], dy=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], fill = "red"))

#字符串中单个字符旋转
paragraph.add(dwg.text("This is a Test", (10, y+200), rotate=[90]))


#paragraph.add(dwg.text("This is a Test", (10, y+220),  transform="rotate(30)"))
#字符串整体旋转

#错误的方法
text = dwg.add(dwg.g(id = "text.group", font_family="sans-serif", font_size=20, fill='black'))
text.add(dwg.text("PhD", insert=(10, y+220)))
for i in range(3,90,3):
    rottext = "translate(10,0)rotate(-"+ str(i) + ")"
    text.add(dwg.text("PhD", insert=(10, y+220), transform=rottext))
for i in range(3,90,3):
    rottext = "translate(0,50)rotate(-"+ str(i) + ")"
    text.add(dwg.text("PhD", insert=(10, y+220), transform=rottext))
for i in range(3,90,3):
    rottext = "translate(0,-200)rotate(-"+ str(i) + ")"
    text.add(dwg.text("PhD", insert=(10, y+220), transform=rottext))
for i in range(3,90,3):
    rottext = "translate(0,-800)rotate(-"+ str(i) + ")"
    text.add(dwg.text("PhD", insert=(10, y+220), transform=rottext))

#正确的两种方法
#1
textrotation0 = dwg.add(dwg.g(transform="translate(300,1200)"))
for i in range(1, 360, 10):
    textrotation1= textrotation0.add(dwg.g(transform="rotate(" + str(i) + ")"))
    textrotation1.add(dwg.text("This is a rotation test1", insert = (0, 0), fill = "black", font_size="20"))
#2
dwg.add(dwg.text("This is a rotation test2", insert = (0, 0), fill = "red", font_size="20", transform="translate(50, 1200)rotate(30)"))
dwg.add(dwg.text("This is a rotation test2", insert = (0, 0), fill = "red", font_size="20", transform="translate(50, 1200)rotate(50)"))
dwg.add(dwg.text("This is a rotation test2", insert = (0, 0), fill = "red", font_size="20", transform="translate(50, 1200)rotate(70)"))

#直线以其一端为圆心旋转
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(0)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(10)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(20)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(30)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(40)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(50)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(60)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(70)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(80)"))
dwg.add(dwg.line(start = (0, 0), end = (150,0),stroke_width=10, stroke="blue",  transform="translate(50, 1400)rotate(90)"))

#直线以其中心为圆心旋转
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(0)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(10)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(20)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(30)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(40)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(50)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(60)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(70)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(80)"))
dwg.add(dwg.line(start = (-100, 0), end = (100,0),stroke_width=10, stroke="blue",  transform="translate(350, 1400)rotate(90)"))
print(textrotation1.attribs)
print("hello")
dwg.save()
