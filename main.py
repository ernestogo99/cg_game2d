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

screen = Screen.create_screen(500, 550)


def viewport_test():
    window_game = [0, 0, 500, 550]
    viewport_game = [0, 0, 500, 550]

    window_minimap = [0, 0, 450, 550]
    viewport_minimap = [450, 0, 500, 55]

    windows = [window_game, window_minimap]
    viewports = [viewport_game, viewport_minimap]

    cat = Cat(screen, windows, viewports)

    dt = 1

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
    viewport_test()
    # run()

