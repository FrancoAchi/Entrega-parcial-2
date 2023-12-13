import pygame
from pygame.locals import *
from levels_setup import *
from config import WIDTH, HEIGHT, BLACK
from button import create_button, show_text
from import_path import load_path
from setup_level_boss import LevelBoss
from levels import Level

class MainMenu:
    def __init__(self, screen, font, background, button_play_rect, button_controls_rect, button_exit_rect, button_level1, button_level2, button_level3, button_music_rect, color_primary=(0, 0, 0), color_secondary=(0, 0, 0), border_color= (0, 0 , 0), music_file= None):
        """
        Inicializa el menú principal.

        Args:
        - screen: Superficie de pantalla de Pygame.
        - font: Fuente de texto de Pygame.
        - background: Imagen de fondo.
        - button_play_rect: Rectángulo del botón de juego.
        - button_controls_rect: Rectángulo del botón de controles.
        - button_exit_rect: Rectángulo del botón de salida.
        - button_level1: Rectángulo del botón del nivel 1.
        - button_level2: Rectángulo del botón del nivel 2.
        - button_level3: Rectángulo del botón del nivel 3.
        -button_music_rect: rectangulo del boton de la musica
        - color_primary: Color principal del botón.
        - color_secondary: Color secundario del botón.
        - border_color: Color del borde del botón.
        - music_file: Archivo de música para reproducir en el fondo.
        """
        self.screen = screen
        self.font = font
        self.background = background
        self.button_play_rect = button_play_rect
        self.button_controls_rect = button_controls_rect
        self.button_exit_rect = button_exit_rect
        self.button_level1 = button_level1
        self.button_level2 = button_level2
        self.button_level3 = button_level3
        self.color_primary = color_primary
        self.color_secondary = color_secondary
        self.border_color = border_color
        self.show_controls = False
        self.music_file = music_file
        self.levels_menu_active = False
        self.in_level = False
        self.level_1 = level1_data
        self.level_2 = level2_data
        self.level_3 = level3_data
        self.boss_level = False
        self.button_music_rect = button_music_rect
        self.music_enabled = True

    def setup_music(self):
        """
        Configura la música de fondo si se proporciona un archivo de música.
        """
        try:
            if self.music_file:
                pygame.mixer.music.load(self.music_file)
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Error al cargar la pantalla final: {e}")


    def run(self):
        try:
            pygame.mixer.init()
            self.setup_music()
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                    elif event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            cursor = event.pos
                            if self.button_play_rect.collidepoint(cursor[0], cursor[1]):
                                self.levels_menu_active = True
                            elif self.button_controls_rect.collidepoint(cursor[0], cursor[1]):
                                self.show_controls = not self.show_controls
                            elif self.button_exit_rect.collidepoint(cursor[0], cursor[1]):
                                pygame.quit()
                            elif self.button_music_rect.collidepoint(cursor[0], cursor[1]):
                                self.toggle_music()  # Llama a la función para cambiar el estado de la música
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            if self.levels_menu_active:
                                self.levels_menu_active = False
                                self.in_level = False
                            else:
                                self.show_controls = False

                if self.levels_menu_active:
                    selected_level = self.levels_menu()
                    if selected_level is not None:
                        return self.setup_level(selected_level, self.screen)

                self.draw()
                pygame.display.flip()
                pygame.time.delay(100)

            pygame.mixer.music.stop()
            pygame.display.flip()
            pygame.mixer.quit()
        except Exception as e:
            print(f"Error al cargar la pantalla final: {e}")

    def toggle_music(self):
        """
        Cambia el estado de la música entre activada y desactivada.
        """
        if self.music_enabled:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        self.music_enabled = not self.music_enabled


    def draw(self):
        """
        Dibuja la interfaz del menú principal.
        """
        self.screen.blit(self.background, (0, 0))

        if not self.show_controls:
            if not self.levels_menu_active:
                create_button(self.screen, self.button_play_rect, "Levels", self.color_primary, self.color_secondary, self.border_color)
                create_button(self.screen, self.button_controls_rect, "Controls", self.color_primary, self.color_secondary, self.border_color)
                create_button(self.screen, self.button_exit_rect, "Quit", self.color_primary, self.color_secondary, self.border_color)
                
            else:
                self.draw_levels_menu()
        else:
            controls_image = pygame.transform.scale(load_path("controls.jpg"), (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(controls_image, (0, 0))
            create_button(self.screen, self.button_music_rect, "Music", self.color_primary, self.color_secondary, self.border_color)

        pygame.display.flip()

    def levels_menu(self):
        """
        Muestra el menú de niveles.

        Returns:
        - dict: Datos del nivel seleccionado.
        """
        try:
            level_menu = True
            self.selected_level = None

            while level_menu:
                for e in pygame.event.get():
                    if e.type == QUIT:
                        pygame.quit()
                    elif e.type == MOUSEBUTTONDOWN:
                        if e.button == 1:
                            mouse = e.pos
                            if self.button_level1.collidepoint(mouse[0], mouse[1]):
                                self.selected_level = level1_data
                                level_menu = False
                                self.boss_level = False  # Nivel sin jefe
                            elif self.button_level2.collidepoint(mouse[0], mouse[1]):
                                self.selected_level = level2_data
                                level_menu = False
                                self.boss_level = False  # Nivel sin jefe
                            elif self.button_level3.collidepoint(mouse[0], mouse[1]):
                                self.selected_level = level3_data
                                level_menu = False
                                self.boss_level = True
                    elif e.type == KEYDOWN:
                        if e.key == K_ESCAPE:
                            level_menu = False
                            self.levels_menu_active = False

                if not self.in_level:
                    self.draw_levels_menu()

                pygame.display.flip()
                pygame.time.delay(100)

            return self.selected_level
        except Exception as e:
            print(f"Error al cargar la pantalla final: {e}")


    def draw_levels_menu(self):
        """
        Dibuja la interfaz del menú de niveles.
        """
        create_button(self.screen, self.button_level1, "Level 1", self.color_primary, self.color_secondary, self.border_color)
        create_button(self.screen, self.button_level2, "Level 2", self.color_primary, self.color_secondary, self.border_color)
        create_button(self.screen, self.button_level3, "Level 3", self.color_primary, self.color_secondary, self.border_color)

    def setup_level(self, level, screen):
        """
        Configura el nivel seleccionado.

        Args:
        - level: Datos del nivel seleccionado.
        - screen: Superficie de pantalla de Pygame.

        Returns:
        - LevelBoss o Level: Objeto del nivel configurado.
        """
        if self.boss_level:
            return LevelBoss(level, screen)
        else:
            return Level(level, screen)

def show_final_screen(screen, final_screen, final_screen_rect, font, max_score):
    """
    Muestra la pantalla final del juego.

    Args:
    - screen: Superficie de pantalla de Pygame.
    - final_screen: Imagen de fondo de la pantalla final.
    - final_screen_rect: Rectángulo de la pantalla final.
    - font: Fuente de texto de Pygame.
    - max_score: Puntuación máxima alcanzada.
    """
    try:
        screen.blit(final_screen, final_screen_rect)
        show_text(screen, "GAME OVER", font, (WIDTH // 2, 20), BLACK, color_fondo=None)
        show_text(screen, f"Maximum Score: {max_score}", font, (WIDTH // 2, HEIGHT // 2), BLACK, color_fondo=None)
        show_text(screen, "Press a key to continue", font, (WIDTH // 2, HEIGHT - 30), BLACK, color_fondo=None)

        pygame.display.flip()
    except Exception as e:
        print(f"Error al cargar la pantalla final: {e}")

def wait_user():
    """
    Espera la interacción del usuario, con los eventos de teclado y salida.

    return:
    - None: Si el usuario presiona la tecla "Esc" o  cierra la ventana, finaliza el programa
    """
    while True:

        for e in pygame.event.get():
            if e.type == QUIT:
                end()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    end()

                return 
            
def end():
    """
    Finaliza la aplicación, cerrando la ventana y saliendo del programa
    """
    pygame.quit()
    exit()
