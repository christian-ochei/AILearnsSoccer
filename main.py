import pygame, sys
from pygame.locals import *
from player import Player
from ball import Ball
from Scene import Scene
from time import sleep
from math import sqrt
def distanceto(a,b,c,a2,b2,c2):
    return sqrt((a-a2)**2+(b-b2)**2+(c-c2)**2)


pygame.init()

DISPLAY=pygame.display.set_mode((800,800),0,32)
score2 = 0
score1 = 0



p1 = Player(x=700, team=1)
p2 = Player(x=100, team=0)
ball = Ball()
scene = Scene()
Font = pygame.font.SysFont("comicsans", 60)


def around(vals,i):
    x, y, z, x2, y2, z2 = vals
    return abs(x-x2)<i and abs(y-y2)<i and abs(z-z2)<i

def by(vals):
    x, y, z, x2, y2, z2 = vals

    # print([x-x2<0,y-y2<0,z-z2<0])
    return [x-x2<0,y-y2<0,z-z2<0]


def i(x): return 1 if x else -1

def reset():
    global p1
    global p2
    global ball



    p1 = Player(x=700, team=1)
    p2 = Player(x=100, team=0)
    ball = Ball()



while True:
    sleep(0.001)
    pygame.event.get()
    DISPLAY.fill((20, 50, 50))
    # for event in pygame.event.get():
    key = pygame.key.get_pressed()
    if key[K_LEFT]:     p1.left()
    if key[K_RIGHT]:    p1.right()
    if key[K_UP]:       p1.up()
    if key[K_DOWN]:     p1.down()
    if key[K_SPACE]:    p1.jump()

    #  ---------------

    if key[K_a]:     p2.left()
    if key[K_d]:    p2.right()
    if key[K_w]:       p2.up()
    if key[K_s]:     p2.down()
    if key[K_e]:    p2.jump()

    #  Collision ----P1 With Ball-----------
    dist = (p1.x,p1.y,p1.z,ball.x,ball.y,ball.z)
    # score1 += 1/(distanceto(*dist)+1)/100
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
    # score2 += 1 / (distanceto(*dist) + 1) / 100
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


    scene.lines(DISPLAY)


    p1.play()

    p1.draw(DISPLAY)
    p2.draw(DISPLAY)
    ball.draw(DISPLAY)
    scene.net(DISPLAY)


    p2.play()


    ball.play()

    if (ball.x < 30 or ball.x>770) and ball.z < 50 and abs(ball.y-400)<50:
        if ball.x>400:
            score1 += 50
        else:
            score2 += 50
        reset()

    score1 += (1/(distanceto(ball.x,ball.y,ball.z,800,400,20)+0.4))/10
    score2 += (1/(distanceto(ball.x,ball.y,ball.z,0,400,20)+0.4))/10

    # scene.score(DISPLAY)
    # DISPLAY.
    pygame.display.update()

    # os.system("ls")
    # os.system('clear')
    print(score1, score2)







