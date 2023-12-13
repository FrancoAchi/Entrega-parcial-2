import os
import pygame

def load_path(nombre_archivo: str, directorio="src/assets")-> pygame.surface:
    """
    Carga una imagen desde un archivo en el directorio especificado.

    Parameters:
    - nombre_archivo (str): El nombre del archivo de imagen.
    - directorio (str): La ruta del directorio donde se encuentra la imagen. Por defecto, es "src/assets".

    Returns:
    pygame.Surface: La superficie de la imagen cargada.
    """
    try:
        ruta = os.path.join(directorio, nombre_archivo)
        imagen = pygame.image.load(ruta)
        return imagen
    except pygame.error as e:
        print(f"No se pudo cargar la imagen apropiadamente: {e}")


def load_sound(nombre_archivo: str, directorio="src/assets") -> pygame.mixer.Sound:
    """
    Carga un sonido desde un archivo en el directorio especificado.

    Parameters:
    - nombre_archivo (str): El nombre del archivo de sonido.
    - directorio (str): La ruta del directorio donde se encuentra el sonido. Por defecto, es "src/assets/sounds".

    Returns:
    pygame.mixer.Sound: El objeto de sonido cargado.
    """
    try:
        ruta = os.path.join(directorio, nombre_archivo)
        sonido = pygame.mixer.Sound(ruta)
        return sonido
    except pygame.error as e:
        print(f"No se pudo cargar el sonido apropiadamente: {e}")


