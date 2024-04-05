import pygame, random, time, sys, math

pygame.init()

WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

class Paddle:
    def __init__(self, color, position, width, height, speed=1):
        self.color = color
        self.position = list(position)
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = None
    
    def draw(self):
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        pygame.draw.rect(window, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self.position[1] > 0:
                self.position[1] -= self.speed

        if keys[pygame.K_DOWN]:
            if self.position[1] < HEIGHT - self.height:
                self.position[1] += self.speed

class Ball:
    def __init__(self, position, width, height, speed=0.4):
        self.position = list(position)
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)        

    def draw(self, color):
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        pygame.draw.rect(window, color, self.rect)

    def move(self):
        self.position[0] += self.speed * self.direction[0]
        self.position[1] += self.speed * self.direction[1]

        if self.position[1] < 0 or self.position[1] > HEIGHT - self.height:
            self.direction[1] *= -1   

class Timer:
    def __init__(self, timeout, color, size=36):
        self.timeout = timeout
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont('Arial', self.size)        
        self.last_time = 0
        self.surface = self.font.render(str(self.timeout), True, self.color)

    def runTimer(self):
        now = pygame.time.get_ticks()
        if now - self.last_time >= 1000:
            self.surface = self.font.render(str(self.timeout), True, self.color)
            self.last_time = now
            self.timeout -= 1     

        if self.timeout >= 0:                   
            window.blit(self.surface, (WIDTH // 2 - self.surface.get_width() // 2, HEIGHT // 2 - self.surface.get_height() // 2))

class Counter:
    def __init__(self, color, position, size=36):
        self.color = color
        self.size = size
        self.position = position
        self.font = pygame.font.SysFont('Arial', self.size)  
        self.value = 0  

    def __iadd__(self, other):
        self.value += other
        return self
    
    def __eq__(self, other):
        return self.value == other

    def draw(self):
        self.surface = self.font.render(str(self.value), True, self.color)    
        window.blit(self.surface, (self.position[0] - self.surface.get_width() // 2, self.position[1] - self.surface.get_height() // 2))

class Text:
    def __init__(self, color, position):
        self.size = 36
        self.position = position
        self.font = pygame.font.SysFont('Arial', self.size)
        self.value = 0
        self.color = color

    def render(self, text):
        self.surface = self.font.render(text, True, self.color)
        window.blit(self.surface, (self.position[0] - self.surface.get_width() // 2, self.position[1] - self.surface.get_height() // 2))

def lerp(x, x0, x1, y0, y1):
    return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))

def colorFromDistance(a, b, t, max_distance):
    r = int(lerp(t, 0, max_distance, a[0], b[0]))
    g = int(lerp(t, 0, max_distance, a[1], b[1]))
    b = int(lerp(t, 0, max_distance, a[2], b[2]))
    return (r, g, b)

def distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def main():
    playerOne = Paddle((255, 0, 0), (10, HEIGHT//2 - 25), 15, 100)
    playerTwo = Paddle((0, 0, 255), (WIDTH - 20, HEIGHT//2 - 25), 15, 100)
    paddles = [playerOne, playerTwo]
    ball = Ball((WIDTH//2 - 5 // 2, HEIGHT//2 - 5), 20, 20, speed=0.4)
    count = {
        'Red': Counter((255, 0, 0), (WIDTH // 3, 30)),
        'Blue': Counter((255, 0, 0), (WIDTH // 4 * 3, 30))
    }
    startTimer = Timer(5, (255, 255, 255))    
    gameEnded = Text((255, 255, 255), (WIDTH // 2, HEIGHT // 2))
    won = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill((0, 0, 0))
        startTimer.runTimer()
        if startTimer.timeout < 0:
            if not won:
                for key in count:
                    count[key].draw()        
                startTimer.runTimer()

                ball.draw(colorFromDistance((0, 0, 0), (0, 255, 0), distance(ball.position, (WIDTH//2, HEIGHT//2)), 450))
                ball.move()

                for paddle in paddles:
                    paddle.draw()
                    paddle.move()
                    if paddle.rect.colliderect(ball.rect):
                        ball.direction[0] *= -1
                        ball.position[0] += 5 * ball.direction[0]
            
                if ball.position[0] < 0:
                    count['Blue'] += 1
                    if count['Blue'] == 3:
                        won = 'Blue'
                    else:
                        ball.position = [WIDTH // 2, HEIGHT // 2]
                elif ball.position[0] > WIDTH:
                    count['Red'] += 1
                    if count['Red'] == 3:
                        won = 'Red'
                    else:
                        ball.position = [WIDTH // 2, HEIGHT // 2]
            else:
                gameEnded.render(f'{won} won!')

        pygame.display.update()

main()

        
