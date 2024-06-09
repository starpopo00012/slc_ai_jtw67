import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (255, 0, 0)
BRICK_COLOR = (0, 255, 0)
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = PADDLE_COLOR
        self.speed = 7

    def move(self, keys):
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.left -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.right += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.color = BALL_COLOR
        self.speed = [5, -5]

    def move(self):
        self.rect.left += self.speed[0]
        self.rect.top += self.speed[1]

    def bounce(self, direction):
        if direction == 'horizontal':
            self.speed[0] = -self.speed[0]
        if direction == 'vertical':
            self.speed[1] = -self.speed[1]

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = BRICK_COLOR

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Breakout Game')
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30)
        self.ball = Ball(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS)
        self.bricks = [Brick(x * (BRICK_WIDTH + 10) + 35, y * (BRICK_HEIGHT + 10) + 35) for y in range(5) for x in range(10)]
        self.running = True

    def handle_collisions(self):
        # Ball collision with walls
        if self.ball.rect.left <= 0 or self.ball.rect.right >= SCREEN_WIDTH:
            self.ball.bounce('horizontal')
        if self.ball.rect.top <= 0:
            self.ball.bounce('vertical')
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.running = False  # Game over if the ball touches the bottom

        # Ball collision with paddle
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.bounce('vertical')

        # Ball collision with bricks
        hit_index = self.ball.rect.collidelist([brick.rect for brick in self.bricks])
        if hit_index != -1:
            hit_rect = self.bricks.pop(hit_index).rect
            if abs(self.ball.rect.bottom - hit_rect.top) < 10 and self.ball.speed[1] > 0:
                self.ball.bounce('vertical')
            elif abs(self.ball.rect.top - hit_rect.bottom) < 10 and self.ball.speed[1] < 0:
                self.ball.bounce('vertical')
            elif abs(self.ball.rect.right - hit_rect.left) < 10 and self.ball.speed[0] > 0:
                self.ball.bounce('horizontal')
            elif abs(self.ball.rect.left - hit_rect.right) < 10 and self.ball.speed[0] < 0:
                self.ball.bounce('horizontal')

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Move paddle
            keys = pygame.key.get_pressed()
            self.paddle.move(keys)

            # Move ball
            self.ball.move()

            # Handle collisions
            self.handle_collisions()

            # Drawing
            self.screen.fill(BG_COLOR)
            self.paddle.draw(self.screen)
            self.ball.draw(self.screen)
            for brick in self.bricks:
                brick.draw(self.screen)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
