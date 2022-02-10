import pygame

class Ball:
    def __init__(self, x=400,y=400,z=5):
        self.x = x
        self.y = y
        self.z = z
        self.g = 0
        # Anything ending with v is Velocity

        self.xv = 0
        self.yv = 0
        self.zv = 0
        self.onFoot = True
        self.Free = self.onFoot
        self.acc = 0.004

    def jump(self):
        # if :
        if self.onFoot:
            # self.z += 3
            self.g -= 0.01 if self.Free else 0.0005
            # self.onFoot = False

    def left(self): self.xv += -self.acc  if self.Free else -self.acc/5
    def right(self): self.xv += self.acc  if self.Free else self.acc/5
    def up(self): self.yv += -self.acc    if self.Free else -self.acc/5
    def down(self): self.yv += self.acc   if self.Free else self.acc/5

    def draw(self,win: pygame.display.set_mode((500,400),0,32)):

        win.fill((0, 0, 0), rect=(int(self.x - 20), int(self.y - 20), 20, 20))
        win.fill((20, 20, 20), rect=(int(self.x - 20), int(self.y - self.z - 20), 20, 20))
        win.fill((5, 5, 5), rect=(int(self.x - 20), int(self.y - self.z - 40), 20, 20))


    def play(self):
        # Collision -------------
        if self.x>800:
            self.x = 800
            self.xv = -abs(self.xv)
        if self.y>800:
            self.y = 800
            self.yv = -abs(self.yv)

        if self.x<20:
            self.x = 20
            self.xv = abs(self.xv)
        if self.y<20:
            self.y = 20
            self.yv = abs(self.yv)



        # ----------------------

        if self.z<0:

            self.z = 0


            self.g = -abs(self.g)
                # self.z += 0.4
        else:
            self.g+=0.001

        self.Free = self.z < 30

        tspeed = 80

        self.x += self.xv*tspeed
        self.y += self.yv*tspeed
        self.z -= self.g*tspeed

        self.zv +=self.g


        self.xv = self.xv/1.002
        self.yv = self.yv/1.002
        self.g = self.g/1.001



