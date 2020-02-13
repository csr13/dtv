# csr


import os
import pdb

from PIL import Image
import pygame
from pygame.locals import *


class Img:
    pass


def load_image(file, transparent=None):
    """
    Loads an image, prepares it for play.
    """
    file = os.path.join(os.getcwd(), "imagenes", file)
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
    Writes a phrase given all the parameters.
    """
    if phrase and font and size and color and where:
        to_write = pygame.font.SysFont(font, size)
        to_write = to_write.render(phrase, 2, color)
        position = to_write.get_rect(**where)
        return to_write, position

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


# -------------------------------------------------------------------------
# Texto
# -------------------------------------------------------------------------

score, score_position = writer(
    phrase=f"Puntos: {PUNTAJE}",
    font="ubuntumono",
    size=20,
    color=(102, 255, 102),
    where={"top" : 30, "right" : 110}
)

vidas = pygame.font.SysFont("ubuntumono", 20)
vidas = vidas.render(f"Vidas: ", 2, (102, 255, 102))
vidas_position = vidas.get_rect(top=30, right=200)

# -------------------------------------------------------------------------
# Imagenes
# -------------------------------------------------------------------------


background = pygame.Surface(SCREENRECT.size)
for x in range(0, SCREENRECT.width, Img.background.get_width()):
    background.blit(Img.background, (x, 0))
background_rect = background.get_rect()

# -------------------------------------------------------------------------
# Imagenes
# -------------------------------------------------------------------------

posicion_init  = (480//2, 480//2)
Img.unicorn    = load_image("unicorn.png")
unicorn_rect   = Img.unicorn.get_rect(center=posicion_init)

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
        unicorn = pygame.transform.rotate(Img.unicorn, 90)
    if shield:
        shield = pygame.Surface(Img.unicorn.get_size(), )
        shield.fill((102, 255, 102))
        screen.blit(shield, (unicorn_rect.x, unicorn_rect.y))

    screen.blit(Img.unicorn, unicorn_rect)

    # -------------------------------------------------------------------------
    # Updatear la pantall
    # -------------------------------------------------------------------------

    pygame.display.update()
    clock.tick(30)
