import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Космический шутер")
pygame.display.set_icon(pygame.image.load("images/icon.png").convert_alpha())
bg_sound = pygame.mixer.Sound('sounds/background_sound.mp3')
bg_sound.set_volume(0.2)
bg_sound.play(-1)

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 48)

background_image = pygame.image.load("images/background_image.jpg").convert()
sprite_image = pygame.image.load("images/spaceship_image.png").convert_alpha()
sprite_image1 = pygame.image.load("images/BossEnemy-Photoroom.png").convert_alpha()
bullet_image = pygame.image.load("images/bullet_image.png").convert_alpha()
enemy_bullet = pygame.image.load("images/enemy_bullet.png").convert_alpha()
shoot_sound = pygame.mixer.Sound("sounds/bullet_sound.wav")


class Sprite:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 4
        self.hp = 100
        self.mxhp = 100
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

    def damage(self, damages):
        self.hp -= damages
        if self.hp < 0:
            self.hp = 0

    def draw_health_bar(self, surface):
        pygame.draw.rect(surface, "red", (10, 10, 180, 20))
        health_view = self.hp / self.mxhp
        bar_width = 180 * health_view
        pygame.draw.rect(surface, "green", (10, 10, bar_width, 20))

    def restart(self):
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


player = Sprite(sprite_image, width // 2 - 50, height // 2 + 150)


class Enemy:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(random.randint(0, width - 50), random.randint(0, height - 400)))
        self.speed = random.uniform(1, 3)
        self.x = random.choice([-1, 1])
        self.y = random.choice([-1, 1])
        self.bullets = []
        self.last_shot_time = 0
        self.shot_delay = 2000

    def random_move(self):
        self.rect.x += self.speed * self.x
        self.rect.y += self.speed * self.y

        if self.rect.left < 0 or self.rect.right > width:
            self.x *= -1
        if self.rect.top < 0 or self.rect.bottom > height:
            self.y *= -1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shot_delay:
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def random_move(self):
        self.rect.x += self.speed * self.x
        self.rect.y += self.speed * self.y

        if self.rect.left < 0 or self.rect.right > width:
            self.x *= -1
        if self.rect.top < 0 or self.rect.bottom > height:
            self.y *= -1

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet_enemy in self.bullets:
            bullet_enemy.draw(surface)


enemy1 = Enemy(sprite_image1)


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


class EnemyBullet:
    def __init__(self, x, y):
        self.image = enemy_bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.top > height


bullets = []
last_shot_time = 0
shot_delay = 500

running = True
game_started = False
clock = pygame.time.Clock()

player_x = width // 2 - 50
player_y = height // 2 + 150

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
            if keys[pygame.K_RIGHT]:
                player_x = player.move_right()
            if keys[pygame.K_UP]:
                player_y = player.move_up()
            if keys[pygame.K_DOWN]:
                player_y = player.move_down()

            current_time = pygame.time.get_ticks()
            enemy1.shoot()
            enemy1.update_bullets()

            if current_time - last_shot_time >= shot_delay:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))
                shoot_sound.play()
                last_shot_time = current_time

            for bullet in bullets[:]:
                bullet.move()
                bullet.draw(screen)
                if bullet.is_off_screen():
                    bullets.remove(bullet)

            player.draw(screen)
            enemy1.random_move()
            enemy1.draw(screen)
            for bullet in enemy1.bullets:
                bullet.draw(screen)
            player.draw_health_bar(screen)

            player_rect = sprite_image.get_rect(topleft=(player_x, player_y))
            enemy_rect = sprite_image1.get_rect(topleft=(enemy1.get_x(), enemy1.get_y()))
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