#!/usr/bin/env python
import npyscreen, curses
import yaml

from dboxwidget import *
from dNewChar import *

class Duiker(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", IntroForm, name="Duiker Character Sheet Editor", color="IMPORTANT",)
        self.addForm("NEW_CHAR_RACE", NewCharRace, name="Character Creator", color="WARNING",  )
        self.addFormClass("NEW_CHAR_SUBRACE", NewCharSubRace, name="Character Creator", color="WARNING",  )
        self.addFormClass("NEW_CHAR_DRACONIC_ANCESTRY", NewCharDraconicAncestry, name="Character Creator", color="WARNING",  )
        self.addForm("NEW_CHAR_CLASS", NewCharClass, name="Character Creator", color="WARNING",  )
        self.addForm("NEW_CHAR_STATS", NewCharStats, name="Character Creator", color="WARNING",  )
        self.addForm("NOT_IMPLEMENTED", IntroForm, name="Not implemented yet", color="WARNING",)
        
    
    def change_form(self, name):
        self.switchForm(name)
   
   
class IntroForm(npyscreen.FormBaseNew):
    def create(self):
        self.menu = self.add(NavMenu, name="Text:", values=["New character", "Load character", "Exit"])
        self.menu.setParentApp(self.parentApp)
    
    

class NavMenu(npyscreen.MultiLineAction):
    def __init__(self, *args, **kwargs):
        super(NavMenu, self).__init__(*args, **kwargs)

    def setParentApp(self, parentApp):
        self.parentApp = parentApp

    def actionHighlighted(self, act_on_this, key_press):
        index = self.values.index(act_on_this)

        if index == 0:
            change_to = "NEW_CHAR_RACE"
        elif index == 1:
            change_to = "NOT_IMPLEMENTED"
        elif index == 2:
            change_to = None

        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)


def main():
    duiker = Duiker()
    duiker.run()


if __name__ == '__main__':
    main()
