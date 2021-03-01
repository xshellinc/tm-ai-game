import random

import pygame
from pygame.locals import *
from detector import Detector


def load_choices():
    rock = pygame.image.load('rock.png').convert_alpha()
    paper = pygame.image.load('paper.png').convert_alpha()
    scissors = pygame.image.load('scissors.png').convert_alpha()

    return [rock, paper, scissors]

class Player:
    def __init__(self):
        self.detector = Detector('model_unquant.tflite', 'labels.txt')
        self.detector.start()
        self.choice = 0
        self.choices = load_choices()
        self.position = (128, 128)

    def show(self):
        self.choice = self.detector.get_result()
        return self.choice

    def draw(self, surface):
        if self.choice:
            surface.blit(self.choices[self.choice-1], self.position)

class Computer:
    def __init__(self):
        self.choice = 0
        self.choices = load_choices()
        self.position = (528, 128)

    def show(self, player_choice):
        if player_choice == 0:
            self.choice = 0
        else:
            self.choice = random.randint(1, 3)
        return self.choice

    def draw(self, surface):
        if self.choice:
            surface.blit(self.choices[self.choice-1], self.position)

class Scorer:
    def __init__(self):
        self.font = pygame.font.Font(None, 72)
        self.player_score = 0
        self.cpu_score = 0
        self.win = [(1, 3), (2, 1), (3, 2)]

    def judge(self, player_choice, cpu_choice):
        if player_choice == cpu_choice:
            return

        if (player_choice, cpu_choice) in self.win:
            self.player_score += 1
        else:
            self.cpu_score += 1

    def draw(self, surface):
        scores = f'{self.player_score} : {self.cpu_score}'
        text = self.font.render(scores, 1, (255, 255, 255))
        x = 400 - (text.get_rect().width / 2)
        surface.blit(text, (x, 10))


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((800, 400))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    pygame.draw.rect(background, (100, 100, 150), Rect(0, 0, 400, 400))
    pygame.draw.rect(background, (150, 100, 100), Rect(400, 0, 400, 400))

    screen.blit(background, (0, 0))
    pygame.display.update()

    player = Player()
    computer = Computer()
    scorer = Scorer()

    prev_choice = 0
    while True:
        clock.tick(8)

        player_choice = player.show()
        if player_choice != prev_choice:
            cpu_choice = computer.show(player_choice)
            scorer.judge(player_choice, cpu_choice)
            prev_choice = player_choice

        screen.blit(background, (0, 0))
        player.draw(screen)
        computer.draw(screen)
        scorer.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()

