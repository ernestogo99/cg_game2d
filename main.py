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


def run():
    cat = Cat()

    dt = 1

    cat.draw(screen)
    pygame.display.flip()

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # key commands
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cat.rotate(1, screen)

                if event.key == pygame.K_d:
                    cat.move_right(dt, screen)

                if event.key == pygame.K_a:
                    cat.move_left(dt, screen)

                if event.key == pygame.K_w:
                    cat.move_up(dt, screen)

                if event.key == pygame.K_s:
                    cat.move_down(dt, screen)

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()

