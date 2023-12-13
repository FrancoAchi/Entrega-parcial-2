import pygame
from pygame.locals import *
from config import *

class Sprites:
    def __init__(self, image, rows, columns, width, height, keys=None) -> None:
        """
        Inicializa la clase Sprites.

        Args:
        - image: Superficie de la imagen de sprites.
        - rows: Número de filas en la hoja de sprites.
        - columns: Número de columnas en la hoja de sprites.
        - width: Ancho individual de cada sprite.
        - height: Altura individual de cada sprite.
        - keys: Lista de claves para las animaciones, en el orden de las filas.
        """
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rows = rows
        self.columns = columns
        self.width_player = width
        self.height_player = height
        self.keys = keys
    
    def get_animation_dict(self, scale=1):
        """
        Obtiene un diccionario de animaciones a partir de la hoja de sprites.

        Args:
        - scale: Factor de escala para ajustar el tamaño de los sprites.

        Returns:
        - animation_dir: Diccionario que mapea claves a listas de superficies de animación.
        """
        self.width = scale * self.width
        self.height = scale * self.height
        self.width_player = scale * self.width_player
        self.height_player = scale * self.height_player
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        column_counter = 0
        animation_dir = {}

        for row in range(self.rows):
            animation_row = []

            for _ in range(self.columns):
                animation_row.append(self.image.subsurface((column_counter * self.width_player, row * self.height_player, self.width_player, self.height_player)))
                column_counter += 1

            animation_dir[self.keys[row]] = animation_row
            column_counter = 0

        return animation_dir
