import pygame

from constants import *

# def event_handler(running):
#     for e in pygame.event.get():
#         if e.type == pygame.QUIT:
#             running = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color("white"))

    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        pygame.display.flip()