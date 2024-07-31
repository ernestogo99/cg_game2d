import random
from cg.cg import Draw, Screen, Texture, TexturePolygon, Transformations


class Enemy:
    def __init__(self, windows, viewports) -> None:
        self.texture = Texture.import_texture("enemy.png")
        # self.polygon = TexturePolygon(
        #     [
        #         [350, 100, 0, 0],
        #         [420, 100, 1, 0],
        #         [420, 150, 1, 1],
        #         [350, 150, 0, 1],
        #     ]
        # )
        x = random.randint(0, 800)
        self.polygon = TexturePolygon(
            [
                [x, 100, 0, 0],
                [x+70, 100, 1, 0],
                [x+70, 150, 1, 1],
                [x, 150, 0, 1],
            ]
        )
        self.max_right = True
        self.windows = windows
        self.viewports = viewports

    def draw(self, screen) -> None:
        pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[0])
        Texture.scanline_with_texture(screen, pol, self.texture)
        # Draw.draw_polygon(screen, self.polygon, (1, 0, 255))

        # pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[1])
        # Texture.scanline_with_texture(screen, pol, self.texture)

        # pol = Screen.mapping_window(self.polygon, self.windows[1], self.viewports[1])
        # Texture.scanline_with_texture(screen, self.polygon, self.texture)

    def is_max_width(self):
        if self.polygon.x_max() == 800:
            self.max_left = True
            self.max_right = False
    
    def is_min_width(self):
        return self.polygon.x_min() == 0

    def is_max_height(self):
        return self.polygon.y_max() == 600

    def is_min_height(self):
        return self.polygon.y_min() == 0

    def rotate(self, ang) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_rotation(m, ang)
        self.polygon = Transformations.apply_transformation(self.polygon, m)

    def move_right(self, dt) -> None:
        limit_right = self.polygon.x_max() == 800
        if not limit_right: 
            self.max_right = False
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, 3*dt, 0)
            self.polygon = Transformations.apply_transformation(self.polygon, m)
        else:
            self.max_right = True

    def move_left(self, dt) -> None:
        limit_left = self.polygon.x_min() == 0
        if not limit_left:
            self.max_right = True
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, -3*dt, 0)
            self.polygon = Transformations.apply_transformation(self.polygon, m)
        else:
            self.max_right = False

    def move_down(self, dt) -> None:
        limit_down = self.polygon.y_max() == 600
        if not limit_down:
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, 0, 2*dt)
            self.polygon = Transformations.apply_transformation(self.polygon, m)

    def move_up(self, dt) -> None:
        limit_up = self.polygon.y_min() == 0
        if not limit_up:
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, 0, -3*dt)
            self.polygon = Transformations.apply_transformation(self.polygon, m)

