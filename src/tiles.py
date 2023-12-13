import pygame
from pygame.locals import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        """
        Inicializa la clase Platform.

        Args:
        - x: Posición en el eje x de la plataforma.
        - y: Posición en el eje y de la plataforma.
        - width: Ancho de la plataforma.
        - height: Altura de la plataforma.
        """
        super().__init__()
        self.image = pygame.Surface((width, height))  # Crea una superficie verde para representar la plataforma
        self.image.fill((0, 255, 0))  # Rellena la superficie con color verde
        self.rect = self.image.get_rect(topleft=(x, y))  # Obtiene el rectángulo de la superficie y establece su posición inicial
