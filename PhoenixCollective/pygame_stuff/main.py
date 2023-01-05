#--------------------------------------#
# Title: main.py
# Desc: compiles game objects into a working UI
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Nov-28, Created File
#   Garrett Bachman, 2022-Nov-28, Added header
#   Garrett Bachman, 2022-Dec-7, Added pygame basic logic
#--------------------------------------#

import os
import pygame as pg
import card
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
asset_dir = os.path.join(main_dir, "assets")

# loads game sounds
def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(asset_dir, "sound", name)
    sound = pg.mixer.Sound(fullname)

    return sound

# loads images, changes scale and removes background
def load_image(name, colorkey = None, scale = 1):
    fullname = os.path.join(asset_dir, name)
    print(fullname)
    image = pg.image.load(fullname)
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


class Main:
    # functions
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1600, 900
        self._background = None
        self._clock = None
        
    def on_init(self):
        pg.init()
        self._display_surf = pg.display.set_mode(self.size, SCALED | RESIZABLE)
        self._background = load_image("image\\background.jpeg")[0]
        self._clock = pg.time.Clock()
        pg.display.set_caption("Phoenix Collective")
        forest = card.Card("cards\\forest", "g", 0)
        self._allsprites = pg.sprite.RenderPlain((forest))
 
    def on_event(self, event):
        # exits main loop if close button is pressed
        if event.type == QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            pass
            
        # resizes background if the window is resized
        elif event.type == VIDEORESIZE:
            self._display_surf = pg.display.set_mode(event.dict['size'], SCALED | RESIZABLE)
            self._display_surf.blit(pg.transform.scale(self._background, event.dict['size']), (0, 0))
            pg.display.flip()
            
    def on_loop(self):
        self._display_surf.blit(self._background, (0, 0))
    
    def on_render(self):
        pg.display.flip() 
        self._clock.tick(30)
    
    def on_cleanup(self):
        pg.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            # handles event queue
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

# runs main method when compiled
if __name__ == "__main__":
    theMain = Main()
    theMain.on_execute()