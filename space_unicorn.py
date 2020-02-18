# csr

import os
import pdb

from PIL import Image
import pygame
from pygame.locals import *

from config import images_path
from utils import Img


# Constantes ==================================================================


SCREENRECT = Rect(0, 0, 640, 480)
PUNTAJE    = 0
VIDAS      = 3


# Funciones de ayuda ==========================================================


def load_image(file, transparent=None):
    """
    Cargador de imagenes.
    """

    file = os.path.join(images_path, file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface


def writer(phrase=None, font=None, size=None, color=None, where=None):
    """
    Esta funcion necesita algo de trabajo, pero funciona, y su uso es
    sencillo, crea un SysFont objeto y regresa un tuple para blitearlo
    a la pantalla.
    """

    if phrase and font and size and color and where:
        to_write = pygame.font.SysFont(font, size)
        to_write = to_write.render(phrase, 2, color)
        position = to_write.get_rect(**where)
        return to_write, position


pygame.init()


# Inits =======================================================================


clock = pygame.time.Clock()
pygame.key.set_repeat(10,100)


# Pantalla ====================================================================


screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("<[*_*]> Space Unicorn")


# Texto =======================================================================


score, score_position = writer(
    phrase=f"Puntos: {PUNTAJE}",
    font="ubuntumono",
    size=20,
    color=(102, 255, 102),
    where={"top" : 30, "right" : 110}
)
vidas, vidas_position = writer(
    phrase=f"Vidas: ",
    font="ubuntumono",
    size=20,
    color=(102,255,102),
    where={"top" : 30, "right" : 200}
)


# Background ==================================================================

Img.background = load_image("background.gif")

background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()


# Carga las vidas de el jugador a la pantalla. ================================


Img.heart      = load_image("heart.png")
courage_meter  = []
padding        = [23, 195]
padding_copy   = padding[:] 

for each in range(VIDAS):
    courage_load = Img.heart
    courage_meter.append(courage_load.get_rect())
    courage_meter[each].x = padding[1]
    courage_meter[each].y = padding[0]
    background.blit(courage_load, courage_meter[each])
    padding[1] += 35


# Imagenes ====================================================================


posicion_init  = (480//2, 480//2)
Img.unicorn    = load_image("unicorn.png")
unicorn_rect   = Img.unicorn.get_rect(center=posicion_init)


# Loop ========================================================================

while bool(1):

    # Acciones ================================================================

    shield, rotate = (False, False,)

    # Eventos =================================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit(1)

        pygame.event.pump()
        key = pygame.key.get_pressed()

        # Para que no se salga de la pantalla el unicornio ====================

        # Reglas para que no se valla para abrriba o para la izquierda 
        if unicorn_rect.x < 0: unicorn_rect.x = 0
        if unicorn_rect.y < 0 : unicorn_rect.y = 0

        # Reglas para que no se valla para abajo o para la derecha 
        if unicorn_rect.x > (480-40): unicorn_rect.x = 473-40
        if unicorn_rect.y > (480-40): unicorn_rect.y = (473-40)
        
        
        # Teclados ============================================================

        if key[K_DOWN]:
            unicorn_rect = unicorn_rect.move(0, 15)
            print("[*] abajo")

        if key[K_UP]:
            unicorn_rect = unicorn_rect.move(0, -15)
            print("[*] arriba")

        if key[K_RIGHT]:
            Img.unicorn  = load_image("unicorn.png")
            copy_pos     = (unicorn_rect.x, unicorn_rect.y)
            unicorn_rect = Img.unicorn.get_rect()
            unicorn_rect.x, unicorn_rect.y = copy_pos
            unicorn_rect = unicorn_rect.move(15, 0)
            print("[*] derecha")

        if key[K_LEFT]:
            Img.unicorn  = load_image("left_unicorn.png")
            copy_pos     = (unicorn_rect.x, unicorn_rect.y)
            unicorn_rect = Img.unicorn.get_rect()
            unicorn_rect.x, unicorn_rect.y = copy_pos
            unicorn_rect = unicorn_rect.move(-15, 0)
            print("[*] izquierda")

        if key[K_SPACE]:
            shield = True
            print("[*] escudo protector activado")
        
        if key[K_r]:
            rotate = True
            print("[*] rotate")
        

   
    # Blits ===================================================================
    

    screen.blit(background, (0,0))
    background.blit(score, score_position)
    background.blit(vidas, vidas_position)


    if rotate:
        Img.unicorn = pygame.transform.rotate(Img.unicorn, 90)
    
    if shield:
        shield = pygame.Surface(Img.unicorn.get_size())
        shield.fill((102, 255, 102))
        screen.blit(shield, (unicorn_rect.x, unicorn_rect.y))

    # blitea el unicornio ya que este activado
    screen.blit(Img.unicorn, unicorn_rect)

    # Updatear la pantalla ====================================================

    pygame.display.update()
    clock.tick(30)
