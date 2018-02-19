import simplejson as json

TRACE_LEVEL = 2
def trace(msg, level=1):
    if level <= TRACE_LEVEL:
        print(msg)

def coordsToStr(coords):
    return chr(coords[0]+97) + chr(coords[1]+97)

def letterToCol(letter):
    return ord(letter) - 97
    
    
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