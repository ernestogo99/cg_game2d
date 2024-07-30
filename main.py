import pygame

from cg.cg import (Screen)
from characters.background import Background
from characters.cat import Bullet, Cat


pygame.init()

FPS = 30
clock = pygame.time.Clock()

width = 800
height = 600

screen = Screen(width, height).display


def run():
    # window = [0, 0, 1200, 1000]
    window = [0, 0, 800, 600]
    viewport1 = [0, 0, 800, 600]

    viewport2 = [450, 0, 500, 55]

    windows = [window]
    viewports = [viewport1, viewport2]

    space = Background(windows, viewports)
    cat = Cat(windows, viewports)

    dt = 1

    bullets = []
    cooldown = 0

    while True:
        if pygame.event.get(pygame.QUIT): break
        pygame.event.pump()

        keys = pygame.key.get_pressed()
        
        # movement
        if keys[pygame.K_w]:
            cat.move_up(dt)

        if keys[pygame.K_s]:
            cat.move_down(dt)

        if keys[pygame.K_a]:
            cat.move_left(dt)

        if keys[pygame.K_d]:
            cat.move_right(dt)

        screen.fill((0, 0, 0))
        space.draw(screen)
        cat.draw(screen)

        # bullets
        cooldown += clock.get_time()
        if cooldown > 200:
            cooldown = 0

        if keys[pygame.K_SPACE] and cooldown == 0:
            x, _ = cat.polygon.center()
            y = cat.polygon.y_min()
            bullets.append(Bullet(x, y))

        if bullets:
            for bullet in bullets:
                bullet.move(screen)
                if bullet.polygon.y_min() <= 0:
                    bullets.pop(0)
                    del(bullet)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    run()

