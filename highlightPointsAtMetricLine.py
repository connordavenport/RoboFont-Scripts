
from random import random, randint
from vanilla import FloatingWindow, CheckBox
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import *
from defconAppKit.windows.baseWindow import BaseWindowController

f = CurrentFont()

class highlightPointsOnMetrics(BaseWindowController):

    def __init__(self):
        self.w = FloatingWindow((135, 40), "", minSize=(123, 200))

        # a checkbox to turn the tool on/off
        self.w.showPoints = CheckBox((10, 10, -10, 20), 'highlight points', value=True)

        # add an observer to the drawPreview event
        addObserver(self, "highlightPoints", "draw")

        # open window
        self.setUpBaseWindowBehavior()
        self.w.open()

    def windowCloseCallback(self, sender):
        # remove observer when window is closed
        removeObserver(self, 'draw')
        super(highlightPointsOnMetrics, self).windowCloseCallback(sender)


    def highlightPoints(self, info):
        # check if checkbox is selected
        if not self.w.showPoints.get():
            return

        # get the current glyph
        glyph = info["glyph"]
        sc = info['scale']

        # Anything more than 3 could be considered an intentional overshoot?
        rang = 3 

        asc = f.info.ascender
        xhe = f.info.xHeight
        cap = f.info.capHeight
        dsc = f.info.descender
        size = 8 * sc
        # draw highlight
        stroke(None)
        if glyph is not None:
            for c in glyph:
                for s in c:
                    for p in s:
                        if p.y == asc or p.y == xhe or p.y == cap or p.y == dsc or p.y == 0:
                            pass
                        else:
                            if (asc+-rang <= p.y <= asc+rang) or (xhe+-rang <= p.y <= xhe+rang) or (cap+-rang <= p.y <= cap+rang) or (dsc+-rang <= p.y <= dsc+rang) or (-rang <= p.y <= rang):

                            # fill(1, 0, 0, .6)
                            
                                fill(None)
                                stroke(1.0, 0.0, 0.0, .5)
                                strokeWidth(7 * sc)
                                oval(p.x-size/2, p.y-size/2, size, size)

highlightPointsOnMetrics()
