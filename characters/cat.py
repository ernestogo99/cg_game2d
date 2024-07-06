from cg.cg import Texture, TexturePolygon, Transformations


class Cat:

    def __init__(self) -> None:
        self.texture = Texture.import_texture("cat_cg.jpeg")
        self.polygon = TexturePolygon(
            [
                [100, 100, 0, 0],
                [100, 500, 0, 1],
                [500, 500, 1, 1],
                [500, 100, 1, 0]
            ]
        )

    def draw(self, screen) -> None:
        screen.fill((0, 0, 0))
        Texture.scanline_with_texture(screen, self.polygon, self.texture)

    def rotate(self, ang, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_rotation(m, ang)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self.draw(screen)

    def move_right(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 10*dt, 0)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self.draw(screen)

    def move_left(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, -10*dt, 0)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self.draw(screen)

    def move_down(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, 10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self.draw(screen)

    def move_up(self, dt, screen) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, -10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
        self.draw(screen)

