import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width, height):
        """
        Inicializa la clase Item.

        Args:
        - x: Posición en el eje x.
        - y: Posición en el eje y.
        - image_path: Ruta de la imagen del ítem.
        - width: Ancho del ítem.
        - height: Altura del ítem.
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

class ItemHeart(Item):
    def __init__(self, x, y, image_path, width, height):
        """
        Inicializa la clase ItemHeart, que hereda de la clase Item.

        Args:
        - x: Posición en el eje x.
        - y: Posición en el eje y.
        - image_path: Ruta de la imagen del ítem.
        - width: Ancho del ítem.
        - height: Altura del ítem.
        """
        super().__init__(x, y, image_path, width, height)
