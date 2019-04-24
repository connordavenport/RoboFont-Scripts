# Soft Otter Tools


from vanilla import *
from mojo.events import addObserver

########## markingTool

class markingTool(object):
    def __init__(self):
        self.w = FloatingWindow((200, 165))
        self.w.button = Button((10, 10, -10, 20), "mark",
                            callback=self.toggleDrawer)
        self.d = Drawer((180, 120), self.w)
        self.d.componentsAndOutlinesButton = Button((10, 10, -10, 20), "comp. + outlines", callback=self.componentsAndOutlinesCallback)
        self.d.componentsButton = Button((10,40,-10,20), 'components', callback=self.componentsCallback)
        self.d.usedAsComponentButton = Button((10,70,-10,20), 'used as components', callback=self.usedAsComponentCallback)
        self.w.open()
        # self.d.open()
                
    def toggleDrawer(self, sender):
        self.d.toggle()

##### Callbacks
        
    def componentsAndOutlinesCallback(self, sender):
        font = CurrentFont()
        glyph = CurrentGlyph()
        print('>>> Glyphs combining components and outlines:\n')
        for glyph in font:
            if len(glyph.contours) > 0 and len(glyph.components) > 0:
                glyph.prepareUndo('mark components and outlines')
                glyph.markColor = 1, 0, 0.5, 0.35
                glyph.performUndo()
                print(glyph.name, end=" ")
        print('\n')
        
                
    def componentsCallback(self,sender):
        font = CurrentFont()
        glyph = CurrentGlyph()
        print('>>> Glyphs completely made out of components:\n')
        for glyph in font:
            if len(glyph.contours) == 0 and len(glyph.components) > 0:
                glyph.prepareUndo('mark components')
                glyph.markColor = 0, 0.25, 0.5, 0.35
                glyph.performUndo()
                print(glyph.name, end = " ")
        print('\n')
        
    def usedAsComponentCallback(self, sender):
        font = CurrentFont()
        glyph = CurrentGlyph()

        print('>>> These glyphs are used as components\n')
        for component in glyph.components:
            baseGlyph = font[component.baseGlyph]
            print(component.baseGlyph)
            baseGlyph.prepareUndo('marks glyphs used as components')
            baseGlyph.markColor = 0.5, 0, 1, 0.35
            baseGlyph.performUndo()
        print('\n')

########## outlineTool 

##### remove overlaps

class removeOverlaps(object):

    def __init__(self, parentWindow):
        self.w = Sheet((250, 100), parentWindow)
        self.w.removeButton = Button((10, 10, -10, 20), "remove overlap in current glyph", callback=self.removeCurrentButton)
        self.w.removeAllButton = Button((10, 40, -10, 20), "remove overlap in all glyphs", callback=self.removeAllButton)
        self.w.myTextBox = TextBox((10, 70, -10, 17), "removing the overlaps")
        self.w.closeButton = Button((-90, -30, 80, 22), "close", self.closeCallback)
        self.w.open()
        
        
##### Callbacks to remove Overlaps

    def removeCurrentButton(self, sender):
        
        font = CurrentFont()
        glyph = CurrentGlyph()

        if glyph.hasOverlap():
            glyph.prepareUndo('remove overlap in current glyph')
            glyph.removeOverlap()
            glyph.markColor = None
            glyph.performUndo()
            print('removed overlap in:', glyph.name)
            self.w.close()
        
    def removeAllButton(self,sender):
        print('\nthis might take a while\n')
        font = CurrentFont()
        glyph = CurrentGlyph()
    
        print('removed overlap in:')
        for glyph in font:
            if glyph.hasOverlap():
                glyph.prepareUndo('remove overlap in current glyph')
                glyph.removeOverlap()
                glyph.markColor = None
                glyph.performUndo()
                print(glyph.name)
        print()
        self.w.close()

        



    def closeCallback(self, sender):
        self.w.close()

##### set the direction


class setDirection(object):

    def __init__(self, parentWindow):
        self.w = Sheet((250, 185), parentWindow) 
        self.w.setPSButton = Button((10, 10, -10, 20), 'set PS direction in current glyph', callback=self.setPSButton)
        self.w.setAllPSButton = Button((10, 40, -10, 20), 'set PS direction in all glyphs', callback=self.setAllPSButton)
        self.w.setTTButton = Button((10,70,-10, 20), 'set TT direction in current glyph', callback=self.setTTButton)
        self.w.setAllTTButton = Button((10, 100, -10, 17), 'set TT direction in all glyphs', callback=self.setAllTTButton)
        self.w.myTextBox = TextBox((10, 130, -10, 17), 'changing the paths direction')
        self.w.closeButton = Button((-90, -30, 80, 22), 'close', self.closeCallback)
        self.w.open()
                
##### Callbacks to set the direction

    def setPSButton(self, sender):
        
        font = CurrentFont()
        glyph = CurrentGlyph()


        for contour in glyph.contours:
            glyph.correctDirection(trueType=False)
        print('Corrected the direction of _%s_ following the PostScript recommendations' % glyph.name)
        glyph.changed()
        print()
        self.w.close()
        
    def setAllPSButton(self,sender):
        font = CurrentFont()
        glyph = CurrentGlyph()
        
        print('all outlines set to PS')
        for glyph in font:
            for contour in glyph.contours:
                glyph.correctDirection(trueType=False)
            glyph.changed()
        
        print()
        self.w.close()
        
    def setTTButton(self, sender):
        font = CurrentFont()
        glyph = CurrentGlyph()
        
        for contour in glyph.contours:
            glyph.correctDirection(trueType=True)
        print('Corrected the direction of _%s_ following the TrueType recommendations' % glyph.name)
        glyph.changed()
        print()
        self.w.close()

    def setAllTTButton(self,sender):
        font = CurrentFont()
        glyph = CurrentGlyph()
        
        print('all outlines set to TT')
        for glyph in font:
            for contour in glyph.contours:
                glyph.correctDirection(trueType=True)
            glyph.changed()
        
        print()
        self.w.close()



    def closeCallback(self, sender):
        self.w.close()





class outlineTool(object):

    def __init__(self):

        self.w = FloatingWindow((300, 75), title='Outline Tool')
        self.w.overlaps = Button((10, 10, -10, 22), "remove overlaps", callback=self.removeOverlapsCallback)
        self.w.direction = Button((10, 40, -10, 22), 'direction', callback=self.setDirectionCallback)
        self.w.open()

    def removeOverlapsCallback(self, sender):
        removeOverlaps(self.w) 
        
    def setDirectionCallback(self, sender):
         setDirection(self.w)

########## SoftOtterTool in Inspector

class SoftOtterTools(object):

    def __init__(self):
        # subscribe to the moment when an inspector will be shown
        addObserver(self, "inspectorWindowWillShowDescriptions", "inspectorWindowWillShowDescriptions")
        # keep a reference of the view inserted in the inspector
        self.editor = Group((0, 0, -0, -0))
        self.editor.markingToolButton = Button((10,10,-10,20), 'Marking Tool', callback=self.markingToolCallback)
        self.editor.outlineToolButton = Button((10,40,-10,20), 'Outline Tool', callback=self.outlineToolCallback)

    def inspectorWindowWillShowDescriptions(self, notification):
        # create an inspector item
        item = dict(label="Soft Otter Tool", view=self.editor)
        # insert or append the item to the list of inspector panes
        notification["descriptions"].insert(1, item)
        
    def markingToolCallback(self, sender):
        markingTool()
        
    def outlineToolCallback(self, sender):
        outlineTool()

    

SoftOtterTools()