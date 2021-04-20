import sys, pygame
import random
import time
import math
from pygame_widgets import Button
from pygame.locals import *

pygame.init()

# fps
FBS = pygame.time.Clock()

# colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# screen
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill(WHITE)
pygame.display.set_caption("My Game Baby")

# speed
speed = 5

# score
score = 0
score_will_inc = True
score_spy = 1

# lives
lives = 3
lives_will_inc = True

# fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("verdana", 30)
game_over = font.render("Game Over", True, BLACK)

# background
background = pygame.image.load('images/background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

# heart
heart = pygame.image.load('images/heart.png')
heart = pygame.transform.scale(heart, (17, 17))

# music
pygame.mixer.music.load('sound/background.mp3')
pygame.mixer.music.play(-1, 0)
music_is_playing = True


def mute_music():
    global music_is_playing
    if music_is_playing:
        pygame.mixer.music.pause()
        music_is_playing = False
    else:
        pygame.mixer.music.unpause()
        music_is_playing = True


# buttons
mute_image = pygame.image.load('images/Audio-mute.png')
mute_image = pygame.transform.scale(mute_image, (17, 17))
mute = Button(screen, 20, 160, 17, 17, image=mute_image,
              onClick=mute_music)


def calculate_distance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist


class Background:
    def __init__(self):
        self.bg_image = pygame.image.load('images/background.png')
        self.bg_image = pygame.transform.scale(self.bg_image, (screen_width, screen_height))
        self.bg_image_rect = self.bg_image.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.bg_image_rect.height
        self.bgX2 = 0

        self.speed = 5

    def update(self):
        self.bgY1 += self.speed
        self.bgY2 += self.speed
        if self.bgY1 >= self.bg_image_rect.height:
            self.bgY1 = -self.bg_image_rect.height
        if self.bgY2 >= self.bg_image_rect.height:
            self.bgY2 = -self.bg_image_rect.height
    
    def render(self):
        screen.blit(self.bg_image, (self.bgX1, self.bgY1))
        screen.blit(self.bg_image, (self.bgX2, self.bgY2))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/enemy.png')
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.surf = pygame.Surface((30, 60))
        self.rect = self.surf.get_rect(center=(random.randint(90, 310), 0))

    def move(self):
        global score
        global score_will_inc
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height-90:
            score += 5
            score_will_inc = True
            self.rect.top = 0
            self.rect.center = (random.randint(90, 310), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/player.png')
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.surf = pygame.Surface((30, 100))
        self.rect = self.surf.get_rect(center=(90, 500))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 65:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-speed, 0)
        if self.rect.right < screen_width-80:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(speed, 0)

        if self.rect.top > 0:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -speed)
        if self.rect.bottom < screen_height:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


p1 = Player()
E1 = Enemy()
back_ground = Background()

# sprite groups
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(p1)

# custom event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 5000)
INC_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(INC_ENEMY, 20000)
INC_SCORE = pygame.event.Event(pygame.USEREVENT, attr1="INC_SCORE")
while True:
    pygame.event.post(INC_SCORE)
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            speed += 1

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INC_ENEMY:
            E2 = Enemy()
            enemies.add(E2)
            all_sprites.add(E2)

        if event.type == INC_SCORE:
            print("asdfasdf")

    back_ground.update()
    back_ground.render()

    mute.listen(pygame.MOUSEBUTTONUP)
    mute.draw()

    screen.blit(heart, (7, 120))

    scores = font_small.render(str(score), True, GREEN)
    live = font_small.render(str(lives), True, GREEN)
    screen.blit(scores, (20, 50))
    screen.blit(live, (30, 107))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    if score % 100 == 0 and score > 0 and lives_will_inc:
        lives += 1
        lives_will_inc = False
        score_spy = score + 5

    if score + 5 == score_spy:
        lives_will_inc = True

    for entity in enemies:
        x = calculate_distance(entity.rect.centerx, entity.rect.centery, p1.rect.centerx, p1.rect.centery)
        if x < 56 and score_will_inc:
            score += 5
            pygame.mixer.Sound('sound/drive-by.wav').play()
            score_will_inc = False

    if pygame.sprite.spritecollideany(p1, enemies):
        pygame.mixer.Sound('sound/crash.wav').play()
        pygame.mixer.music.pause()
        if lives > 1:
            lives -= 1
            time.sleep(2)
            pygame.sprite.spritecollide(p1, enemies, True)
            E3 = Enemy()
            enemies.add(E3)
            all_sprites.add(E3)

            pygame.mixer.music.unpause()
        else:
            time.sleep(2)
            pygame.mixer.music.stop()
            screen.fill(RED)
            screen.blit(game_over, (30, 250))
            pygame.display.update()
            for entity in all_sprites:
                entity.kill()
            time.sleep(2)
            pygame.quit()
            sys.exit()

    pygame.display.update()
    FBS.tick(90)
