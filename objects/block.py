import pygame
from config import *
from numpy import array


class Block(pygame.sprite.Sprite):
    def __init__(self, position, size, color=WHITE) -> None:
        super().__init__()

        self.color = color
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = pygame.draw.rect(self.image, self.color, self.image.get_rect(), 1)
        self.rect.center = position

        self.position = array(position, dtype=float)  

    def draw(self, window):
        window.blit(self.image, self.rect)
        # pygame.draw.rect(window, self.color, self.image.get_rect())
