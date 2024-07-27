from numpy import random
from cg.cg import Draw


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

