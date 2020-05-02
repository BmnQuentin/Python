import pygame
pygame.init()

# Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GROUND_LEVEL = 480
SPEED_INIT = 15
ACCELERATION = 100
GENERATION = 0

## Cloud
CLOUD_MIN_HEIGHT = 60
CLOUD_MAX_HEIGHT = 100
CLOUD_SPACING_MIN = 50
CLOUD_SPACING_MAX = 200

## Cactus
CACTUS_MIN_WIDTH = 30
CACTUS_MAX_WIDTH = 50
OBSTACLE_SPACING_MIN = 20
OBSTACLE_SPACING_MAX = 40
CACTUS_PROBABILITY = 0.7

## Trex
PLAYER_X = 30
NB_FRAMES_JUMP = 20
HEIGHT_JUMP = 100
FRAMES_DISPLAY = 4

## Pterodactyl
PTERODACTYL_YS = [320, 360, 430]
PTERODACTYL_WIDTH = 50

# Images
icon = pygame.image.load('images/carnivore.png')
playerImg = [pygame.image.load('images/trex.png'), pygame.image.load('images/trex2.png')]
PLAYER_WIDTH, PLAYER_HEIGHT = pygame.Surface.get_size(playerImg[0])
cloudImg= [pygame.image.load('images/cloud.png'), pygame.image.load('images/cloud3.png'), pygame.image.load('images/cloud4.png'),
           pygame.image.load('images/cloud5.png'), pygame.image.load('images/cloud6.png')]
cactusImg = [pygame.image.load('images/cactus.png'), pygame.image.load('images/cactus2.png'), pygame.image.load('images/cactus3.png')]
CACTUS_IMG_WIDTH, CACTUS_IMG_HEIGHT = pygame.Surface.get_size(cactusImg[0])
CLOUD_IMG_WIDTH, CLOUD_IMG_HEIGHT = pygame.Surface.get_size(cloudImg[0])
bgImg = pygame.image.load('images/background.png')
birdImg = [pygame.image.load('images/pterodactyl1.png'), pygame.image.load('images/pterodactyl2.png')]
PTERODACTYL_IMG_WIDTH, PTERODACTYL_IMG_HEIGHT = pygame.Surface.get_size(birdImg[0])
PTERODACTYL_HEIGHT = PTERODACTYL_WIDTH * PTERODACTYL_IMG_HEIGHT // PTERODACTYL_IMG_WIDTH
birdImg = [pygame.transform.scale(img, (PTERODACTYL_WIDTH, PTERODACTYL_HEIGHT)) for img in birdImg]

# Initialize pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# settings
clock = pygame.time.Clock()