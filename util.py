import simplejson as json

settings = None
class Settings:
    def __init__(self):
        if settings is None:
            settingsFile = open("settings.json")
            self.data = json.load(settingsFile)
            settingsFile.close()
            
    def __getitem__(self, item):
        return self.data[item]

settings = Settings()

def trace(msg, level=1):
    if level <= settings["verbose_level"]:
        print(msg)

def coordsToStr(coords):
    return chr(coords[0]+97) + chr(coords[1]+97)

def letterToCol(letter):
    return ord(letter) - 97
    
    