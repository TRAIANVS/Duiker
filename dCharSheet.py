from collections import Counter

class CharacterSheet():
    def __init__(self, 
            name    = None, 
            race    = None, 
            subrace = None, 
            clss    = None,
            stats   = None,
            index   = None):
        self.name = name
        self.raceIndex = race
        self.subraceIndex = subrace
        self.classIndex = clss
        self.backgroundIndex = index
        self.stats = stats or Counter(STR=10, DEX=10, CON=10, INT=10, WIS=10, CHA=10)

    
    def setStats(self, **newStats):
        self.stats = Counter(**newStats)


gCharacterSheet = None

def setCharSheet(newSheet):
    global gCharacterSheet
    gCharacterSheet = newSheet

def getCharSheet():
    return gCharacterSheet
