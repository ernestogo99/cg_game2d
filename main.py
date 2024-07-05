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



pygame.init()

FPS = 30
clock = pygame.time.Clock()

screen = Screen.create_screen(600, 600)


cat_texture = Texture.import_texture("cat_cg.jpeg")
cat = TexturePolygon(
    [
        [100, 100, 0, 0],
        [100, 500, 0, 1],
        [500, 500, 1, 1],
        [500, 100, 1, 0]
    ]
)

transform_cat = Transformations.create_transformation_matrix()

value = 1

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                transform_cat = Transformations.compose_rotation(transform_cat, value)
                cat = Transformations.apply_transformation(cat, transform_cat)

    screen.fill((0, 0, 0))

    Texture.scanline_with_texture(screen, cat, cat_texture)

    clock.tick(FPS)
    pygame.display.update()

pygame.quit()

