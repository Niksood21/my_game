import pygame
import sys

pygame.init()
pygame.mixer.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Космический шутер")
pygame.display.set_icon(pygame.image.load("images/icon.png").convert_alpha())
bg_sound = pygame.mixer.Sound('sounds/background_sound.mp3')
bg_sound.play()

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 48)

background_image = pygame.image.load("images/background_image.jpg").convert()
sprite_image = pygame.image.load("images/spaceship_image.png").convert_alpha()
sprite_image1 = pygame.image.load("images/BossEnemy-Photoroom.png").convert_alpha()
bullet_image = pygame.image.load("images/bullet_image.png").convert_alpha()
shoot_sound = pygame.mixer.Sound("sounds/bullet_sound.wav")


class Sprite:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.x = x
        self.y = y


    def move_left(self):
        if self.rect.x - self.speed >= 0:
            self.rect.x -= self.speed
            return self.rect.x

    def move_right(self):
        if self.rect.x + self.speed <= width - self.rect.width:
            self.rect.x += self.speed
            return self.rect.x

    def move_up(self):
        if self.rect.y - self.speed >= 0:
            self.rect.y -= self.speed
            return self.rect.y

    def move_down(self):
        if self.rect.y + self.speed <= height - self.rect.height:
            self.rect.y += self.speed
            return self.rect.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def restart(self):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


player = Sprite(sprite_image, width // 2 - 50, height // 2 + 150)


class Enemy:

    def __init__(self, image, x, y, hp):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hp = hp

    def draw(self, surface):
        surface.blit(self.image, self.rect)


enemy1 = Enemy(sprite_image1, 20, 20, 10)


def initial_window(text):
    text_surface = font.render(text, True, black)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)


class Bullet:
    def __init__(self, x, y):
        self.image = bullet_image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.bottom < 0


player_x = width // 2 - 50
player_y = height // 2 + 150

bullets = []
last_shot_time = 0
shot_delay = 500

running = True
game_started = False
clock = pygame.time.Clock()

label = pygame.font.Font('fonts/OpenSans_Condensed-SemiBold.ttf', 40)
restart_label = label.render("Играть заново", False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(270, 450))

gameplay = True

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
        if gameplay:
            screen.blit(background_image, (0, 0))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_x = player.move_left()
                print(player_x)
            if keys[pygame.K_RIGHT]:
                player_x = player.move_right()
                print(player_x)
            if keys[pygame.K_UP]:
                player_y = player.move_up()
                print(player_y)
            if keys[pygame.K_DOWN]:
                player_y = player.move_down()
                print(player_y)

            player.draw(screen)
            enemy1.draw(screen)

            current_time = pygame.time.get_ticks()
            if current_time - last_shot_time >= shot_delay:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))
                shoot_sound.play()
                last_shot_time = current_time

            for bullet in bullets[:]:
                bullet.move()
                bullet.draw(screen)
                if bullet.is_off_screen():
                    bullets.remove(bullet)

            player_rect = sprite_image.get_rect(topleft=(player_x, player_y))
            enemy_rect = sprite_image1.get_rect(topleft=(20, 20))

            if player_rect.colliderect(enemy_rect):
                gameplay = False

        else:
            screen.fill((255, 255, 255))
            initial_window("Вы проиграли(((")
            screen.blit(restart_label, restart_label_rect)

            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player_x = width // 2 - 50
                player_y = height // 2 + 150
                player.restart()


    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
