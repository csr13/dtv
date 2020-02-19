import os


from pygame import Rect


# Constantes ==================================================================


SCREENRECT = Rect(0, 0, 640, 480)
PUNTAJE    = 0
VIDAS      = 3


# Utilidades ===================================================================


images_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "imagenes"
)

