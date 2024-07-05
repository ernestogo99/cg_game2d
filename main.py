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
screen = Screen(600, 600).screen


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
transform_cat = Transformations.compose_rotation(transform_cat, 10)

cat = Transformations.apply_transformation(cat, transform_cat)

Texture.scanline_with_texture(screen, cat, cat_texture)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()

