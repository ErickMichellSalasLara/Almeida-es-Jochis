# Archivo donde se hara el proyecto
import pygame, random, numpy as np

WHITE = (255, 255, 255)

pygame.init()

size = (800, 600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    screen.fill(WHITE)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()