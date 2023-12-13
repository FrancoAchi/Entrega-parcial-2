import pygame
from sprite_sheet import Sprites
from config import WIDTH_PROJECTILE, HEIGHT_PROJECTILE


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        """
        Inicializa la clase Projectile.

        Args:
        - x: Posición inicial en el eje x.
        - y: Posición inicial en el eje y.
        - direction: Dirección del proyectil (-1 para izquierda, 1 para derecha).
        """
        super().__init__()

        self.animations = self.load_projectile_animations()
        self.current_sprite = 0
        self.image = self.animations["default"][self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 8
        self.direction = direction

    def load_projectile_animations(self):
        """
        Carga las animaciones del proyectil desde una hoja de sprites.

        Returns:
        - Diccionario de animaciones del proyectil.
        """
        sprite_projectile = Sprites(pygame.image.load("./src/assets/projectile.png").convert_alpha(), 1, 1, WIDTH_PROJECTILE, HEIGHT_PROJECTILE, ["default"])
        return sprite_projectile.get_animation_dict()

    def update(self):
        """
        Actualiza el proyectil en cada fotograma del juego.
        """
        self.current_sprite = (self.current_sprite + 1) % len(self.animations["default"])
        self.image = self.animations["default"][self.current_sprite]
        self.mask = pygame.mask.from_surface(self.image)

        # Invertir la imagen si el proyectil se mueve hacia la izquierda
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect.x += self.direction * self.speed
