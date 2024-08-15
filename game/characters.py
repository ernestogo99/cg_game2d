import random
from cg.cg import Draw, Polygon, Screen, Texture, TexturePolygon, Transformations


RIGHT = 0
LEFT = 1


class Spaceship:
    def __init__(self, windows, viewports) -> None:
        self.texture = Texture.import_texture("spaceship.png")
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

        pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[1])
        Texture.scanline_with_texture(screen, pol, self.texture)

        pol = Screen.mapping_window(self.polygon, self.windows[1], self.viewports[1])
        Texture.scanline_with_texture(screen, self.polygon, self.texture)


    def rotate(self, ang) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_rotation(m, ang)
        self.polygon = Transformations.apply_transformation(self.polygon, m)


    def move_right(self, dt) -> None:
        limit_right = self.polygon.x_max() >= 780
        if not limit_right: 
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, 250*dt, 0)
            self.polygon = Transformations.apply_transformation(self.polygon, m)


    def move_left(self, dt) -> None:
        limit_left = self.polygon.x_min() <= 20
        if not limit_left:
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, -250*dt, 0)
            self.polygon = Transformations.apply_transformation(self.polygon, m)


    def move_down(self, dt) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, 10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)


    def move_up(self, dt) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, -10*dt)
        self.polygon = Transformations.apply_transformation(self.polygon, m)


class Enemy:
    def __init__(self, windows, viewports) -> None:
        self.texture = Texture.import_texture("enemy.png")
        x = random.randint(1, 799)
        self.polygon = TexturePolygon(
            [
                [x, 100, 0, 0],
                [x+70, 100, 1, 0],
                [x+70, 150, 1, 1],
                [x, 150, 0, 1],
            ]
        )
        self._move = RIGHT if random.randint(0, 1) == 0 else LEFT
        self.shoot = False
        self.windows = windows
        self.viewports = viewports


    def draw(self, screen) -> None:
        pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[0])
        Texture.scanline_with_texture(screen, pol, self.texture)

        pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[1])
        Texture.scanline_with_texture(screen, pol, self.texture)

        pol = Screen.mapping_window(self.polygon, self.windows[1], self.viewports[1])
        Texture.scanline_with_texture(screen, self.polygon, self.texture)


    def is_max_right(self):
        return self.polygon.x_max() == 800


    def is_max_left(self):
        return self.polygon.x_min() == 0


    def is_max_height(self):
        return self.polygon.y_max() == 600
    

    def is_min_height(self):
        return self.polygon.y_min() == 0


    def move(self, dt) -> None:
        if self._move == RIGHT:
            limit_right = self.polygon.x_max() >= 790
            if limit_right:
                self._move = LEFT
                self._move_left(dt)
            else:
                self._move_right(dt)
        elif self._move == LEFT:
            limit_left = self.polygon.x_min() <= 10
            if limit_left:
                self._move = RIGHT
                self._move_right(dt)
            else:
                self._move_left(dt)


    def _move_right(self, dt) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 100*dt, 0)
        self.polygon = Transformations.apply_transformation(self.polygon, m)


    def _move_left(self, dt) -> None:
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, -100*dt, 0)
        self.polygon = Transformations.apply_transformation(self.polygon, m)


    def move_down(self, dt) -> None:
        limit_down = self.polygon.y_max() == 600
        if not limit_down:
            m = Transformations.create_transformation_matrix()
            m = Transformations.compose_translation(m, 0, 100*dt)
            self.polygon = Transformations.apply_transformation(self.polygon, m)


class Bullet:
    def __init__(self, x, y, rgb) -> None:
        self.polygon = Polygon(
            [
                [x, y-2],
                [x+1, y-2],
                [x+1, y-1],
                [x, y-1]
            ]
        ) 
        self.color = rgb


    def draw(self, screen):
        Draw.draw_polygon(screen, self.polygon, self.color)


    def move_up(self):
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, -10)
        self.polygon = Transformations.apply_transformation(self.polygon, m)


    def move_down(self):
        m = Transformations.create_transformation_matrix()
        m = Transformations.compose_translation(m, 0, 10)
        self.polygon = Transformations.apply_transformation(self.polygon, m)
