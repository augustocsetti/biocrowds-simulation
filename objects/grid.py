import pygame
from config import *
from numpy import array


class Grid(pygame.sprite.Sprite):
    def __init__(self, position, size) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.position = array(position)
        self.image = pygame.Surface((size, size))
        self.rect = pygame.draw.rect(self.image, WHITE, self.image.get_rect(), 1)

        self.rect.topleft = self.position * size

    def draw(self, window):
        window.blit(self.image, self.rect)
