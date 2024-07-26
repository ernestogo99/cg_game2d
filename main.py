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
    window = [0, 0, 1200, 1000]
    # window = [0, 0, 500, 550]
    viewport1 = [0, 0, 500, 550]

    viewport2 = [450, 0, 500, 55]

    windows = [window]
    viewports = [viewport1, viewport2]

    cat = Cat(screen, windows, viewports)

    dt = 1

    while True:
        if pygame.event.get(pygame.QUIT): break
        pygame.event.pump()

        # move up/down by checking for pressed keys
        # and moving the paddle rect in-place
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            screen.fill((0,0,0))    
            cat.move_up(dt, screen)

        if keys[pygame.K_s]:
            screen.fill((0,0,0))    
            cat.move_down(dt, screen)

        if keys[pygame.K_a]:
            screen.fill((0,0,0))    
            cat.move_left(dt, screen)

        if keys[pygame.K_d]:
            screen.fill((0,0,0))    
            cat.move_right(dt, screen)

        if keys[pygame.K_SPACE]:
            screen.fill((0,0,0))    
            cat.rotate(dt, screen)

        pygame.display.flip()
        clock.tick(60)


    #         # key commands
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 cat.rotate(1, screen)
    #
    #             if event.key == pygame.K_d:
    #                 cat.move_right(dt, screen)
    #
    #             if event.key == pygame.K_a:
    #                 cat.move_left(dt, screen)
    #
    #             if event.key == pygame.K_w:
    #                 cat.move_up(dt, screen)
    #
    #             if event.key == pygame.K_s:
    #                 cat.move_down(dt, screen)
    #
    #     clock.tick(FPS)
    #     pygame.display.flip()
    #
    # pygame.quit()


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

