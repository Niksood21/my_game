import pygame
import sys

pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Космический шутер")

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 48)

background_image = pygame.image.load("images/background_image.jpg").convert()
sprite_image = pygame.image.load("images/spaceship_image.png").convert_alpha()


class Sprite:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def move_left(self):
        if self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed

    def move_right(self):
        if self.rect.x + self.speed <= width - self.rect.width:
            self.rect.x += self.speed

    def move_up(self):
        if self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.y + self.speed <= height - self.rect.height:
            self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Sprite(sprite_image, width // 2 - 50, height // 2 + 150)


def initial_window(text):
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)


running = True
game_started = False
clock = pygame.time.Clock()
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
        screen.blit(background_image, (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()
        player.draw(screen)
        clock.tick(120)
    pygame.display.flip()
pygame.quit()
sys.exit()
