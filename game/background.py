from numpy import random
from cg.cg import Draw, Screen, Texture, TexturePolygon


class Star:
    def __init__(self) -> None:
        self.pos = []
        self.color = (255, 255, 255)
        for _ in range(150):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            self.pos.append(
                [
                    [x, y+1],
                    [x-1, y],
                    [x, y],
                    [x+1, y],
                    [x, y-1]
                ]
            )


class Background:
    def __init__(self, windows, viewports) -> None:
        self.stars = Star()
        self.windows = windows
        self.viewports = viewports


    def draw(self, screen) -> None:
        for star in self.stars.pos:
            for x, y in star:
                Draw.set_pixel(screen, x, y, self.stars.color)


class Image:
    def __init__(self, windows, viewports, nome_img) -> None:
        self.texture = Texture.import_texture(nome_img)
        # Obtendo a largura e altura da tela a partir do viewport
        screen_width = viewports[0][2]
        screen_height = viewports[0][3]

        # Definindo o TexturePolygon para preencher a tela
        self.polygon = TexturePolygon(
            [
                [0, 0, 0, 0],          # Canto superior esquerdo
                [0, screen_height, 0, 1],  # Canto inferior esquerdo
                [screen_width, screen_height, 1, 1], # Canto inferior direito
                [screen_width, 0, 1, 0]   # Canto superior direito
            ]
        )
        self.windows = windows
        self.viewports = viewports


    def draw(self, screen) -> None:
        pol = Screen.mapping_window(self.polygon, self.windows[0], self.viewports[0])
        Texture.scanline_with_texture(screen, pol, self.texture)
