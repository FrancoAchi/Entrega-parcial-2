from typing import Any
import pygame
from pygame.locals import *
from config import WIDTH, GRAVITY
from sprite_sheet import Sprites
from projectiles import Projectile
from import_path import load_sound


class Player(pygame.sprite.Sprite):
    def __init__(self, groups, sprites: Sprites) -> None:
        """
        Inicializa la clase Player.

        Args:
        - groups: Lista de grupos a los que pertenece el jugador.
        - sprites: Objeto Sprites que contiene las animaciones del jugador.
        """
        super().__init__(groups)
        self.animations = sprites.get_animation_dict()
        self.current_sprite = 0
        self.image = self.animations["idle_right"][self.current_sprite]
        self.rect = self.image.get_rect(topleft=(500, 500))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 3
        self.last_update = pygame.time.get_ticks()
        self.animation_time = 70
        self.speed_v = 0
        self.is_jumping = False
        self.jump_speed = -10
        self.is_second_jump = False
        self.is_jump_key_pressed = False
        self.projectiles = pygame.sprite.Group()
        self.shoot_key_pressed = False
        self.shoot_key2_pressed = False
        self.max_health = 3
        self.current_health = self.max_health

        # Sonidos
        self.jump_sound = pygame.mixer.Sound(load_sound("jump.wav"))
        self.shoot_sound = pygame.mixer.Sound(load_sound("player_shoot.wav"))

    def handle_movement(self, direction: str, animation_key: str) -> None:
        """
        Maneja el movimiento del jugador basado en la dirección y clave de animación.

        Args:
        - direction: Dirección del movimiento ("right" o "left").
        - animation_key: Clave de animación correspondiente a la dirección.
        """
        if direction == "right" and self.rect.right <= WIDTH:
            self.rect.x += self.speed
        elif direction == "left" and self.rect.left >= 0:
            self.rect.x -= self.speed

        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_time:
            self.current_sprite = (self.current_sprite + 1) % len(self.animations[animation_key])
            self.image = self.animations[animation_key][self.current_sprite]
            self.mask = pygame.mask.from_surface(self.image)
            self.last_update = current_time

    def get_inputs(self) -> None:
        """
        Obtiene las entradas del teclado y maneja el movimiento y saltos del jugador.
        """
        keys = pygame.key.get_pressed()
        if keys[K_d]:
            self.handle_movement("right", "right")
        elif keys[K_a]:
            self.handle_movement("left", "left")

        if keys[K_j] and not self.is_jump_key_pressed:
            self.jump()
            self.is_jump_key_pressed = True

        if not keys[K_j]:
            self.is_jump_key_pressed = False
            self.is_jumping = False
            self.is_second_jump = False

        if keys[K_l] and not self.shoot_key_pressed:
            self.shoot_projectile(1)
            self.shoot_key_pressed = True

        if not keys[K_l]:
            self.shoot_key_pressed = False

        if keys[K_k] and not self.shoot_key2_pressed:
            self.shoot_projectile(-1)
            self.shoot_key2_pressed = True

        if not keys[K_k]:
            self.shoot_key2_pressed = False

    def get_gravity(self) -> None:
        """
        Aplica la gravedad al jugador y ajusta la posición vertical.
        """
        self.speed_v += GRAVITY
        self.rect.y += self.speed_v

    def shoot_projectile(self, direction):
        """
        Dispara un proyectil en la dirección especificada.

        Args:
        - direction: Dirección del proyectil (-1 para izquierda, 1 para derecha).
        """
        projectile = Projectile(self.rect.centerx, self.rect.centery, direction)  # Se mueve hacia la derecha
        self.projectiles.add(projectile)
        self.shoot_sound.play()

    def jump(self) -> None:
        """
        Maneja el salto del jugador.
        """
        if not self.is_jumping:
            self.speed_v = self.jump_speed
            self.is_jumping = True
            self.jump_sound.play()

    def second_jump(self) -> None:
        """
        Maneja el segundo salto del jugador.
        """
        if not self.is_second_jump and self.speed_v < 0:
            self.speed_v = self.jump_speed * 0.75  # Ajusta la velocidad del mini salto
            self.is_second_jump = True

    def draw(self, surface):
        """
        Dibuja el jugador en la superficie especificada.

        Args:
        - surface: Superficie en la que se dibujará el jugador.
        """
        pass

    def update(self) -> None:
        """
        Actualiza el jugador en cada fotograma del juego.
        """
        self.get_inputs()
        self.get_gravity()
