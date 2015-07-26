import npyscreen, curses
import yaml

import dCharSheet as charSheet
from dboxwidget import *
from yamlLoader import *

class NewCharRace(npyscreen.FormBaseNew):
    def create(self):
        races = [race["Name"] for race in race_descriptions]
        # TODO: Make it relative to window size, resize method 
        self.pRace  = self.add(OptionSelector, name="Race", values=races, rely=3, relx=5, max_width=20)
        self.pRace.setParent(self)

        self.optionDisplay = self.add(OptionDisplay, descriptions=race_descriptions, name="Details", autowrap=True, rely=2, relx=-60, contained_widget_arguments={'color': 'WARNING', 'widgets_inherit_color': True})
        self.optionDisplay.updateDescription(0)

        self.pRace.handlers.update({
                curses.KEY_UP: self.updateDescription,
                curses.KEY_DOWN: self.updateDescription,
                curses.KEY_LEFT: self.updateDescription,
                curses.KEY_RIGHT: self.updateDescription,
                curses.ascii.TAB: self.updateDescription 
            })
  
    def updateDescription(self, key):
        if key in [curses.KEY_UP, curses.KEY_LEFT]:
            self.pRace.h_cursor_line_up(key)
        elif key in [curses.KEY_DOWN, curses.KEY_RIGHT]:
            self.pRace.h_cursor_line_down(key)

        self.optionDisplay.updateDescription(self.pRace.cursor_line)
        self.optionDisplay.display()

    def nextForm(self, index):
        charSheet.getCharSheet().raceIndex = index
        race_desc = race_descriptions[index]
        race_desc = [i for sublist in race_desc for i in sublist]
        if "Subraces" in race_descriptions[index].keys():
            change_to = "NEW_CHAR_SUBRACE"
        elif "Draconic Ancestry" in race_descriptions[index].keys():
            change_to = "NEW_CHAR_DRACONIC_ANCESTRY"
        else:
            change_to = "NEW_CHAR_CLASS"

        self.parentApp.change_form(change_to)


class OptionSelector(npyscreen.MultiLineAction):
    def __init__(self, *args, **kwargs):
        super(OptionSelector, self).__init__(*args, **kwargs)

    def setParent(self, parent):
        self.parent = parent

    def actionHighlighted(self, act_on_this, key_press):
        self.parent.nextForm(self.values.index(act_on_this))



class OptionDisplay(dBoxTitle):
    _contained_widget = npyscreen.Pager

    def __init__(self, *args, descriptions=None, **kwargs):
        super(OptionDisplay, self).__init__(*args, **kwargs)
        self.descriptions = descriptions


    def updateDescription(self, index):
        self.values = [": ".join(d) for d in self.descriptions[index]["Details"]]
        # Pad list of values with empty entries between real entries
        self.values = [self.values[int(i/2)] if i%2==0 else '' for i in range(len(self.values)*2-1)]
        self.entry_widget.setValuesWrap(list(self.values))


class NewCharSubRace(npyscreen.FormBaseNew):
    def create(self):
        race_index = charSheet.getCharSheet().raceIndex
        subraces = [subrace["Name"] for subrace in race_descriptions[race_index]["Subraces"]]
        self.pRace  = self.add(OptionSelector, name="Race", values=subraces, rely=3, relx=5, max_width=20)
        self.pRace.setParent(self)

        self.optionDisplay = self.add(OptionDisplay, descriptions=race_descriptions[race_index]["Subraces"], name="Details", autowrap=True, rely=2, relx=-60, contained_widget_arguments={'color': 'WARNING', 'widgets_inherit_color': True})
        self.optionDisplay.updateDescription(0)

        self.pRace.handlers.update({
                curses.KEY_UP: self.updateDescription,
                curses.KEY_DOWN: self.updateDescription,
                curses.KEY_LEFT: self.updateDescription,
                curses.KEY_RIGHT: self.updateDescription,
                curses.ascii.TAB: self.updateDescription 
            })
   
    def updateDescription(self, key):
        if key in [curses.KEY_UP, curses.KEY_LEFT]:
            self.pRace.h_cursor_line_up(key)
        elif key in [curses.KEY_DOWN, curses.KEY_RIGHT]:
            self.pRace.h_cursor_line_down(key)

        self.optionDisplay.updateDescription(self.pRace.cursor_line)
        self.optionDisplay.display()

    def nextForm(self, index):
        charSheet.getCharSheet().subraceIndex = index
        change_to = "NEW_CHAR_CLASS"

        self.parentApp.change_form(change_to)


class NewCharDraconicAncestry(npyscreen.FormBaseNew):
    def create(self):
        #subraces = [subrace["Name"] for subrace in race_descriptions[race_index]["Subraces"]]
        #self.pRace  = self.add(OptionSelector, name="Race", values=subraces, rely=3, relx=5, max_width=20)
        #self.pRace.setParent(self)
        ancestries = race_descriptions[race_index]["Draconic Ancestry"]
        ancestries = [[s.ljust(20, " ") for s in row] for row in ancestries]
        ancestries = ["".join(row) for row in ancestries]
        # Add padding line to separate header from content
        ancestries[1:1] = ['-'*60]

        self.table = self.add(npyscreen.MultiLineAction, 
                name = "Draconic Ancestries",
                values = ancestries,
                relx = 5, rely = 3
            )

        self.table.cursor_line = 2

        self.table.handlers.update({
                curses.KEY_UP: self.checkLine,
                curses.KEY_LEFT: self.checkLine,
                curses.ascii.NL: self.nextForm,
                curses.ascii.CR: self.nextForm
            })
 
  
    def checkLine(self, key):
        if self.table.cursor_line > 2: 
            self.table.h_cursor_line_up(key)


    def nextForm(self, key):
        charSheet.getCharSheet().draconicAncestryIndex = self.table.cursor_line - 1
        change_to = "NEW_CHAR_CLASS"

        self.parentApp.change_form(change_to)



class NewCharClass(npyscreen.FormBaseNew):
    def create(self):
        # TODO: Menu select
        classes = [cls["Name"] for cls in class_descriptions]
        self.pClass  = self.add(OptionSelector, name="Race", values=classes, rely=3, relx=5, max_width=20)
        self.pClass.setParent(self)

        self.optionDisplay = self.add(OptionDisplay, descriptions=class_descriptions, name="Details", autowrap=True, rely=2, relx=-60, contained_widget_arguments={'color': 'WARNING', 'widgets_inherit_color': True})
        self.optionDisplay.updateDescription(0)

        self.pClass.handlers.update({
                curses.KEY_UP: self.updateDescription,
                curses.KEY_DOWN: self.updateDescription,
                curses.KEY_LEFT: self.updateDescription,
                curses.KEY_RIGHT: self.updateDescription,
                curses.ascii.TAB: self.updateDescription 
            })
    
    def updateDescription(self, key):
        if key in [curses.KEY_UP, curses.KEY_LEFT]:
            self.pClass.h_cursor_line_up(key)
        elif key in [curses.KEY_DOWN, curses.KEY_RIGHT]:
            self.pClass.h_cursor_line_down(key)

        self.optionDisplay.updateDescription(self.pClass.cursor_line)
        self.optionDisplay.display()

        self.parentApp.setNextForm("NEW_CHAR_STATS")

    def nextForm(self, index):
        charSheet.getCharSheet().classIndex = index

        change_to = "NEW_CHAR_STATS"

        self.parentApp.change_form(change_to)
        

class NewCharStats(npyscreen.Form):
    def create(self):
        relx = 5
        rely = 3

        self.strField = self.add(npyscreen.TitleText, name='STR', value='10', field_width=20, relx=relx, rely=rely)
        self.dexField = self.add(npyscreen.TitleText, name='DEX', value='10', field_width=20, relx=relx)
        self.conField = self.add(npyscreen.TitleText, name='CON', value='10', field_width=20, relx=relx)
        self.intField = self.add(npyscreen.TitleText, name='INT', value='10', field_width=20, relx=relx)
        self.wisField = self.add(npyscreen.TitleText, name='WIS', value='10', field_width=20, relx=relx)
        self.chaField = self.add(npyscreen.TitleText, name='CHA', value='10', field_width=20, relx=relx)

    def afterEditing(self):
        charSheet.getCharSheet().setStats(newStats = {
             'STR': self.strField.value,
             'DEX': self.dexField.value,
             'CON': self.conField.value,
             'INT': self.intField.value,
             'WIS': self.wisField.value,
             'CHA': self.chaField.value
        })
        self.parentApp.setNextForm("NEW_CHAR_BACKGROUND")
 

class NewCharBackground(npyscreen.FormBaseNew):
    def create(self):
        relx = 5
        rely = 3

        backgrounds = [background["Name"] for background in background_descriptions]

        self.pBackgrounds = self.add(OptionSelector, name="Background", values=backgrounds, rely=3, relx=5, max_width=20)
        self.pBackgrounds.setParent(self)

        self.optionDisplay = self.add(OptionDisplay, descriptions=background_descriptions, name="Details", autowrap=True, rely=2, relx=-60, contained_widget_arguments={'color': 'WARNING', 'widgets_inherit_color': True})
        self.optionDisplay.updateDescription(0)

        self.pBackgrounds.handlers.update({
                curses.KEY_UP: self.updateDescription,
                curses.KEY_DOWN: self.updateDescription,
                curses.KEY_LEFT: self.updateDescription,
                curses.KEY_RIGHT: self.updateDescription,
                curses.ascii.TAB: self.updateDescription 
            })
  
    def updateDescription(self, key):
        if key in [curses.KEY_UP, curses.KEY_LEFT]:
            self.pBackgrounds.h_cursor_line_up(key)
        elif key in [curses.KEY_DOWN, curses.KEY_RIGHT]:
            self.pBackgrounds.h_cursor_line_down(key)

        self.optionDisplay.updateDescription(self.pBackgrounds.cursor_line)
        self.optionDisplay.display()

    def nextForm(self, index):
        charSheet.getCharSheet().backgroundIndex = index

        change_to = None

        self.parentApp.change_form(change_to)


