import pygame
from pygame.locals import *
from player import Player
from tiles import Platform
from sprite_sheet import Sprites
from config import RED, WIDTH_PLAYER, HEIGHT_PLAYER, SIZE_SCREEN
from enemy import Enemy
from import_path import load_path, load_sound
from enemy_static import StaticEnemy
from items import Item, ItemHeart
from spikes import Spike
from levels_setup import levels

class Level:
    def __init__(self, level_data, surface):
        """
        Inicializa la clase Level.

        Args:
        - level_data: Datos del nivel.
        - surface: Superficie en la que se representa el nivel.
        """
        self.font = pygame.font.Font(None, 36)
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.score_value = 0
        self.time_limit = 60
        self.player_lives = 3
        self.clock = pygame.time.Clock()
        self.setup_level(level_data)
        self.death_sound = pygame.mixer.Sound(load_sound("explosion.wav"))
        self.heart_point = pygame.mixer.Sound(load_sound("heart_point.wav"))
        self.item_point = pygame.mixer.Sound(load_sound("item_point.wav"))

        self.screen = pygame.display.set_mode(SIZE_SCREEN)
        self.update_score_surface()
        self.timer = self.font.render(f"Time: {int(self.time_limit)}", True, RED)
        self.rect_timer = self.timer.get_rect(center=(SIZE_SCREEN[0] // 2, 20))
        self.paused = False
        self.health_font = pygame.font.Font(None, 36)
        self.health_position = (10, 10)
        self.current_level = 0
        self.completed = False

    def setup_level(self, level_data):
        """
        Configura el nivel con base en los datos proporcionados.

        Args:
        - level_data: Datos del nivel.
        """
        # Configuración del fondo del nivel
        self.background_image = pygame.image.load(level_data['background']).convert()
        self.background_rect = self.background_image.get_rect()

        # Configuración de las plataformas
        self.platforms = pygame.sprite.Group()
        for platform_info in level_data['platforms']:
            x, y, width, height = platform_info
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)

        # Configuración del jugador
        self.all_sprites = pygame.sprite.Group()
        sprite_player = Sprites(load_path("skeletor.png"), 8, 4, WIDTH_PLAYER, HEIGHT_PLAYER, ["idle_right", "idle_left", "right", "left", "attack_right", "attack_left", "death_right", "death_left"])
        self.player = Player([self.all_sprites], sprite_player)

        # Configuración de los enemigos
        self.enemies = pygame.sprite.Group()
        for enemy_info in level_data.get('enemies', []):
            x, y, move_speed, move_range = enemy_info
            enemy = Enemy(x, y, move_speed, move_range)
            self.enemies.add(enemy)

        self.static_enemies = pygame.sprite.Group()
        for static_enemy_info in level_data.get('static_enemies', []):
            x, y, is_facing_left, speed = static_enemy_info
            static_enemy = StaticEnemy(x, y, is_facing_left, speed, all_sprites_group=self.all_sprites)
            self.static_enemies.add(static_enemy)

        # Configuración de los items
        self.items = pygame.sprite.Group()
        for item_info in level_data.get('items', []):
            x, y, image_path, width, height = item_info
            item = Item(x, y, image_path, width, height)
            self.items.add(item)

        # Configuración de los items curativos
        self.healing_items = pygame.sprite.Group()
        for healing_item_info in level_data.get('healing_items', []):
            x, y, image_path, width, height = healing_item_info
            healing_item = ItemHeart(x, y, image_path, width, height)
            self.healing_items.add(healing_item)

        # Configuración de las trampas
        self.spikes = pygame.sprite.Group()
        for spike_info in level_data.get('spikes', []):
            x, y, image_path, width, height = spike_info
            spike = Spike(x, y, image_path, width, height)
            self.spikes.add(spike)

    def draw_health_bar(self, surface):
        """
        Dibuja la barra de salud del jugador en la pantalla.

        Args:
        - surface: Superficie en la que se dibuja la barra de salud.
        """
        health_text = self.health_font.render(f"Health: {self.player.current_health}", True, RED)
        surface.blit(health_text, self.health_position)

    def handle_time_limit(self):
        """
        Maneja la reducción del tiempo límite del nivel.
        """
        # Reduzca el tiempo restante según el tiempo transcurrido desde el último fotograma
        self.time_limit -= self.clock.get_time() / 1000

        self.timer = self.font.render(f"Time: {int(self.time_limit)}", True, RED)
        self.rect_timer = self.timer.get_rect(center=(SIZE_SCREEN[0] // 2, 15))

        if self.time_limit <= 0:
            self.game_over()

    def handle_player_lives(self):
        """
        Maneja la pérdida de vidas del jugador y finaliza el juego si no hay más vidas.
        """
        if self.player_lives <= 0:
            self.game_over()

    def game_over(self):
        """
        Finaliza el juego.
        """
        print("Game Over")
        pygame.quit()
        exit()

    def level_complete(self):
        """
        Maneja la finalización del nivel.
        """
        print("Level Complete!")
        self.completed = True

    def handle_healing_item_collisions(self):
        """
        Maneja las colisiones entre el jugador y los ítems curativos.
        """
        healing_item_collisions = pygame.sprite.spritecollide(self.player, self.healing_items, True)
        for _ in healing_item_collisions:
            self.player.current_health += 1
            self.heart_point.play()
            if self.player.current_health > self.player.max_health:
                self.player.current_health = self.player.max_health
            self.update_health_surface()

    def horizontal_movement_collision(self):
        """
        Maneja las colisiones horizontales del jugador con las plataformas.
        """
        collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in collisions:
            if self.player.rect.bottom >= platform.rect.top and self.player.speed_v > 0:
                self.player.rect.bottom = platform.rect.top
                self.player.speed_v = 0

    def bottom_top_collision(self):
        """
        Maneja las colisiones entre el jugador y las plataformas para evitar caídas.
        """
        collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
        for platform in collisions:
            if self.player.rect.bottom >= platform.rect.top and self.player.speed_v > 0:
                self.player.rect.bottom = platform.rect.top
                self.player.is_jumping = False
                if self.player.is_jumping:
                    pass
                else:
                    self.player.speed_v = 0

    def handle_enemy_projectile_collisions(self):
        """
        Maneja las colisiones entre los proyectiles del jugador y los enemigos.
        """
        for enemy in self.enemies:
            collisions = pygame.sprite.spritecollide(enemy, self.player.projectiles, True)
            for _ in collisions:
                self.death_sound.play()
                self.score_value += 20
                self.update_score_surface()
                enemy.kill()

        static_enemy_collisions = pygame.sprite.spritecollide(self.player, self.static_enemies, True)
        for static_enemy in static_enemy_collisions:
            self.death_sound.play()
            static_enemy.kill()
            self.score_value += 30
            self.update_score_surface()

    def handle_enemy_collisions(self):
        """
        Maneja las colisiones entre el jugador y los enemigos.
        """
        enemy_collisions = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in enemy_collisions:
            self.death_sound.play()
            self.player.current_health -= 1
            if self.player.current_health <= 0:
                self.player.current_health = 0
                self.game_over()
            self.update_health_surface()

    def handle_spike_collisions(self):
        """
        Maneja las colisiones entre el jugador y las trampas (púas).
        """
        spike_collisions = pygame.sprite.spritecollide(self.player, self.spikes, False)
        for _ in spike_collisions:
            self.player.current_health -= 1  # Reducir la salud del jugador en 1 punto
            if self.player.current_health <= 0:
                self.player.current_health = 0
            self.update_health_surface()

    def update_items(self):
        """
        Actualiza los ítems en el nivel.
        """
        self.items.update()

    def draw_items(self):
        """
        Dibuja los ítems en la pantalla.
        """
        self.items.draw(self.display_surface)
        self.healing_items.draw(self.display_surface)

    def update_health_surface(self):
        """
        Actualiza la superficie de la barra de salud.
        """
        self.health_text = self.health_font.render(f"Health: {self.player.current_health}", True, RED)
        self.rect_health = self.health_text.get_rect(topleft=self.health_position)

        if self.player.current_health <= 0:
            self.game_over()

    def handle_item_collisions(self):
        """
        Maneja las colisiones entre el jugador y los ítems.
        """
        collisions = pygame.sprite.spritecollide(self.player, self.items, True)

        for item in collisions:
            self.score_value += 10
            self.item_point.play()
            self.update_score_surface()

    def update_score_surface(self):
        """
        Actualiza la superficie de la puntuación.
        """
        self.score = self.font.render(f"Score: {self.score_value}", True, RED)
        self.rect_score = self.score.get_rect(topleft=(650, 5))

    def draw_spikes(self):
        """
        Dibuja las trampas (púas) en la pantalla.
        """
        self.spikes.draw(self.display_surface)

    def run(self):
        """
        Ejecuta el bucle principal del nivel.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    self.paused = True

        if not self.paused:
            self.handle_time_limit()
            self.handle_player_lives()
            self.horizontal_movement_collision()
            self.bottom_top_collision()
            self.enemies.update()
            self.static_enemies.update()
            self.handle_item_collisions()
            self.update_items()
            self.handle_enemy_collisions()
            self.handle_healing_item_collisions()
            self.handle_spike_collisions()

            self.player.update()
            self.player.projectiles.update()

            # Dibujar el fondo
            self.platforms.draw(self.display_surface)
            self.display_surface.blit(self.background_image, (0, 0))

            # Dibujar las plataformas y el jugador
            self.player.projectiles.draw(self.display_surface)
            self.enemies.draw(self.display_surface)
            self.static_enemies.draw(self.display_surface)
            self.player.draw(self.display_surface)
            self.draw_spikes()

            self.draw_items()

            self.all_sprites.draw(self.display_surface)
            self.handle_enemy_projectile_collisions()
            if len(self.enemies) == 0 and len(self.static_enemies) == 0:
                self.level_complete()

        self.screen.blit(self.score, self.rect_score)
        self.screen.blit(self.timer, self.rect_timer)
        self.draw_health_bar(self.screen)
        self.clock.tick(60)  # Ajusta según sea necesario
