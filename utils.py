import pygame
import numpy as np

def make_surface(size, color):
    """
    size, color로 surface를 생성합니다.
    """
    surf = pygame.Surface(size)
    surf.fill(color)
    return surf
