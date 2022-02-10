import pygame, sys
from pygame.locals import *
from functools import lru_cache
from player import Player
from ball import Ball
from Scene import Scene
import os
import neat
import time

pygame.init()

DISPLAY=pygame.display.set_mode((800,800),0,32)


# @lru_cache()
def main(genomes,config):
    nets = []
    ge = []
    # birds = []

    p1s = []
    # p2s = []
    balls = []


    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        p1s.append(Player(x=700))
        balls.append(Ball())
        ge.append(g)
        g.fitness = 0




    scene = Scene()

    def around(vals,i):
        x, y, z, x2, y2, z2 = vals
        return abs(x-x2)<i and abs(y-y2)<i and abs(z-z2)<i
    def by(vals):
        x, y, z, x2, y2, z2 = vals

        # print([x-x2<0,y-y2<0,z-z2<0])
        return [x-x2<0,y-y2<0,z-z2<0]
    def i(x): return 1 if x else -1

    clock = pygame.time.Clock()

    game = True

    _time = time.time()
    while game:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                pygame.quit()
                quit()

        if len(p1s) <= 0:
            break

        pygame.event.get()
        DISPLAY.fill((20, 50, 50))
        scene.lines(DISPLAY)


        for x, p1 in enumerate(p1s):
            # p2 = p2s[x]
            ball = balls[x]


            dist = (p1.x,p1.y,p1.z,ball.x,ball.y,ball.z)
            if around(dist,20):
                ge[x].fitness = + 10
                xyz = by(dist)
                ball.xv += i(xyz[0])*abs(p1.xv)
                ball.yv += i(xyz[1])*abs(p1.yv)
                ball.yv += i(xyz[2])*abs(p1.zv)

                ball.g += (abs(p1.xv)+abs(ball.yv))/20

                p1.xv -= i(xyz[0]) * abs(ball.xv)/5
                p1.yv -= i(xyz[1]) * abs(ball.yv)/5
                p1.yv -= i(xyz[2]) * abs(ball.zv)/5

            if (ball.x < 30 or ball.x>770) and ball.z < 50 and abs(ball.y-400)<50:
                if ball.x>400:
                    ge[x].fitness -= 4
                    p1s.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    balls.pop(x)

                else:
                    _time = time.time()
                    ge[x].fitness =+ 4


            if time.time()-_time>40:

                ge[x].fitness -= 3
                p1s.pop(x)
                nets.pop(x)
                ge.pop(x)
                balls.pop(x)
                game = False
                break








            # ge[x] -= 0.001
            try:
                output = nets[x].activate((p1.x,p1.y,p1.z,ball.x,ball.y,ball.z))
            except:
                game = False
                break

            if output[0] > 0.5: p1.jump()
            if output[1] > 0.5: p1.left()
            if output[2] > 0.5: p1.right()
            if output[3] > 0.5: p1.up()
            if output[4] > 0.5: p1.down()


            ball.draw(DISPLAY)
            ball.play()
            p1.play()
            p1.draw(DISPLAY)

        # -------------------------






        # p2.draw(DISPLAY)

        scene.net(DISPLAY)


        # p2.play()






        # scene.score(DISPLAY)
        # DISPLAY.
        pygame.display.update()



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)


if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "Config.txt")
    print(config_path)

    run(config_path)


