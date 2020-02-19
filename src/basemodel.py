import os

import pygame
from pygame.locals import *

from utils import load_image



class BaseModel(object):


    def __init__(self, image, spawn_location=None):
        self.image    = load_image(image)
        self.rect     = self.image.get_rect()
        if spawn_location:
            self.rect.x , self.rect.y = spawn_location
        

    @property 
    def position(self):
        return self.rect.x, self.rect.y


    @position.setter
    def position(self, xy):
        x = xy[0]
        y = xy[1]
        self.rect.x = x
        self.rect.y = y


    @position.deleter
    def position(self):
        self.rect.x = 0
        self.rect.y = 0
    

    def move(self, xy):
        x = xy[0]
        y = xy[1]
        self.rect.move(x, y)
        self.position = (x, y)
        


    def update(self, screen):
        """
        Dale override a este metodo para darle mas funcionalidad,
        por ahora es basica, blitea una image con su rect a una
        pantalla, unico parametro que recibe esta funcion
        """
        screen.blit(self.image, self.rect)
