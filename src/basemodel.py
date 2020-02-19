from utils import load_image



class BaseModel(object):

    def __init__(self, img, spawn_location=None):
        self.image    = load_image(img)
        self.rect     = self.image.get_rect()

    def update(self): pass
