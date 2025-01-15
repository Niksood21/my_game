import pygame
import sys

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Наша игра")

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 48)


# background_image = pygame.image.load("D:\projectpygame(game)\background_sky_stain_65935_1440x900.jpg").convert()


def initial_window(text):
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)


running = True
game_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_started = True

    if not game_started:

        screen.fill(white)
        initial_window("Нажмите Enter, чтобы начать игру")
    else:
        screen.fill(black)
        # screen.blit(background_image, (0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()
