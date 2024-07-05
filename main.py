import pygame

from cg.cg import (
    Screen,
    Draw,
    Color,
    Texture,
    Polygon,
    TexturePolygon,
    Polygon,
    Transformations
)
from characters.cat import Cat



pygame.init()

FPS = 30
clock = pygame.time.Clock()

screen = Screen.create_screen(600, 600)

cat = Cat()

value = 1

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key commands
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                cat.rotate_cat(value)

    screen.fill((0, 0, 0))

    cat.show_cat(screen)

    clock.tick(FPS)

    pygame.display.update()

pygame.quit()

