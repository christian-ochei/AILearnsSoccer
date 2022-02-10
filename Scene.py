import pygame
# import os

class Scene:
    def __init__(self, x=400,y=400,z=5):
        self.color = (255, 100, 0)
        self.color2 = (0, 100, 255)

    def net(self,win: pygame.display.set_mode((500,400),0,32)):

        win.fill((20, 30, 30), rect=(0, 350, 20, 100))
        win.fill(self.color,rect=(0,300,20,100))

        win.fill((20, 30, 30), rect=(780, 350, 20, 100))
        win.fill(self.color2, rect=(780, 300, 20, 100))

    def lines(self, win: pygame.display.set_mode((500, 400), 0, 32)):
        win.fill((20, 55, 55), rect=(0, 395, 800, 10))
        win.fill((10, 20, 20), rect=(0, 0, 800, 20))

    def score(self, win:pygame.display.set_mode((500,400),0,32)):
        pass


    # def score(self, win: pygame.display.set_mode((500, 400), 0, 32)):


        # win.fill((100,100,200),rect=(int(self.x-20),int(self.y-self.z-30),20,10))

