import os

import pygame
from pygame.locals import *

from config import CHECK
from utils import load_image

from basemodel import BaseModel


class Unicorn(BaseModel):
    """
    El Unicorn.
    """

    def boundary_check(self):

        if self.rect.x < 0: self.rect.x = 0
        if self.rect.y < 34: self.rect.y = 35
 
        if self.rect.x > CHECK["limite"]: self.rect.x = CHECK["reset"]
        if self.rect.y > CHECK["limite"]: self.rect.y = CHECK["reset"]


    def activate_shield(self, screen):
        shield = pygame.Surface(self.image.get_size())
        shield.fill((102, 255, 102))
        screen.blit(shield, (self.rect.x, self.rect.y))


    def state(self, key, screen):

        self.shield = False
        self.rotate = False

        if key[K_ESCAPE]:
            exit(1)

        if key[K_DOWN]:
            self.rect    = self.rect.move(0, 15)
            print("[*] abajo")

        if key[K_UP]:
            self.rect    = self.rect.move(0, -15)
            print("[*] arriba")

        if key[K_RIGHT]:
            self.image   = load_image("unicorn.png")
            copy_pos     = (self.rect.x, self.rect.y)
            self.rect    = self.image.get_rect()
            self.rect.x, \
            self.rect.y  = copy_pos
            self.rect = self.rect.move(15, 0) 
            print("[*] derecha")

        if key[K_LEFT]:
            self.image   = load_image("left_unicorn.png")
            copy_pos     = (self.rect.x, self.rect.y)
            self.rect    = self.image.get_rect()
            self.rect.x, \
            self.rect.y  = copy_pos
            self.rect    = self.rect.move(-15, 0)
            print("[*] izquierda")

        if key[K_SPACE]:
            self.shield = True
            print("[*] escudo protector activado")

        if key[K_r]:
            self.rotate = True
            print("[*] rotate")
    
        self.boundary_check()


    def update(self, screen):

        if self.rotate:
            self.image = pygame.transform.rotate(self.image, 90)
    
        if self.shield:
            self.activate_shield(screen)

        screen.blit(self.image, self.rect)
        
