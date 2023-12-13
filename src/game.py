import pygame
from pygame.locals import * 
from config import WIDTH, HEIGHT, FPS, button_height, button_width, SIZE_SCREEN, GREY, PURPLE, BLACK, CENTER_SCREEN
from levels_setup import *
from import_path import load_path
from menu_levels import MainMenu, show_final_screen, wait_user
from levels import Level
from setup_level_boss import LevelBoss
from bdd import create_database, insert_player 
from button import show_text

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.icon = pygame.display.set_icon(load_path("logo.png"))
        self.background = pygame.transform.scale(load_path("menu.jpg"), SIZE_SCREEN)
        self.font = pygame.font.Font(None, 36)
        self.center_x = self.screen.get_width() // 2
        self.play_button = pygame.Rect(10, 545, 200, 50)
        self.controls_button = pygame.Rect(300, 545, 200, 50)
        self.exit_button = pygame.Rect(590, 545, 200, 50)
        self.music_menu = "./src/assets/menu_song.mp3"
        self.button_level1 = pygame.Rect(self.center_x - button_width // 2, 150, button_width, button_height)
        self.button_level2 = pygame.Rect(self.center_x - button_width // 2, 250, button_width, button_height)
        self.button_level3 = pygame.Rect(self.center_x - button_width // 2, 350, button_width, button_height)
        self.button_music = pygame.Rect(self.center_x - button_width // 2, 350, button_width, button_height)
        self.levels = [level1_data, level2_data, level3_data]
        self.current_level_index = 0
        self.setup_level(self.levels[self.current_level_index], self.screen)
        self.acumulated_score = 0
        self.max_score = 0
        self.current_score = 0 
        self.final_screen = load_path("final_screen.jpg")
        self.final_screen = pygame.transform.scale(self.final_screen, (WIDTH, HEIGHT))
        self.final_screen_rect = self.final_screen.get_rect()
        self.paused = False

        create_database() 

        self.menu = MainMenu(
            self.screen, self.font, self.background, self.play_button, self.controls_button, 
            self.exit_button, self.button_level1, self.button_level2, self.button_level3, self.button_music, 
            GREY, PURPLE, BLACK, self.music_menu
        )

    def run(self):
        while True:
            self.menu.run()
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    elif event.type == KEYDOWN:
                        if event.key == K_p: 
                            show_text(self.screen, "PAUSE", self.font, CENTER_SCREEN, BLACK, backgorund_color=None)
                            pygame.display.flip()
                            wait_user()
                            
                self.level.run()

                if self.level.completed:
                    # Acumula el puntaje del nivel actual
                    self.acumulated_score += self.current_score
                    self.switch_to_next_level()

                pygame.display.flip()
                self.clock.tick(FPS)

            if self.acumulated_score > self.max_score:
                self.max_score = self.acumulated_score

            player_name = "player"
            insert_player(player_name, self.acumulated_score)

            show_final_screen(self.screen, self.final_screen, self.final_screen_rect, self.font, self.max_score)
            pygame.quit()

    


    def switch_to_next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.setup_level(self.levels[self.current_level_index], self.screen)
        else:
            print("¡Has completado todos los niveles!")
            pygame.quit()
            exit()

    def setup_level(self, level, screen):
        if 'boss' in level:
            self.level = LevelBoss(level, screen)
        else:
            self.level = Level(level, screen)
    

if __name__ == "__main__":
    game = Game()
    game.run()
