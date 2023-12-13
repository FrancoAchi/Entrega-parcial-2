import pygame
from sprite_sheet import Sprites
from import_path import load_path
from config import STATIC_WIDTH, STATIC_HEIGHT

class StaticEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, is_facing_left=False, speed=2, all_sprites_group=None):
        """
        Inicializa la clase StaticEnemy.

        Args:
        - x: Posición en el eje x.
        - y: Posición en el eje y.
        - is_facing_left: Indica si el enemigo está mirando hacia la izquierda.
        - speed: Velocidad de movimiento del enemigo.
        - all_sprites_group: Grupo de sprites al que pertenece el enemigo.
        """
        super().__init__()
        # Configuración del sprite y la máscara
        self.animations = self.load_enemy_animations()
        self.current_sprite = 0
        self.direction = -1 if is_facing_left else 1
        self.image = self.animations["walk_left" if is_facing_left else "walk_right"][self.current_sprite]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.all_sprites_group = all_sprites_group

    def load_enemy_animations(self):
        """
        Carga las animaciones del enemigo estático desde un sprite sheet.

        Returns:
        - dict: Diccionario de animaciones del enemigo estático.
        """
        sprite_enemy = Sprites(load_path("enemy2.png"), 4, 2, STATIC_WIDTH, STATIC_HEIGHT, ["walk_right", "walk_left", "death_left", "death_right"])
        return sprite_enemy.get_animation_dict()

    def update(self):
        """
        Actualiza la animación del enemigo estático en cada fotograma del juego.
        """
        animation_key = "walk_left" if self.direction == -1 else "walk_right"
        self.current_sprite = (self.current_sprite + 1) % len(self.animations[animation_key])
        self.image = self.animations[animation_key][self.current_sprite]
        self.mask = pygame.mask.from_surface(self.image)
