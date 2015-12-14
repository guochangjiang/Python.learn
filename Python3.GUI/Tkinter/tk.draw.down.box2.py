#coding:utf-8
import sys
import tkinter
import Pmw

class Demo:
    def __init__(self, parent):
        parent.configure(background = 'white')
        self.target = tkinter.Label(
                parent,
                relief = 'sunken',
                padx = 20,
                pady = 20,
        )
        self.target.pack(fill = 'x', padx = 8, pady = 8)
        colours = ('cornsilk1', 'snow1', 'seashell1', 'antiquewhite1',
                    'bisque1', 'peachpuff1', 'navajowhite1', 'lemonchiffon1',
                    'ivory1', 'honeydew1', 'lavenderblush1', 'mistyrose1')
        dropdown = Pmw.ComboBox(
                parent,
                label_text = 'Dropdown ComboBox:',
                labelpos = 'nw',
                selectioncommand = self.changeColour,
                scrolledlist_items = colours,
        )
        dropdown.pack(side = 'left', anchor = 'n',
                    fill = 'x', expand = 1, padx = 8, pady = 8)
        first = colours[0]
        dropdown.selectitem(first)
        self.changeColour(first)
    def changeColour(self, colour):
        print('Colour: ' + colour)
        self.target.configure(background = colour)
if __name__ == '__main__':
    root = tkinter.Tk()
    Pmw.initialise(root)
    widget = Demo(root)
    root.mainloop()