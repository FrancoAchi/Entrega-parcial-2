import pygame

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, width, height):
        """
        Inicializa la clase Spike.

        Args:
        - x: Posición inicial en el eje x.
        - y: Posición inicial en el eje y.
        - image_path: Ruta de la imagen del spike.
        - width: Ancho del spike.
        - height: Altura del spike.
        """
        super().__init__()
        
        # Carga la imagen del spike y la escala al tamaño especificado
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        
        # Obtiene el rectángulo de la imagen y lo posiciona en (x, y)
        self.rect = self.image.get_rect(topleft=(x, y))
