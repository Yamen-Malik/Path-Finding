import pygame
from enum import Enum

class NodeColors(Enum):
    text = pygame.Color("black")
    normal = pygame.Color("white")
    path = pygame.Color("magenta")
    start = pygame.Color("blue")
    end = pygame.Color("red")
    obstacle = pygame.Color("black")
    visited = pygame.Color("purple")
    cheking = pygame.Color("cyan")
