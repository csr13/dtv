import os

import pygame
from pygame.locals import *

from config import SCREENRECT
from utils import load_image

from basemodel import BaseModel



class Unicornio(BaseModel):
    """
    El Unicornio.
    """

    def get_position(self, rect):
        self.prev_pos = (self.rect.x, self.rect.y,)


    def draw(self, screen):
        screen.blit(self.img, self.rect)


    def erase(self, screen, background):
        screen.blit(background, self.rect, self.rect)


    def location_check(self, check):
        pass

        
        


    

    
