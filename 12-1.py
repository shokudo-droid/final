import pyxel
import math

class Ball:
    def __init__(self):
        self.restart()  

    def restart(self):
        self.x = pyxel.rndi(0, 199)
        self.y = 0
        angle = pyxel.rndi(30, 150)
        self.vx = math.cos(math.radians(angle))
        self.vy = math.sin(math.radians(angle))
        self.speed = 6

    def move(self, acceleration):
        self.speed += acceleration
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

       
        if self.x >= 200 or self.x <= 0:
            self.vx = -self.vx

    def update(self, acceleration):
        self.move(acceleration)

class Pad:
    def __init__(self):
        self.x = 100  
        self.width = 40
        self.height = 5
        self.y = 195  

    def update(self):
        self.x = pyxel.mouse_x

    def check_collision(self, ball):
        
        return self.y <= ball.y < self.y + self.height and (self.x - self.width / 2 < ball.x < self.x + self.width / 2)

class Game:
    def __init__(self):
        pyxel.init(200, 200)
        
        self.acceleration = 0.01  
        self.score = 0
        self.misses = 0  
        self.balls = [Ball()]
        self.pad = Pad()

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.misses >= 10:
            return

        self.pad.update()

        for ball in self.balls:
            ball.update(self.acceleration)

           
            if ball.y >= 200:
                if not self.pad.check_collision(ball):
                    self.misses += 1
                ball.restart()  

           
            if self.pad.check_collision(ball):
                self.score += 1

       
        if self.score % 10 == 0 and len(self.balls) < (self.score // 10) + 1:
            self.balls.append(Ball())

    def draw(self):
        pyxel.cls(7)

        if self.misses >= 10:
            pyxel.text(80, 100, "You are dead", pyxel.COLOR_RED)
            return

        for ball in self.balls:
            pyxel.circ(ball.x, ball.y, 10, 6)

        pyxel.rect(self.pad.x - self.pad.width / 2, self.pad.y, self.pad.width, self.pad.height, 14)
        pyxel.text(20, 20, f"Score: {self.score}", 0)
        pyxel.text(20, 30, f"Misses: {self.misses}", 0)

Game()
