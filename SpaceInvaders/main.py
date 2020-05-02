import pygame

# Variables
running = True
clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 560
FRAME_COUNT = 0
PLAYER_SPEED = 15
PLAYER_WIDTH = 64
ENEMY_WIDTH = 32
ENEMY_SPEED = 7
MAX_HEALTH = 5
BULLET_WIDTH = 32
BULLET_SPEED = 15
BULLET_Y_INIT = HEIGHT - BULLET_WIDTH - 50
NUMBER_BULLETS = 10
NUMBER_ENEMIES = [10, 3]
BODY_COUNT = 0

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Images
icon = pygame.image.load('images/gaming.png')
bgImg = pygame.image.load('images/background.jpg')
playerImg = pygame.image.load('images/spaceship.png')
enemyImg = [pygame.transform.scale(pygame.image.load('images/invader1.png'), (ENEMY_WIDTH, ENEMY_WIDTH)),
            pygame.transform.scale(pygame.image.load('images/invader2.png'), (ENEMY_WIDTH, ENEMY_WIDTH))]
bulletImg = pygame.image.load('images/bullet.png')

# Sounds
invaderKilledSound = pygame.mixer.Sound('sounds/invaderkilled.wav')
explosionSound = pygame.mixer.Sound('sounds/explosion.wav')
bulletSound = pygame.mixer.Sound('sounds/shoot.wav')

# Title and icon
pygame.display.set_caption('Space Invaders')
pygame.display.set_icon(icon)


# classes
class player(object):
    def __init__(self, x, y, width, vel):
        self.x = x
        self.y = y
        self.width = width
        self.vel = vel
        self.hitbox = (self.x, self.y, PLAYER_WIDTH, PLAYER_WIDTH)
        self.visible = True

    def draw(self, win):
        screen.blit(playerImg, (self.x, self.y))
        self.hitbox = (self.x, self.y, PLAYER_WIDTH, PLAYER_WIDTH)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.visible = False


class enemy(object):
    def __init__(self, x, y, width, vel):
        self.x = x
        self.y = y
        self.width = width
        self.vel = vel
        self.hitbox = (self.x, self.y + 5, ENEMY_WIDTH, ENEMY_WIDTH - 10)
        self.health = MAX_HEALTH

    def draw(self, win):
        screen.blit(enemyImg[(FRAME_COUNT // 5) % 2], (self.x, self.y))
        self.hitbox = (self.x, self.y + 5, ENEMY_WIDTH, ENEMY_WIDTH - 10)
        if self.health < MAX_HEALTH:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, 2), 2)
            pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y, self.width * (self.health / MAX_HEALTH), 2), 2)

        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.health -= 1


class projectile(object):
    def __init__(self, x, y, width, vel):
        self.x = x
        self.y = y
        self.width = width
        self.vel = vel
        self.hitbox = (self.x + 10, self.y, 10, BULLET_WIDTH)

    def draw(self, win):
        screen.blit(bulletImg, (self.x, self.y))
        self.hitbox = (self.x + 10, self.y, 10, BULLET_WIDTH)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


my_player = player(WIDTH / 2 - PLAYER_WIDTH / 2, HEIGHT - PLAYER_WIDTH - 50, PLAYER_WIDTH, PLAYER_SPEED)
bullets = []
enemies = [enemy(ENEMY_SPEED + i * ENEMY_WIDTH * 1.5, ENEMY_WIDTH * (j + 0.5), ENEMY_WIDTH, ENEMY_SPEED)
           for i in range(NUMBER_ENEMIES[0]) for j in range(NUMBER_ENEMIES[1])]
shootLoop = 0
font1 = pygame.font.SysFont("arial", 15, True, False)
font2 = pygame.font.SysFont("arial", 45, True, False)
game_over = False


def redrawGameWindow():
    screen.blit(bgImg, (0, 0))
    text = font1.render(f"Score: {BODY_COUNT}", 1, (0, 0, 0))
    screen.blit(text, (20, 20))
    if not game_over:
        for bullet in bullets:
            bullet.draw(screen)
        my_player.draw(screen)
    else:
        text_game_over = font2.render("GAME OVER", 1, (0, 0, 0))
        screen.blit(text_game_over, ((WIDTH - text_game_over.get_rect().width) // 2, HEIGHT // 2))
    for my_enemy in enemies:
        my_enemy.draw(screen)
    pygame.display.update()


def collide(object1, object2):
    if ((((object2.hitbox[0] > object1.hitbox[0]) and (object2.hitbox[0] < object1.hitbox[0] + object1.hitbox[2])) or
         ((object2.hitbox[0] + object2.hitbox[2] > object1.hitbox[0]) and (
                 object2.hitbox[0] + object2.hitbox[2] < object1.hitbox[0] + object1.hitbox[2]))) and
            (((object2.hitbox[1] > object1.hitbox[1]) and (
                    object2.hitbox[1] < object1.hitbox[1] + object1.hitbox[3])) or
             ((object2.hitbox[1] + object2.hitbox[3] > object1.hitbox[1]) and (
                     object2.hitbox[1] + object2.hitbox[3] < object1.hitbox[1] + object1.hitbox[3])))):
        return True
    else:
        return False


# Game loop
while running:
    clock.tick(27)
    shootLoop = (shootLoop + 1) % 3  # basic timer for shooting
    FRAME_COUNT += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and my_player.x > PLAYER_SPEED:
        my_player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and my_player.x < WIDTH - my_player.width - PLAYER_SPEED:
        my_player.x += PLAYER_SPEED
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if len(bullets) < NUMBER_BULLETS:  # how many bullets at the same time o the screen
            bulletSound.play()
            bullets.append(
                projectile(my_player.x + my_player.width // 2 - BULLET_WIDTH // 2, BULLET_Y_INIT, BULLET_WIDTH,
                           BULLET_SPEED))
    if keys[pygame.K_a]:
        running = False

    for bullet in bullets:
        for my_enemy in enemies:
            if collide(bullet, my_enemy):
                explosionSound.play()
                BODY_COUNT += 1
                my_enemy.hit()
                bullets.pop(bullets.index(bullet))
                break
        if bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    if len(enemies) > 0:
        global_enemies_left = min([my_enemy.x for my_enemy in enemies])
        global_enemies_right = max([my_enemy.x for my_enemy in enemies]) + ENEMY_WIDTH
        for my_enemy in enemies:
            if my_enemy.health <= 0:
                invaderKilledSound.play()
                enemies.pop(enemies.index(my_enemy))
                BODY_COUNT += 5
            if global_enemies_left <= ENEMY_WIDTH // 2:
                my_enemy.vel = ENEMY_SPEED
                my_enemy.y += my_enemy.width // 2
            elif global_enemies_right >= WIDTH - ENEMY_WIDTH // 2:
                my_enemy.vel = - ENEMY_SPEED
                my_enemy.y += ENEMY_WIDTH / 2
            if collide(my_enemy, my_player):
                my_player.hit()
                game_over = True
            my_enemy.x += my_enemy.vel

    redrawGameWindow()
