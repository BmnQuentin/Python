from trex_classes import *
from trex_settings import *
from trex_functions import *
import os

# Title and icon
pygame.display.set_caption('Chrome T-Rex')
pygame.display.set_icon(icon)


def redrawGameWindow(bgd, clds, obs, plrs, ft, score, generation, fitness):
    bgd.draw(screen)
    for my_cloud in clds:
        my_cloud.draw(screen)
    for my_obstacle in obs:
        my_obstacle.draw(screen)
    for my_player in plrs:
        my_player.draw(screen)
    text_score = ft.render(f"Score: {score}", 1, (0, 0, 0))
    text_generation = ft.render(f"Generation: {generation}", 1, (0, 0, 0))
    text_players = ft.render(f"T-Rex: {len(plrs)}", 1, (0, 0, 0))
    text_fitness = ft.render(f"Global fitness: {fitness}", 1, (0, 0, 0))
    screen.blit(text_score, (20, 20))
    screen.blit(text_generation, (SCREEN_WIDTH - text_generation.get_rect().width , 20))
    screen.blit(text_players, (SCREEN_WIDTH - text_players.get_rect().width , 60))
    screen.blit(text_fitness, (SCREEN_WIDTH - text_fitness.get_rect().width , 100))
    pygame.display.update()


# Game loop
def main(genomes, config):

    # keeping track of the generation
    global GENERATION
    GENERATION += 1

    #neat part
    nets = []
    ge = []
    players = []

    my_font = pygame.font.SysFont("arial", 15, True, False)
    my_background = Background(bgImg)
    clouds = []
    obstacles = [Cactus(cactusImg[0], GROUND_LEVEL)]
    defaultObstacle = Cactus(cactusImg[0], GROUND_LEVEL) # not moving, gives our trex sth to see
    obstacle_counter = 0
    cloud_counter = 0
    obstacle_trigger = random.randint(OBSTACLE_SPACING_MIN, OBSTACLE_SPACING_MAX)
    cloud_trigger = random.randint(CLOUD_SPACING_MIN, CLOUD_SPACING_MAX)

    global_fitness = 0
    frame_count = 0

    for _, g in genomes:  # genome is a tuple, first value is index
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        players.append(Player(PLAYER_X, GROUND_LEVEL - PLAYER_HEIGHT, playerImg))
        g.fitness = 0
        ge.append(g)

    running = True

    while running:
        clock.tick(30)
        frame_count += 1
        score = frame_count // 2
        SPEED = SPEED_INIT + (frame_count//ACCELERATION)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # adding new elements with a probability condition
        if cloud_counter < cloud_trigger:
            cloud_counter += 1
        else:
            clouds.append(Cloud(cloudImg[random.randint(0, len(cloudImg) - 1)], random.randint(30, 200)))
            cloud_counter = 0
            cloud_trigger = random.randint(CLOUD_SPACING_MIN, CLOUD_SPACING_MAX)

        if obstacle_counter < obstacle_trigger:
            obstacle_counter += 1
        else:
            chose_obstacle = random.random()
            if (score > 100) and (chose_obstacle > CACTUS_PROBABILITY):
                obstacles.append(Pterodactyl(birdImg, random.choice(PTERODACTYL_YS)))
            else:
                obstacles.append(Cactus(cactusImg[random.randint(0, len(cactusImg) - 1)], GROUND_LEVEL))
            obstacle_counter = 0
            obstacle_trigger = random.randint(OBSTACLE_SPACING_MIN, OBSTACLE_SPACING_MAX)

        # telling the dinos which cactus to look at
        obstacle_ind = 0
        if len(players) > 0:
            if len(obstacles) > 1 and obstacles[0].x2 < players[0].x:
                obstacle_ind = 1
            if len(obstacles) > 1 and obstacles[0].x2 < players[0].x:
                obstacle_ind = 1
        else:
            running = False
            break

        # neat part to move players, give a bit of fitness and output nn
        if len(players) > 0:
            for n, player in enumerate(players):
                player.move(SPEED)
                ge[n].fitness += .5
                # Different neurons are distance to the 4 main values for obstacle 1 and 2, and speed
                output = nets[n].activate((abs(player.x - (obstacles[obstacle_ind:]+[defaultObstacle])[0].x1),
                                           abs(player.x - (obstacles[obstacle_ind:]+[defaultObstacle])[0].x2),
                                           player.y - (obstacles[obstacle_ind:] + [defaultObstacle])[0].y1,
                                           player.y - (obstacles[obstacle_ind:] + [defaultObstacle])[0].y2,
                                           abs(player.x - (obstacles[obstacle_ind+1:] + [defaultObstacle])[0].x1),
                                           abs(player.x - (obstacles[obstacle_ind+1:] + [defaultObstacle])[0].x2),
                                           player.y - (obstacles[obstacle_ind+1:] + [defaultObstacle])[0].y1,
                                           player.y - (obstacles[obstacle_ind+1:] + [defaultObstacle])[0].y2,
                                           SPEED))
                if output[0] > .5:  # only on output to our nn, jump
                    player.jump()
                    ge[n].fitness -= .1  # giving a malus for jumping too much

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for my_player in players:
                my_player.jump()

        for my_cloud in clouds:
            if my_cloud.x < - my_cloud.width:
                clouds.remove(my_cloud)
            else:
                my_cloud.move(SPEED//2)

        for my_obstacle in obstacles:
            for n, player in enumerate(players):
                if collide(my_obstacle, player):
                    ge[n].fitness -= 1  # One less move from the fitness
                    players.pop(n)
                    nets.pop(n)
                    ge.pop(n)
                    # game_over = True
            if my_obstacle.x2 < PLAYER_X:
                for g in ge:
                    g.fitness += 10  # increase the fitness when gone through a bird
            if my_obstacle.x2 < 0:
                obstacles.remove(my_obstacle)
            else:
                my_obstacle.move(SPEED)

        my_background.move(SPEED)

        global_fitness = round(max([g.fitness for g in ge] + [global_fitness]),2)
        redrawGameWindow(my_background, clouds, obstacles, players, my_font, score, GENERATION, global_fitness)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.run(main, 100) # How many generations going to run


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'neat_configuration.txt')
    run(config_path)