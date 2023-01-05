#--------------------------------------#
# Title: cost.py
# Desc: object for holding cards' costs
# Change Log: (Who, When, What)
#   Garrett Bachman, 2022-Nov-04, Created File
#   Garrett Bachman, 2022-Nov-04, Added header
#   Garrett Bachman, 2022-Nov-04, Added code
#--------------------------------------#
import os, pygame as pg, collections
class Cost:
    # input 3ww would output a list of 3 colorless and 2 white mana
    def __init__ (self, c, w, u, b, r, g):
        #colorless mana
        self.c = c
        
        # white mana
        self.w = w
        
        # blue mana
        self.u = u
        
        # black mana
        self.b = b
        
        # red mana
        self.r = r
        
        # green mana
        self.g = g
    #def decrypt(self):
        