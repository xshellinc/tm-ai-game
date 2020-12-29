import random

from detector import Detector
import pygame


SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 24
GRID_WIDTH = SCREEN_WIDTH / GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)
        self.detector = Detector('model_unquant.tflite', 'labels.txt')
        self.detector.start()

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x*GRID_SIZE)) % SCREEN_WIDTH,
               (cur[1] + (y*GRID_SIZE)) % SCREEN_HEIGHT)

        if new in self.positions:
            self.reset()
            return 

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

#    def handle_directions(self):
#        for event in pygame.event.get():
#            if event.type != pygame.KEYDOWN:
#                continue
#
#            if event.key == pygame.K_UP:
#                self.turn(UP)
#            elif event.key == pygame.K_DOWN:
#                self.turn(DOWN)
#            elif event.key == pygame.K_LEFT:
#                self.turn(LEFT)
#            elif event.key == pygame.K_RIGHT:
#                self.turn(RIGHT)

    def handle_directions(self):
        result = self.detector.get_result()
        if result == 1:
            self.turn(UP)
        elif result == 2:
            self.turn(DOWN)
        elif result == 3:
            self.turn(LEFT)
        elif result == 4:
            self.turn(RIGHT)

    def turn(self, point):
        if self.length == 1:
            self.direction = point

        if self.direction != (point[0]*-1, point[1]*-1):
            self.direction = point

    def draw(self, screen):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.color, r)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE,
                         random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)

    def draw(self, screen):
        r = pygame.Rect((self.position[0], self.position[1]),
                        (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, r)


def draw_grid(screen):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE),
                                (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, (88, 211, 41), r)
            else:
                rr = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE),
                                 (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, (90, 173, 36), rr)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    snake = Snake()
    food = Food()
    while True:
        clock.tick(8)
        draw_grid(screen)
        snake.handle_directions()
        snake.move()
        
        if snake.get_head_position() == food.position:
            snake.length += 1
            food.randomize_position()

        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
