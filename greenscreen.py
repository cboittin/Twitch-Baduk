import os
from threading import Timer

import PIL, PIL.ImageDraw, PIL.ImageFont

from util import trace, settings

class GreenScreenGenerator:
    
    def __init__(self):
        self.gsImagePath = settings["greenscreen_image_path"]
        self.gsBaseImageSize = (760, 760) 
        self.antialias = 4
        
        w = self.gsBaseImageSize[0] * self.antialias
        h = self.gsBaseImageSize[1] * self.antialias
        self.gsTopleft = (int(settings["greenscreen_padding_left"]), int(settings["greenscreen_padding_top"]))
        self.gsDimensions = (w - int(settings["greenscreen_padding_right"]) - self.gsTopleft[0], \
                             h - int(settings["greenscreen_padding_bottom"]) - self.gsTopleft[1] \
                             )
        fontPath = os.path.join(".", "greenscreen", "fonts", "steelfis.ttf") # https://fontlibrary.org/en/font/steelfish
        self.gsFont = PIL.ImageFont.truetype(fontPath, size=22 * self.antialias)
        
        # Initialize empty greenscreen image
        self.gsBaseImage = PIL.Image.new(mode='RGB', size=self.gsBaseImageSize, color=(0, 255, 0))
        self.gsBaseImage.save(self.gsImagePath)
        
        self.baseTimeVariation = int(settings["base_variation_displaying_time"])
        self.timePerStone = int(settings["variation_displaying_time_per_stone"])
        
    def generateGreenScreen(self, variation, user):
        trace("Generating GreenScreen image for variation %s" % variation, 2)
        drawSize = (self.gsBaseImageSize[0] * self.antialias, self.gsBaseImageSize[1] * self.antialias)
        output = PIL.Image.new(mode='RGB', size=drawSize, color=(0, 255, 0))
        drawContext = PIL.ImageDraw.Draw(output)
        for i in range(len(variation)):
            move, color = variation[i]
            x, y = move
            left = self.gsTopleft[0] + self.gsDimensions[0] * x / 19 + self.antialias * 2
            top = self.gsTopleft[1] + self.gsDimensions[1] * y / 19 + self.antialias * 2
            right = self.gsTopleft[0] + self.gsDimensions[0] * (x + 1) / 19 - self.antialias * 2 
            bottom = self.gsTopleft[1] + self.gsDimensions[1] * (y + 1) / 19 - self.antialias * 2
            
            # Draw an outlined circle
            offset = self.antialias
            drawContext.ellipse( (left, top, right, bottom), outline="black", fill="black" )
            drawContext.ellipse( (left + offset, top + offset, right - offset, bottom - offset), outline="white", fill="white" )
            drawContext.ellipse( (left + offset*2, top + offset*2, right - offset*2, bottom - offset*2), outline="black", fill="black" )
            drawContext.ellipse( (left + offset*3, top + offset*3, right - offset*3, bottom - offset*3), fill=(0,255,0), outline=(0,255,0) )
            
            # Draw the move number
            moveNumber = str(i)
            w, h = drawContext.textsize(moveNumber, font=self.gsFont)
            W = right - left
            H = bottom - top
            textX = left + 2 + (W - w) / 2
            textY = top - 2 + (H - h) / 2
            drawContext.text( (textX - offset, textY - offset), moveNumber, font=self.gsFont, fill="black")
            drawContext.text( (textX + offset, textY - offset), moveNumber, font=self.gsFont, fill="black")
            drawContext.text( (textX - offset, textY + offset), moveNumber, font=self.gsFont, fill="black")
            drawContext.text( (textX + offset, textY + offset), moveNumber, font=self.gsFont, fill="black")
            drawContext.text( (textX, textY), moveNumber, font=self.gsFont, fill="white")
            
        output = output.resize(self.gsBaseImageSize, PIL.Image.ANTIALIAS)
        output.save(self.gsImagePath)
        
        t = self.baseTimeVariation + len(variation) * self.timePerStone
        timer = Timer(t, self.resetGreenScreen)
        timer.start()
    
    def resetGreenScreen(self):
        trace("Clearing on-screen variation", 1)
        self.gsBaseImage.save(self.gsImagePath)
