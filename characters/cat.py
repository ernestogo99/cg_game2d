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
        self.transf_matrix = Transformations.create_transformation_matrix()

    def show_cat(self, screen) -> None:
        Texture.scanline_with_texture(screen, self.polygon, self.texture)

    def rotate_cat(self, ang) -> None:
        self.transf_matrix = Transformations.compose_rotation(self.transf_matrix, ang)
        self.polygon = Transformations.apply_transformation(self.polygon, self.transf_matrix)

