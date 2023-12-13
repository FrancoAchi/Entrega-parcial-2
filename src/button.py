import pygame



def create_button(screen: pygame.surface, rect: pygame.Rect, text: str, normal_color: tuple, second_color: tuple, border_color: tuple) -> None:
    """
    Crea un botón y lo muestra en la pantalla.

    Args:
    - screen (pygame.surface): Superficie de Pygame donde se mostrará el botón.
    - rect (pygame.Rect): Rectángulo que define la posición y el tamaño del botón.
    - text (str): Texto que se mostrará en el botón.
    - normal_color (tuple): Color del botón cuando no está resaltado.
    - second_color (tuple): Color del botón cuando está resaltado.

    Return:
    - None
    """
    try:
        # Obtener la posición del mouse
        pos_mouse = pygame.mouse.get_pos()

        # Verificar si el mouse está sobre el botón y ajustar el color en consecuencia
        if rect.collidepoint(pos_mouse):
            pygame.draw.rect(screen, second_color, rect)
            pygame.draw.rect(screen, border_color, rect, 3)
        else:
            pygame.draw.rect(screen, normal_color, rect)

        # Mostrar el texto en el centro del botón
        show_text_button(screen, text, rect.centerx, rect.centery)
    except Exception as e:
        print(f"Error al crear y mostrar el botón: {e}")


def show_text_button(surface,  text, x, y, font_size = 36, color = (0, 0, 0)):
    """
    Muestra texto en una superficie en la posición especificada.

    Args:
    - surface: Superficie de Pygame donde se mostrará el texto.
    - text: Texto que se mostrará en el botón.
    - x, y: Coordenadas (x, y) donde se posicionará el centro del texto.
    - font_size: Tamaño de la fuente del texto (por defecto, 36).
    - color: Color del texto (por defecto, negro).

    Returns:
    - None
    """
    font = pygame.font.SysFont("Arial Black", font_size)
    render = font.render(text, True, color)
    rect_text = render.get_rect(center = (x, y))
    surface.blit(render, rect_text)

def show_text(surface:pygame.surface, text:str, font:pygame.font, position:tuple, font_color:tuple, backgorund_color=(0, 0 ,0))->None:
    """
    Muestra texto en una surface.

    Parámetros:
    - surface (pygame.surface): La surface de Pygame donde se mostrará el texto.
    - text (str): El texto que se mostrará.
    - font (pygame.font): La fuente de Pygame utilizada para renderizar el texto.
    - position (tuple): Las coordenadas (x, y) donde se centrará el texto.
    - font_color (tuple): El color del texto en formato RGB.
    - backgorund_color: El color del fondo detrás del texto. Puede ser None para un fondo transparente.

    Return:
    -None
    """
    surface_texto = font.render(text, True, font_color, backgorund_color)
    rect_texto = surface_texto.get_rect()
    rect_texto.center = position
    surface.blit(surface_texto, rect_texto)