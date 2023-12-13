import pygame
from sprite_sheet import Sprites
from config import WIDTH_ENEMY, HEIGHT_ENEMY
from import_path import load_path

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, move_speed, move_range):
        """
        Inicializa la clase Enemy.

        Args:
        - x: Posición en el eje x.
        - y: Posición en el eje y.
        - move_speed: Velocidad de movimiento del enemigo.
        - move_range: Rango de movimiento del enemigo (tupla con límites izquierdo y derecho).
        """
        super().__init__()
        # Configuración del sprite y la máscara
        self.animations = self.load_enemy_animations()
        self.current_sprite = 0
        self.image = self.animations["walk_left"][self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.move_speed = move_speed
        self.move_range = move_range
        self.direction = 1  

    def load_enemy_animations(self):
        """
        Carga las animaciones del enemigo desde un sprite sheet.

        Returns:
        - dict: Diccionario de animaciones del enemigo.
        """
        sprite_enemy = Sprites(load_path("enemy1.png").convert_alpha(), 5, 4, WIDTH_ENEMY, HEIGHT_ENEMY, ["walk_left", "walk_right", "hit_left", "hit_right", "death_right", "death_left"])
        return sprite_enemy.get_animation_dict()

    def update(self):
        """
        Actualiza la posición y animación del enemigo en cada fotograma del juego.
        """
        animation_key = "walk_right" if self.direction == 1 else "walk_left"
        self.current_sprite = (self.current_sprite + 1) % len(self.animations[animation_key])
        self.image = self.animations[animation_key][self.current_sprite]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x += self.direction * self.move_speed

        # Invierte la dirección si el enemigo alcanza los límites del rango
        if self.rect.right >= self.move_range[1] or self.rect.left <= self.move_range[0]:
            self.direction *= -1
