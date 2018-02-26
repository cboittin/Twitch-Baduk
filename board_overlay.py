import os
from threading import Thread
from collections import deque
import time

import PIL, PIL.ImageDraw, PIL.ImageFont

from util import trace, settings
from go_game import COLOR_BLACK, COLOR_WHITE

class OverlayTimer(Thread):

    def __init__(self, generator):
        super(OverlayTimer, self).__init__()
        self.generator = generator
        self.images = deque([])
        self.running = False

    def addImage(self, image, t):
        self.images.append( (image, t) )
        
    def resetOverlay(self):
        trace("Clearing on-screen variation", 1)
        self.generator.ovBaseImage.save(self.generator.ovImagePath)

    def setOverlay(self, image):
        trace("New on-screen variation", 1)
        image.save(self.generator.ovImagePath)
    
    def nextOverlay(self):
        if len(self.images) == 0:
            self.resetOverlay()
            return
        image, t = self.images.popleft()
        self.setOverlay(image)
        time.sleep(t)
    
    def start(self):
        if not self.running:
            super(OverlayTimer, self).start()
    
    def run(self):
        self.running = True
        while len(self.images) > 0:
            self.nextOverlay()
        self.resetOverlay()
        self.running = False

class VariationOverlayGenerator:
    
    def __init__(self):
        self.ovImagePath = settings["overlay_image_path"]
        self.ovBaseImageSize = (1520, 1520) 
        self.antialias = 4
        
        w = self.ovBaseImageSize[0] * self.antialias
        h = self.ovBaseImageSize[1] * self.antialias
        self.ovTopleft = (int(settings["overlay_padding_left"]), int(settings["overlay_padding_top"]))
        self.ovDimensions = (w - int(settings["overlay_padding_right"]) - self.ovTopleft[0], \
                             h - int(settings["overlay_padding_bottom"]) - self.ovTopleft[1] \
                             )
        fontPath = os.path.join(".", "overlay", "fonts", "steelfis.ttf") # https://fontlibrary.org/en/font/steelfish
        self.ovFont = PIL.ImageFont.truetype(fontPath, size=52 * self.antialias)
        
        # Initialize empty overlay image
        self.ovBaseImage = PIL.Image.new(mode="RGBA", size=self.ovBaseImageSize, color=(0, 0, 0, 0))
        self.ovBaseImage.save(self.ovImagePath)
        
        self.timer = OverlayTimer(self)
        self.baseTimeVariation = int(settings["base_variation_displaying_time"])
        self.timePerStone = int(settings["variation_displaying_time_per_stone"])
        
    def generateOverlay(self, variation, user, colors=False):
        trace("Generating Overlay image for variation %s" % variation, 2)
        drawSize = (self.ovBaseImageSize[0] * self.antialias, self.ovBaseImageSize[1] * self.antialias)
        output = PIL.Image.new(mode="RGBA", size=drawSize, color=(0, 0, 0, 0))
        drawContext = PIL.ImageDraw.Draw(output)
        for i in range(len(variation)):
            move, color = variation[i]
            x, y = move
            
            offset = self.antialias * 3
            
            left = self.ovTopleft[0] + self.ovDimensions[0] * x / 19 + offset
            top = self.ovTopleft[1] + self.ovDimensions[1] * y / 19 + offset
            right = self.ovTopleft[0] + self.ovDimensions[0] * (x + 1) / 19 - offset
            bottom = self.ovTopleft[1] + self.ovDimensions[1] * (y + 1) / 19 - offset
            
            # Draw an outlined circle
            if colors:
                if color == COLOR_BLACK:
                    drawContext.ellipse( (left, top, right, bottom), outline="white", fill="white" )
                    drawContext.ellipse( (left + offset, top + offset, right - offset, bottom - offset), outline="black", fill="black" )
                else:
                    drawContext.ellipse( (left, top, right, bottom), outline="black", fill="black" )
                    drawContext.ellipse( (left + offset, top + offset, right - offset, bottom - offset), outline="white", fill="white" )
            else:
                drawContext.ellipse( (left + offset*6, top + offset*6, right - offset*6, bottom - offset*6), outline="black", fill="black" )
                drawContext.ellipse( (left + offset*7, top  + offset*7, right - offset*7, bottom - offset*7), outline=(205,200,60,0), fill=(205,200,60,0) )
            
            # Draw the move number
            moveNumber = str(i)
            w, h = drawContext.textsize(moveNumber, font=self.ovFont)
            W = right - left
            H = bottom - top
            textX = left + self.antialias + (W - w) / 2
            textY = top - self.antialias + (H - h) / 2
            drawContext.text( (textX - offset, textY - offset), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX + offset, textY - offset), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX - offset, textY + offset), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX + offset, textY + offset), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX - offset, textY), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX + offset, textY), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX, textY - offset), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX, textY + offset), moveNumber, font=self.ovFont, fill="black")
            drawContext.text( (textX, textY), moveNumber, font=self.ovFont, fill="white")
        
        output = output.resize(self.ovBaseImageSize, PIL.Image.LANCZOS)
        # output.save(self.ovImagePath)
        
        t = self.baseTimeVariation + len(variation) * self.timePerStone
        self.timer.addImage(output, t)
        self.timer.start()
    