import pygame
from levels import Level
from tiles import Platform
from sprite_sheet import Sprites
from player import Player
from config import HEIGHT, WIDTH, WIDTH_PLAYER, HEIGHT_PLAYER, SIZE_SCREEN, RED
from import_path import load_path, load_sound
from boss import Boss
import random

class SkyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, fall_speed):
        """
        Inicializa la clase SkyProjectile.

        Args:
        - x: Posición en el eje x del proyectil.
        - y: Posición en el eje y del proyectil.
        - fall_speed: Velocidad de caída del proyectil.
        """
        super().__init__()
        self.image = load_path("fire.png")  # Carga la imagen del proyectil
        self.image = pygame.transform.scale(self.image, (20, 20))  # Ajusta el tamaño del proyectil según sea necesario
        self.rect = self.image.get_rect(topleft=(x, y))  # Obtiene el rectángulo del proyectil y establece su posición inicial
        self.fall_speed = fall_speed
        self.initial_y = y  # Almacena la posición y inicial
        

    def update(self):
        """
        Actualiza la posición del proyectil en cada fotograma.
        """
        self.rect.y += self.fall_speed

        # Si el proyectil del cielo llega a la parte inferior, reinicia su posición
        if self.rect.top > HEIGHT:
            self.rect.y = self.initial_y
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

class LevelBoss(Level):
    def __init__(self, level_data, surface):
        """
        Inicializa la clase LevelBoss, que representa un nivel con un jefe.

        Args:
        - level_data: Datos del nivel.
        - surface: Superficie en la que se representa el nivel.
        """
        super().__init__(level_data, surface)
        self.timer = self.font.render(f"Time: {int(self.time_limit)}", True, RED)
        self.rect_timer = self.timer.get_rect(center=(SIZE_SCREEN[0] // 2, 20))
        self.clock = pygame.time.Clock()
        self.death_sound = pygame.mixer.Sound(load_sound("explosion.wav"))

        self.boss_health = 20

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

        boss_data = level_data.get('boss', None)
        if boss_data:
            boss_x, boss_y = boss_data
            self.boss = Boss(boss_x, boss_y,)
            self.all_sprites.add(self.boss)

        self.sky_projectiles = pygame.sprite.Group()  # Grupo para proyectiles del cielo

        # Generar proyectiles del cielo
        for _ in range(15):  # Ajusta la cantidad de proyectiles según sea necesario
            x = random.randint(0, WIDTH)
            y = random.randint(-200, -50)
            fall_speed = random.randint(3, 5)  # Ajusta la velocidad según sea necesario
            sky_projectile = SkyProjectile(x, y, fall_speed)
            self.sky_projectiles.add(sky_projectile)
            self.all_sprites.add(sky_projectile)

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

    def defeat_boss(self):
        """
        Maneja la derrota del jefe, eliminándolo y finalizando el juego.
        """
        self.boss.kill()  # Elimina al jefe cuando es derrotado
        self.score_value += 1000  # Suma 1000 puntos cuando el jefe muere
        self.update_score_surface()  # Actualiza la superficie de puntos
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

    def update_score_surface(self):
        """
        Actualiza la superficie que muestra la puntuación en la pantalla.
        """
        self.score = self.font.render(f"Score: {self.score_value}", True, RED)
        self.rect_score = self.score.get_rect(topleft=(650, 5))

    def handle_enemy_projectile_collisions(self):
        """
        Maneja las colisiones entre los proyectiles enemigos y el jugador o el jefe.
        """
        boss_collisions = pygame.sprite.spritecollide(self.boss, self.player.projectiles, True)
        for _ in boss_collisions:
            self.death_sound.play()
            self.boss_health -= 1
            if self.boss_health <= 0:
                self.boss.kill()

        player_collisions = pygame.sprite.spritecollide(self.player, self.sky_projectiles, True)
        for _ in player_collisions:
            self.death_sound.play()
            self.player.current_health -= 1
            if self.player.current_health <= 0:
                self.player.current_health = 0
                self.game_over()

    def run(self):
        """
        Ejecuta el bucle principal del nivel.
        """
        self.clock.tick(60)
        self.player.update()
        self.horizontal_movement_collision()
        self.bottom_top_collision()
        self.sky_projectiles.update()
        self.boss.update()
        self.handle_time_limit()
        self.player.update()
        self.player.projectiles.update()

        # Dibujar el fondo
        self.platforms.draw(self.display_surface)
        self.display_surface.blit(self.background_image, (0, 0))

        # Dibujar las plataformas y el jugador
        self.player.projectiles.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.all_sprites.draw(self.display_surface)
        self.screen.blit(self.score, self.rect_score)
        self.screen.blit(self.timer, self.rect_timer)
        self.draw_health_bar(self.screen)
        self.handle_enemy_projectile_collisions()
        if self.boss_health <= 0:
            self.defeat_boss()
