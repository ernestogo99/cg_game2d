import pygame

from cg.cg import Color, Draw, Screen
from game.characters import Enemy, Spaceship, Bullet
from game.background import Background, Image


pygame.init()

FPS = 30
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600
screen = Screen(WIDTH, HEIGHT).display

GREEN = (0, 255, 0)
RED = (255, 0, 0)


def home_screen():
    window = [0, 0, 800, 600]
    viewport1 = [0, 0, 800, 600]
    viewport2 = [0, 0, 800, 600]

    windows = [window]
    viewports = [viewport1, viewport2]

    space = Background(windows, viewports)
    img = Image(windows, viewports, "spaceinvaders.png")

    color_filler = Color()

    screen.fill((0, 0, 0))
    img.draw(screen)
    space.draw(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    instructions()
                    return
                elif event.key == pygame.K_ESCAPE:  
                    running = False

        Draw.circumference(screen, 650, 500, 50, (255, 255, 255))  
        color_filler.flood_fill(
            screen,
            WIDTH,
            HEIGHT,
            650,
            500,
            (255, 165, 0),
            animation=False,
        )
        Draw.anti_alising_dda(screen, 50, 600, 250, 500, [0, 150, 255])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def instructions():
    window = [0, 0, 800, 600]
    viewport1 = [0, 0, 800, 600]
    viewport2 = [450, 0, 500, 55]

    windows = [window]
    viewports = [viewport1, viewport2]

    space = Background(windows, viewports)
    img = Image(windows, viewports, "instructions.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    py_invaders()
                    return
                elif event.key == pygame.K_ESCAPE:  
                    running = False

        screen.fill((0, 0, 0))
        img.draw(screen)
        space.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def py_invaders():
    # window and viewports
    window1 = [0, 0, 800, 600]
    window2 = [0, 0, 800, 600]
    viewport1 = [0, 0, 800, 600]

    viewport2 = [600, 0, 800, 100]

    windows = [window1, window2]
    viewports = [viewport1, viewport2]

    # deltaTime
    dt = 1

    # characters and background
    space = Background(windows, viewports)
    spaceship = Spaceship(windows, viewports)

    # enemies
    enemies = []

    # enemies bullets
    enemy_bullets = []
    enemy_cooldown = 0

    # spaceship bullets
    bullets = []
    spaceship_cooldown = 0

    # score
    score = 0
    enemies_score = 0

    running = True
    while running:
        if pygame.event.get(pygame.QUIT): running = False
        pygame.event.pump()

        keys = pygame.key.get_pressed()


        # movement
        if keys[pygame.K_a]:
            spaceship.move_left(dt)

        if keys[pygame.K_d]:
            spaceship.move_right(dt)


        # drawing
        screen.fill((0, 0, 0))
        space.draw(screen)
        spaceship.draw(screen)


        # generate enemies
        if len(enemies) < 1:
            enemies.append(Enemy(windows, viewports))

        for enemy in enemies:
            enemy.shoot = True
            enemy.move_down(dt)
            enemy.move(dt)
            enemy.draw(screen)
            if enemy.polygon.y_max() >= 600:
                enemies_score += 1
                enemies.pop(0)
                del(enemy)

        
        # enemies bullets
        enemy_cooldown += clock.get_time()
        if enemy_cooldown > 1700:
            enemy_cooldown = 0

        if  enemy_cooldown == 0:
            for enemy in enemies:
                x, _ = enemy.polygon.center()
                y = enemy.polygon.y_min()
                enemy_bullets.append(Bullet(x, y, RED))


        # check collision with enemy
        for enemy in enemies:
            if enemy.polygon.check_collision(spaceship.polygon):
                del(enemies)
                del(spaceship)
                del(bullets)
                del(enemy_bullets)
                game_over(score, enemies_score)
                return

            # check collision with enemy bullet
            if enemy_bullets:
                for enemy_bullet in enemy_bullets:
                    enemy_bullet.move_down()
                    if spaceship.polygon.check_collision(enemy_bullet.polygon):
                        del(enemies)
                        del(spaceship)
                        del(bullets)
                        del(enemy_bullets)
                        game_over(score, enemies_score)
                        return
                    else:
                        enemy_bullet.draw(screen)
                        if enemy_bullet.polygon.y_max() >= 600:
                            enemy_bullets.pop(0)
                            del(enemy_bullet)


        # spaceship bullets
        spaceship_cooldown += clock.get_time()
        if spaceship_cooldown > 1500:
            spaceship_cooldown = 0

        if keys[pygame.K_SPACE] and spaceship_cooldown == 0:
            x, _ = spaceship.polygon.center()
            y = spaceship.polygon.y_min()
            bullets.append(Bullet(x, y, GREEN))


        # spaceship bullets + enemies
        if bullets:
            for bullet in bullets:
                bullet.move_up()
                if enemies:
                    for enemy in enemies:
                        if enemy.polygon.check_collision(bullet.polygon):
                            bullets.pop(-1)
                            del(bullet)
                            enemies.pop(0)
                            del(enemy)
                            score += 1
                        else:
                            bullet.draw(screen)
                            enemy.draw(screen)
                            if bullet.polygon.y_min() <= 0:
                                bullets.pop(-1)
                                del(bullet)
                else:
                    bullet.draw(screen)
                    if bullet.polygon.y_min() <= 0:
                        bullets.pop(-1)
                        del(bullet)


        pygame.display.flip()
        dt = clock.tick(FPS)/1000


def game_over(score, enemies_score):
    window = [0, 0, 800, 600]
    viewport1 = [0, 0, 800, 600]
    viewport2 = [450, 0, 500, 55]

    windows = [window]
    viewports = [viewport1, viewport2]

    space = Background(windows, viewports)
    img = Image(windows, viewports, "game_over.png")

    print("\n --------------------------------------")
    print(f"\n Inimigos destruidos: {score}")
    print(f"\n Inimigos que passaram: {enemies_score}")
    print(f"\n Pontuação final: {score-enemies_score}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    py_invaders()
                    return
                elif event.key == pygame.K_ESCAPE:  
                    running = False
                    
        screen.fill((0, 0, 0))
        img.draw(screen)
        space.draw(screen)
       
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    home_screen()

