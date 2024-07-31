from cg.cg import Draw, Screen, Texture, TexturePolygon, Transformations, Polygon


class Bullet:
    def __init__(self, x, y) -> None:
        self.polygon = Polygon(
            [
                [x, y-2],
                [x+1, y-2],
                [x+1, y-1],
                [x, y-1]
            ]
        ) 
        self.color = (0, 255, 0)

    def draw(self, screen):
        Draw.draw_polygon(screen, self.polygon, (5, 219, 0))

    def move(self):
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, -10)
        self.polygon = Transformations.apply_transformation(self.polygon, m)


class Cat:
    def __init__(self, windows, viewports) -> None:
        self.texture = Texture.import_texture("spaceship3_copy.png")
        self.polygon = TexturePolygon(
            [
                [400, 510, 0.5, 0],
                [360, 590, 0, 1],
                [440, 590, 1, 1],
            ]
        )
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

    def rotate(self, ang) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_rotation(m, ang)
        self.polygon = Transformations.apply_transformation(self.polygon, m)

    def move_right(self, dt) -> None:
        limit_right = self.polygon.x_max() == 800
        if not limit_right: 
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, 10*dt, 0)
            self.polygon = Transformations.apply_transformation(self.polygon, m)

    def move_left(self, dt) -> None:
        limit_left = self.polygon.x_min() == 0
        if not limit_left:
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, -10*dt, 0)
            self.polygon = Transformations.apply_transformation(self.polygon, m)

    def move_down(self, dt) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, 10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)

    def move_up(self, dt) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, -10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)

