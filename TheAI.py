import neat
import pygame, sys
from pygame.locals import *
from player import Player
from ball import Ball
from Scene import Scene
from time import sleep, time
from math import sqrt
import os

def distanceto(a,b,c,a2,b2,c2):
    return sqrt((a-a2)**2+(b-b2)**2+(c-c2)**2)
pygame.init()
DISPLAY=pygame.display.set_mode((800,800),0,32)
Font = pygame.font.SysFont("comicsans", 60)

def around(vals,i):
    x, y, z, x2, y2, z2 = vals
    return abs(x-x2)<i and abs(y-y2)<i and abs(z-z2)<i
def by(vals):
    x, y, z, x2, y2, z2 = vals
    return [x-x2<0,y-y2<0,z-z2<0]
def i(x): return 1 if x else -1


def main(genomes,config):
    nets = []
    ge = []
    p1s = []
    p2s = []
    balls = []
    scene = Scene()
    # print(len(genomes))

    for xx, (_, g) in enumerate(genomes):
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)

        if xx < len(genomes)/2:
            p1s.append(Player(x=100,ateam=0))
            balls.append(Ball())
        else:
            p2s.append(Player(x=700, ateam=1))

        ge.append(g)
        g.fitness = 0
    game = True
    clock = pygame.time.Clock()
    _time = time()



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
        scene.net(DISPLAY)
        num = len(p1s)


        for x,p1 in enumerate(p1s):
            score1 = 0
            score2 = 0
            ball = balls[x]
            try:
                p2 = p2s[x]
            except:
                break


            dist = (p1.x,p1.y,p1.z,ball.x,ball.y,ball.z)
            score1 += 1/(distanceto(*dist)+1)/100



            #  Collision ----P1 With Ball-----------

            if around(dist,20):

                xyz = by(dist)
                ball.xv += i(xyz[0])*abs(p1.xv)
                ball.yv += i(xyz[1])*abs(p1.yv)
                ball.yv += i(xyz[2])*abs(p1.zv)

                ball.g += (abs(p1.xv)+abs(p2.yv))/20

                p1.xv -= i(xyz[0]) * abs(ball.xv)/5
                p1.yv -= i(xyz[1]) * abs(ball.yv)/5
                p1.yv -= i(xyz[2]) * abs(ball.zv)/5

            #  Collision ----P2 With Ball-----------
            dist = (p2.x, p2.y, p2.z, ball.x, ball.y, ball.z)
            score2 += 1 / (distanceto(*dist) + 1) / 100
            if around(dist, 20):

                xyz = by(dist)
                ball.xv += i(xyz[0]) * abs(p2.xv)
                ball.yv += i(xyz[1]) * abs(p2.yv)
                ball.yv += i(xyz[2]) * abs(p2.zv)

                ball.g += (abs(p2.xv) + abs(p2.yv)) / 20

                p2.xv -= i(xyz[0]) * abs(ball.xv) / 5
                p2.yv -= i(xyz[1]) * abs(ball.yv) / 5
                p2.yv -= i(xyz[2]) * abs(ball.zv) / 5

            #  Collision ----P2 With Ball-----------
            dist = (p2.x, p2.y, p2.z, p1.x, p1.y, p1.z)
            if around(dist, 20):
                xyz = by(dist)
                p1.xv += i(xyz[0]) * abs(p2.xv)
                p1.yv += i(xyz[1]) * abs(p2.yv)
                p1.yv += i(xyz[2]) * abs(p2.zv)

                # p1.g += (abs(p2.xv) + abs(p2.yv))

                p2.xv -= i(xyz[0]) * abs(p1.xv)
                p2.yv -= i(xyz[1]) * abs(p1.yv)
                p2.yv -= i(xyz[2]) * abs(p1.zv)

            p1.play()
            p2.play()
            ball.play()

            if x%40 == 1:

                p1.draw(DISPLAY)
                p2.draw(DISPLAY)
                # p1.color = (0,int(team)*255,0)
                # p2.color = (0, int(team)*255, 0)
                ball.draw(DISPLAY)



            if (ball.x < 30 or ball.x>770) and ball.z < 50 and abs(ball.y-400)<50:
                if ball.x<400:
                    ge[x].fitness += 15
                else:
                    ge[x+len(p1s)].fitness += 15

                game=False
                break

            b = ball

            score1 += (1/(distanceto(b.x,b.y,b.z,800,400,20)+0.4))/10 # Should / by 10
            score2 += (1/(distanceto(b.x,b.y,b.z,0,400,20)+0.4))/10

            # print(1*(len(p1s)))
            ge[x].fitness += score1**2/40
            # print(len(p1s))
            ge[x+len(p1s)].fitness += score2**2/40

            if time() - _time > 60:
                game = False
                break


            # Controls -----------------------------------

            try:
                output = nets[x].activate((p1.x,p1.y,p1.z,p1.xv,p1.yv,p1.zv,p1.g,
                                           p2.x,p2.y,p2.z,p2.xv,p2.yv,p2.zv,p2.g

                                           ,ball.x,ball.y,ball.z,ball.xv,ball.yv,ball.g,0))

                output2 = nets[x+len(p1s)].activate((p1.x,p1.y,p1.z,p1.xv,p1.yv,p1.zv,p1.g,
                                           p2.x,p2.y,p2.z,p2.xv,p2.yv,p2.zv,p2.g

                                           ,ball.x,ball.y,ball.z,ball.xv,ball.yv,ball.g,100))
            except Exception as e:
                print(e)
                game = False
                break


            if output[0] > 0.5: p1.jump()
            if output[1] > 0.5: p1.left()
            if output[2] > 0.5: p1.right()
            if output[3] > 0.5: p1.up()
            if output[4] > 0.5: p1.down()

            if output2[0] > 0.5: p2.jump()
            if output2[1] > 0.5: p2.left()
            if output2[2] > 0.5: p2.right()
            if output2[3] > 0.5: p2.up()
            if output2[4] > 0.5: p2.down()


        pygame.display.update()


# Boiler Plate


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

    winner = p.run(main,1000)


if __name__ == "__main__":

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "Config.txt")
    print(config_path)

    run(config_path)
    assert False



