import pygame
from enum import Enum

class NodeColors(Enum):
    normal = pygame.Color("white")
    path = pygame.Color("magenta")
    start = pygame.Color("blue")
    end = pygame.Color("red")
    obstacle = pygame.Color("black")
    visited = pygame.Color("purple")
    cheking = pygame.Color("cyan")
class General(Enum):
    text = pygame.Color(237, 240, 255)
    info_text = pygame.Color(0, 122, 2)
