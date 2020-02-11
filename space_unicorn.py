# csr


import os
import pdb

from PIL import Image
import pygame
from pygame.locals import *


dirty_rect = []


class BaseObject(object):

    def init(self, imagen):
        self.imagen = imagen
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def draw(self, screen):
        t = screen.blit(self.imagen, self.rect)
        dirty_rect.append(t)


    def erase(self, screen, background):
        t = screen.blit(background, self.rect, self.rect)
        dirty_rect.append(t)


class Unicornio(BaseObject):
    
    def __init__(self):
        super().__init__(self)
        pass 


class Bigot(BaseObject):
    
    def __init__(self):
        super().__init__(self)
        pass 


class Explosion(BaseObject):
    
    def __init__(self):
        super().__init__(self)
        pass 



class Laser(BaseObject):
    
    def __init__(self):
        super().__init__(self)
        pass


# -------------------------------------------------------------------------
# Llamada principal
# -------------------------------------------------------------------------

pygame.init()

# -------------------------------------------------------------------------
# Configuraciones 
# -------------------------------------------------------------------------

# Constantes
SCREENRECT = Rect(0, 0, 640, 480)
PUNTAJE    = 0
VIDAS      = 3

# Inits
clock = pygame.time.Clock()
pygame.key.set_repeat(10,100)

# -------------------------------------------------------------------------
# Pantalla
# -------------------------------------------------------------------------

screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("<[*_*]> Space Unicorn -- CSR")
background = pygame.Surface(screen.get_size()).convert()
background.fill((0,0,0))

# -------------------------------------------------------------------------
# Texto
# -------------------------------------------------------------------------

score = pygame.font.SysFont("ubuntumono", 20)
score = score.render(f"Puntos : {PUNTAJE}", 2, (102, 255, 102))
score_position = score.get_rect(top=30, right=110)

vidas = pygame.font.SysFont("ubuntumono", 20)
vidas = vidas.render(f"Vidas: ", 2, (102, 255, 102))
vidas_position = vidas.get_rect(top=30, right=200)

# -------------------------------------------------------------------------
# Fondo de imagen.
# -------------------------------------------------------------------------

background_path = os.path.join(os.getcwd(), "imagenes", "background.gif")
background_tile = pygame.image.load(background_path).convert()
background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, background_tile.get_width()):
    background.blit(background_tile, (x, 0))
background_rect = background.get_rect()

# -------------------------------------------------------------------------
# Imagenes
# -------------------------------------------------------------------------

posicion_init  = (480//2, 480//2)
unicorn_path   = os.path.join(os.getcwd(), "imagenes", "unicorn.png")
unicorn        = pygame.image.load(unicorn_path)
unicorn_rect   = unicorn.get_rect(center=posicion_init)

courage_symbol = os.path.join(os.getcwd(), "imagenes", "heart.png")
courage_meter  = []
padding        = [23, 195] # se incrementa el rango aqui
padding_copy   = padding[:] # copia para reiniciar vidas

# Carga las vidas de el jugador a la pantalla.
for each in range(VIDAS):
    courage_load = pygame.image.load(courage_symbol)
    courage_meter.append(courage_load.get_rect())
    courage_meter[each].x = padding[1]
    courage_meter[each].y = padding[0]
    background.blit(courage_load, courage_meter[each])
    padding[1] += 35


# -------------------------------------------------------------------------
# Loop
# -------------------------------------------------------------------------

while bool(1):

    # -------------------------------------------------------------------------
    # Acciones
    # -------------------------------------------------------------------------

    shield, rotate = (False, False,)

    # -------------------------------------------------------------------------
    # Eventos
    # -------------------------------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit(1)


        pygame.event.pump()
        key = pygame.key.get_pressed()


        if key[K_DOWN]:
            unicorn_rect = unicorn_rect.move(0, 15)
            print("[*] abajo")

        if key[K_UP]:
            unicorn_rect = unicorn_rect.move(0, -15)
            print("[*] arriba")

        if key[K_RIGHT]:
            unicorn_rect = unicorn_rect.move(15, 0)
            print("[*] derecha")

        if key[K_LEFT]:
            unicorn_rect = unicorn_rect.move(-15, 0)
            print("[*] izquierda")

        if key[K_SPACE]:
            shield = True
            print("[*] escudo protector activado")
        
        if key[K_r]:
            rotate = True
            print("[*] rotate")
        
    # -------------------------------------------------------------------------
    # Blits
    # -------------------------------------------------------------------------

    screen.blit(background, (0,0))
    background.blit(score, score_position)
    background.blit(vidas, vidas_position)
    if rotate:
        unicorn = pygame.transform.rotate(unicorn, 90)
    if shield:
        shield = pygame.Surface(unicorn.get_size(), )
        shield.fill((102, 255, 102))
        screen.blit(shield, (unicorn_rect.x, unicorn_rect.y))

    screen.blit(unicorn, unicorn_rect)

    # -------------------------------------------------------------------------
    # Updatear la pantall
    # -------------------------------------------------------------------------

    pygame.display.update()
    clock.tick(30)
