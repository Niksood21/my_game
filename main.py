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
bg_sound2 = pygame.mixer.Sound('sounds/bgsound2.mp3')
bg_sound2.set_volume(0.2)
bg_sound3 = pygame.mixer.Sound('sounds/bgsound3.mp3')
bg_sound3.set_volume(0.2)

white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font(None, 48)

background_image = pygame.image.load("images/background_image.jpg").convert()
sprite_image = pygame.image.load("images/spaceship_image.png").convert_alpha()
sprite_image1 = pygame.image.load("images/BossEnemy-Photoroom.png").convert_alpha()
bullet_image = pygame.image.load("images/bullet_image.png").convert_alpha()
enemy_bullet = pygame.image.load("images/enemy_bullet.png").convert_alpha()
shoot_sound = pygame.mixer.Sound("sounds/bullet_sound.wav")
BossBullet_image = pygame.image.load("images/BulletBoss.png").convert_alpha()
Big_Enemy_Ship = pygame.image.load("images/BigEnemyShip.png").convert_alpha()


class Player:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(width // 2 - self.image.get_rect().size[0] // 2, 550))
        self.speed = 4
        self.hp = 100
        self.mxhp = 100

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
        self.rect = self.image.get_rect(topleft=(width // 2 - self.image.get_rect().size[0] // 2, 550))

    def alive(self):
        return self.hp > 0

    def restart_hp(self):
        self.hp = self.mxhp


player = Player(sprite_image)


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
        self.hp = 50
        self.mxhp = 50

    def random_move(self):
        self.rect.x += self.speed * self.x
        self.rect.y += self.speed * self.y

        if self.rect.left < 0 or self.rect.right > width:
            self.x *= -1
        if self.rect.top < 0 or self.rect.bottom > height:
            self.y *= -1

    def shoot(self):
        current_time_enemy = pygame.time.get_ticks()
        if current_time_enemy - self.last_shot_time >= self.shot_delay:
            bullets_enemy = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.bullets.append(bullets_enemy)
            self.last_shot_time = current_time_enemy

    def update_bullets(self):
        for bullet_enemy in self.bullets[:]:
            bullet_enemy.move()
            if bullet_enemy.is_off_screen():
                self.bullets.remove(bullet_enemy)

    def random_move_enemy(self):
        self.rect.x += self.speed * self.x
        self.rect.y += self.speed * self.y

        if self.rect.left < 0 or self.rect.right > width:
            self.x *= -1
        if self.rect.top < 0 or self.rect.bottom > height:
            self.y *= -1

    def damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0

    def alive(self):
        return self.hp > 0

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def restart(self):
        self.rect = self.image.get_rect(topleft=(random.randint(0, width - 50), random.randint(0, height - 400)))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet_enemy in self.bullets:
            bullet_enemy.draw(surface)

    def restart_hp(self):
        self.hp = self.mxhp


class Boss:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(height // 2 - self.image.get_rect().size[0] // 2, width - 700))
        self.hp = 300
        self.speed_x = 3
        self.speed_y = 1
        self.bullets = []
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_delay = 1000

    def move(self):
        if self.rect.right >= width or self.rect.left <= 0:
            self.speed_x *= -1
        self.rect.x += self.speed_x

    def shoot(self):
        current_time_enemy = pygame.time.get_ticks()
        if current_time_enemy - self.last_shot_time >= self.shot_delay:
            bullets_enemy = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.bullets.append(bullets_enemy)
            self.last_shot_time = current_time_enemy

    def update_bullets(self):
        for bullet_enemy in self.bullets[:]:
            bullet_enemy.move()
            if bullet_enemy.is_off_screen():
                self.bullets.remove(bullet_enemy)

    def alive(self):
        return self.hp > 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for bullet_enemy in self.bullets:
            bullet_enemy.draw(surface)


boss = Boss(Big_Enemy_Ship)


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

cause = None

enemies = [Enemy(sprite_image1) for _ in range(7)]

sound1 = False
sound2 = False
sound3 = False

while running:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_1]:
        sound1 = True
        sound2 = False
        sound3 = False
        bg_sound2.stop()
        bg_sound3.stop()
        if sound1:
            bg_sound.stop()
            bg_sound.play(-1)

    if keys[pygame.K_2]:
        sound1 = False
        sound2 = True
        sound3 = False
        bg_sound.stop()
        bg_sound3.stop()
        if sound2:
            bg_sound2.stop()
            bg_sound2.play(-1)

    if keys[pygame.K_3]:
        sound1 = False
        sound2 = False
        sound3 = True
        bg_sound.stop()
        bg_sound2.stop()
        if sound3:
            bg_sound3.stop()
            bg_sound3.play(-1)

    if keys[pygame.K_0]:
        sound1 = False
        sound2 = False
        sound3 = False
        bg_sound.stop()
        bg_sound2.stop()
        bg_sound3.stop()

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

            for enemy in enemies:
                enemy.shoot()
                enemy.update_bullets()

                if enemy.alive():
                    enemy.random_move()
                    enemy.draw(screen)

                    for bullet_enemy in enemy.bullets:
                        bullet_enemy.move()
                        bullet_enemy.draw(screen)
                        if bullet_enemy.rect.colliderect(player.rect) and player.alive():
                            player.damage(10)
                            enemy.bullets.remove(bullet_enemy)

            if current_time - last_shot_time >= shot_delay:
                bullets.append(Bullet(player.rect.centerx, player.rect.top))
                shoot_sound.play()
                last_shot_time = current_time

            for bullet in bullets[:]:
                bullet.move()
                bullet.draw(screen)
                if bullet.is_off_screen():
                    bullets.remove(bullet)

                for enemy in enemies[:]:
                    player_rect = sprite_image.get_rect(topleft=(player_x, player_y))
                    enemy_rect = sprite_image1.get_rect(topleft=(enemy.get_x(), enemy.get_y()))
                    if player_rect.colliderect(enemy_rect):
                        cause = "defeat"
                        gameplay = False

                    if bullet.rect.colliderect(enemy.rect) and enemy.alive():
                        enemy.damage(25)
                        bullets.remove(bullet)
                        if not enemy.alive():
                            enemies.remove(enemy)

            player.draw(screen)
            player.draw_health_bar(screen)

            if not enemies:
                # initial_window("Вы выиграли!!!")
                # cause = "win"
                # gameplay = False
                boss.shoot()
                boss.update_bullets()

                if boss.alive():
                    boss.move()
                    boss.draw(screen)

                    for bullet_enemy_boss in boss.bullets:
                        bullet_enemy_boss.move()
                        bullet_enemy_boss.draw(screen)
                        if bullet_enemy_boss.rect.colliderect(player.rect) and player.alive():
                            player.damage(10)
                            boss.bullets.remove(bullet_enemy_boss)

            if player.hp <= 0:
                cause = "defeat"
                gameplay = False

        else:
            screen.fill((255, 255, 255))
            if cause == "defeat":
                initial_window("Вы проиграли(((")
            elif cause == "win":
                initial_window("Вы выиграли!!!")

            screen.blit(restart_label, restart_label_rect)
            mouse = pygame.mouse.get_pos()
            if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player_x = width // 2 - 50
                player_y = height // 2 + 150
                player.restart()
                player.restart_hp()

                enemies = [Enemy(sprite_image1) for _ in range(7)]
                for i in enemies:
                    i.restart_hp()
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
sys.exit()
