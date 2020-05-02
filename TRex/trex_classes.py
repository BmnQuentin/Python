import random
from trex_settings import *

class Background(object):
    def __init__(self, img):
        self.y = 0
        self.img = img
        self.width = pygame.Surface.get_width(img)
        self.x1 = 0
        self.x2 = self.width
    def move(self, speed):
        self.vel = speed
        self.x1 -= self.vel
        self.x2 -= self.vel
        if self.x1 < - self.width:
            self.x1 = self.x2 + self.width
        if self.x2 < - self.width:
            self.x2 = self.x1 + self.width
    def draw(self, win):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

class Cloud(object):
    def __init__(self, img, y):
        self.img = img
        self.x = SCREEN_WIDTH
        self.y = y
        self.width = random.randint(CLOUD_MIN_HEIGHT, CLOUD_MAX_HEIGHT)
        self.height = self.width * CLOUD_IMG_HEIGHT // CLOUD_IMG_WIDTH
        self.img = pygame.transform.scale(img, (self.width, self.height))
    def move(self, speed):
        self.vel = speed // 2
        self.x -= self.vel
    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

class Cactus(object):
    def __init__(self, img, y):
        self.img = img
        self.width = random.randint(CACTUS_MIN_WIDTH, CACTUS_MAX_WIDTH)
        self.height = self.width * CACTUS_IMG_HEIGHT // CACTUS_IMG_WIDTH
        self.x1 = SCREEN_WIDTH
        self.x2 = self.x1 + self.width
        self.y1 = y - self.height
        self.y2 = y
        self.img = pygame.transform.scale(img, (self.width, self.height))
        self.hitbox = (self.x1, self.y1, self.width, self.height)
    def move(self, speed):
        self.vel = speed
        self.x1 -= self.vel
        self.x2 = self.x1 + self.width
    def draw(self, win):
        win.blit(self.img, (self.x1, self.y1))
        self.hitbox = (self.x1, self.y1, self.width, self.height)
        # pygame.draw.rect(win, (0, 255, 0), self.hitbox, 2 )

class Player(object):
    def __init__(self, x, y, img_list):
        self.x = x
        self.y = y
        self.img_list = img_list
        self.hitbox = (self.x, self.y, PLAYER_WIDTH-20, PLAYER_HEIGHT)
        self.img_count = 0
        self.img = img_list[0]
        self.visible = True
        self.jumping = False
        self.tick_count = 0
    def jump(self):
        if self.jumping == False:
            self.tick_count = 0
        self.jumping = True
    def move(self, speed):
        self.vel = speed
        if self.jumping:
            if self.tick_count <= NB_FRAMES_JUMP:
                d = self.tick_count * (NB_FRAMES_JUMP - self.tick_count) * 4 * HEIGHT_JUMP / NB_FRAMES_JUMP ** 2
                self.y = GROUND_LEVEL - PLAYER_HEIGHT - d
                self.tick_count +=1
            else:
                self.jumping = False
    def draw(self, win):
        self.img_count +=1
        self.img = self.img_list[(self.img_count//FRAMES_DISPLAY)%2]
        win.blit(self.img, (self.x, self.y))
        self.hitbox = (self.x, self.y, PLAYER_WIDTH-20, PLAYER_HEIGHT)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class Pterodactyl(object):
    def __init__(self, img_list, y):
        self.img_list = img_list
        self.img = img_list[0]
        self.width = PTERODACTYL_WIDTH
        self.height = PTERODACTYL_HEIGHT
        self.x1 = SCREEN_WIDTH
        self.x2 = self.x1 + self.width
        self.y1 = y
        self.y2 = self.y1 + self.height
        self.img_count = 0
        self.hitbox = (self.x1, self.y1, self.width, self.height)
    def move(self, speed):
        self.vel = speed
        self.x1 -= self.vel
        self.x2 = self.x1 + self.width
    def draw(self, win):
        self.img_count += 1
        self.img = self.img_list[(self.img_count // FRAMES_DISPLAY) % 2]
        win.blit(self.img, (self.x1, self.y1))
        self.hitbox = (self.x1, self.y1, self.width, self.height)
        # pygame.draw.rect(win, (0, 255, 0), self.hitbox, 2)