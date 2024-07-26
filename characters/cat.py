from cg.cg import Screen, Texture, TexturePolygon, Transformations


class Cat:

    def __init__(self, screen, windows, viewports) -> None:
        self.texture = Texture.import_texture("cat_cg.jpeg")
        self.polygon = TexturePolygon(
            [
                [100, 100, 0, 0],
                [100, 200, 0, 1],
                [200, 200, 1, 1],
                [200, 100, 1, 0]
            ]
        )
        self.windows = windows
        self.viewports = viewports
        self._draw(screen)


    def _draw(self, screen) -> None:
        pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[0])
        Texture.scanline_with_texture(screen, pol, self.texture)

        # pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[1])
        # Texture.scanline_with_texture(screen, pol, self.texture)

        # pol = Screen.mapping_window(self.polygon, self.windows[1], self.viewports[1])
        # Texture.scanline_with_texture(screen, self.polygon, self.texture)


    def rotate(self, ang, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_rotation(m, ang)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self._draw(screen)

    def move_right(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 10*dt, 0)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self._draw(screen)

    def move_left(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, -10*dt, 0)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self._draw(screen)

    def move_down(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, 10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self._draw(screen)

    def move_up(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, -10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self._draw(screen)

