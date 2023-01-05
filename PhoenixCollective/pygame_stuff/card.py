#--------------------------------------#
# Title: card.py
# Desc: creates a new Card object
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Nov-04, Created File
#   Garrett Bachman, 2022-Nov-04, Added header
#   Garrett Bachman, 2022-Nov-04, Added code
#--------------------------------------#

import os
import pygame as pg
import cost
import main
from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")
print(main_dir)
class Card(pg.sprite.Sprite):
    def __init__(self, name, color, cost):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.name = name
        self.color = color
        self.cost = cost
        self.selected = False
        self.image, self.rect, = main.load_image(self.name + ".jfif", -1)
        
    def update(self):
        if self.selected:
            pos = pg.mouse.get_pos()
            self.rect.center = pos
    
    def select(self):
        if not self.selected:
            self.selected = True
            
""""
    def highlight(self, win):
        tempRect = self.rect.copy().inflate(4, 4)
        if not self.highlight:
            pg.draw.rect(win, pg.Color(255,128,0), tempRect)
        else:
            self.highlight = False

# an arrow that follows your mouse from a selected card
class Arrow(pg.sprite.Sprite):
    def __init__(self, cardRect):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.cardRect = cardRect
        
    def update(self):
        pos = pg.mouse.get_pos()
"""