import pygame
from pygame import gfxdraw
import numpy as np
import time
from PIL import Image
import os


class Screen:
    def __init__(self, screen_width, screen_height) -> None:
        self.display = pygame.display.set_mode((screen_width, screen_height))

    def get_pixel(screen, x, y):
        color = screen.get_at((x, y))
        return (color[0], color[1], color[2], color[3])

    def get_pixel_with_texture(texture, x, y):
        num_rows, num_cols, _ = texture.shape

        x = max(min(x, 1), 0)
        y = max(min(y, 1), 0)

        x = int(x * (num_cols - 1))
        y = int(y * (num_rows - 1))

        color = texture[y][x]

        return (color[0], color[1], color[2])

    def mapping_window(polygon, window, viewport):
        initial_x_viewport = viewport[0]
        initial_y_viewport = viewport[1]
        final_x_viewport = viewport[2]
        final_y_viewport = viewport[3]

        initial_x_window = window[0]
        initial_y_window = window[1]
        final_x_window = window[2]
        final_y_window = window[3]

        a = (final_x_viewport - initial_x_viewport)/(final_x_window - initial_x_window)
        b = (final_y_viewport - initial_y_viewport)/(final_y_window - initial_y_window)

        matrix = np.array(
            [
                [a, 0, initial_x_viewport - a * initial_x_window],
                [0, b, initial_y_viewport - b * initial_y_window],
                [0, 0, 1],
            ]
        )

        return Transformations.apply_transformation(polygon, matrix)


class Transformations:
    def create_transformation_matrix():
        return np.identity(3)

    def compose_translation(matrix, tx, ty):
        return (
            np.array(
                [
                    [1, 0, tx],
                    [0, 1, ty],
                    [0, 0, 1]
                ]
            )
            @ matrix
        )

    def compose_scale(matrix, sx, sy):
        return (
            np.array(
                [
                    [sx, 0, 0],
                    [0, sy, 0],
                    [0, 0, 1]
                ]
            )
            @ matrix
        )

    def compose_rotation(matrix, ang):
        ang = (ang * np.pi)/180

        return np.array(
            [
                [np.cos(ang), -np.sin(ang), 0],
                [np.sin(ang), np.cos(ang), 0],
                [0, 0, 1]
            ]
            @ matrix
        )

    #bugando
    def compose_mirroring(matrix):
        return (
            np.array(
                [
                    [-1, 0, 0],
                    [0, -1, 0],
                    [0, 0, 1]
                ]
            )
            @ matrix
        )

    def compose_shear(matrix, cx, cy):
        return (
            np.array(
                [
                    [1, cx, 0],
                    [cy, 1, 0],
                    [0, 0, 1]
                ]
            )
            @ matrix
        )

    def apply_transformation(polygon, matrix):
        points = []

        for i in range(len(polygon.points)):
            pt = polygon.points[i][:2]
            pt.append(1)
            pt = np.transpose(pt)

            transformed_pt = matrix @ pt

            transformed_pt = np.transpose(transformed_pt)
            points.append(transformed_pt[:2].tolist())

            for j in range(2, len(polygon.points[i])):
                points[i].append(polygon.points[i][j])

        if type(polygon) is Polygon:
            return Polygon(points)
        return TexturePolygon(points)


class Polygon:
    def __init__(self, points=[]):
        self.points = points

    def insert_vertex(self, x, y):
        self.points.append([x, y])

    def y_min(self):
        return min(int(row[1]) for row in self.points)

    def y_max(self):
        return max(int(row[1]) for row in self.points)

    def center(self):
        x_sum = sum(row[0] for row in self.points)
        y_sum = sum(row[1] for row in self.points)
        num_points = len(self.points)

        center_x = int(x_sum / num_points)
        center_y = int(y_sum / num_points)

        return center_x, center_y

    def check_collision(self, rectangle):
        rect1_x1, rect1_y1, rect1_x2, rect1_y2 = self.get_rectangle_bounds()
        rect2_x1, rect2_y1, rect2_x2, rect2_y2 = rectangle.get_rectangle_bounds()

        return (
            rect1_x1 <= rect2_x2
            and rect1_x2 >= rect2_x1
            and rect1_y1 <= rect2_y2
            and rect1_y2 >= rect2_y1
        )

    def get_rectangle_bounds(self):
        x_coords = [point[0] for point in self.points]
        y_coords = [point[1] for point in self.points]

        x1 = min(x_coords)
        y1 = min(y_coords)
        x2 = max(x_coords)
        y2 = max(y_coords)

        return x1, y1, x2, y2


class TexturePolygon:
    def __init__(self, points=[]):
        self.points = points

    def insert_vertex(self, points):
        self.polygon += points

    def x_min(self):
        return min(int(row[0]) for row in self.points)

    def x_max(self):
        return max(int(row[0]) for row in self.points)

    def y_min(self):
        return min(int(row[1]) for row in self.points)

    def y_max(self):
        return max(int(row[1]) for row in self.points)

    def center(self):
        x_sum = sum(row[0] for row in self.points)
        y_sum = sum(row[1] for row in self.points)
        num_points = len(self.points)

        center_x = int(x_sum / num_points)
        center_y = int(y_sum / num_points)

        return center_x, center_y

    def check_collision(self, rectangle):
        rect1_x1, rect1_y1, rect1_x2, rect1_y2 = self.get_rectangle_bounds()
        rect2_x1, rect2_y1, rect2_x2, rect2_y2 = rectangle.get_rectangle_bounds()

        return (
            rect1_x1 <= rect2_x2
            and rect1_x2 >= rect2_x1
            and rect1_y1 <= rect2_y2
            and rect1_y2 >= rect2_y1
        )

    def get_rectangle_bounds(self):
        x_coords = [point[0] for point in self.points]
        y_coords = [point[1] for point in self.points]

        x1 = min(x_coords)
        y1 = min(y_coords)
        x2 = max(x_coords)
        y2 = max(y_coords)

        return x1, y1, x2, y2


class Draw:
    def set_pixel(screen, x, y, color):
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x >= screen.get_width():
            x = screen.get_width() - 1
        if y >= screen.get_height():
            y = screen.get_height() - 1

        gfxdraw.pixel(screen, x, y, color)

    def bresenham(screen, initial_x, initial_y, final_x, final_y, color):
        dx = final_x - initial_x
        dy = final_y - initial_y

        x_sign = 1 if dx > 0 else -1
        y_sign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = x_sign, 0, 0, y_sign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, y_sign, x_sign, 0

        dx2 = 2 * dx
        dy2 = 2 * dy

        p = dy2 - dx
        y = 0

        for x in range(dx):
            Draw.set_pixel(screen, initial_x + x * xx + y * yx, initial_y + x * xy + y * yy, color)

            if p >= 0:
                y += 1
                p -= dx2

            p += dy2

    def dda(screen, initial_x, initial_y, final_x, final_y, color):
        dx = final_x - initial_x
        dy = final_y - initial_y

        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)

        steps_x = dx/steps
        steps_y = dy/steps

        x = initial_x
        y = initial_y

        Draw.set_pixel(screen, round(x), round(y), color)

        for _ in range(int(steps)):
            x = x + steps_x
            y = y + steps_y
            Draw.set_pixel(screen, round(x), round(y), color)

    # TO DO: bugando
    def anti_alising_dda(screen, initial_x, initial_y, final_x, final_y, color):
        dx = final_x - initial_x
        dy = final_y - initial_y

        if abs(dx) > abs(dy):
            steps = abs(dx)
        else:
            steps = abs(dy)

        step_x = dx / steps
        step_y = dy / steps

        x = initial_x
        y = initial_y

        Draw.set_pixel(screen, int(x), int(y), color)

        for _ in range(1, steps + 1):
            x = x * step_x
            y = y * step_y

            if step_x == 1:
                prop = abs(y - int(y))
                Draw.set_pixel(screen, int(x), int(y), round((1 - prop) * color))
                Draw.set_pixel(screen, int(x), int(y + Draw.__sign(step_y)), round(prop * color))
            else:
                prop = abs(x - int(x))
                # bugando aqui
                Draw.set_pixel(screen, int(x), int(y), round((1 - prop) * color))
                Draw.set_pixel(screen, int(x), int(y + Draw.__sign(step_y)), round(prop * color))
    
    def draw_polygon(screen, polygon, color):
        for i in range(len(polygon.points) - 1):
            Draw.dda(screen, polygon.points[i][0], polygon.points[i][1], polygon.points[i + 1][0], polygon.points[i + 1][1], color)

        Draw.dda(screen, polygon.points[len(polygon.points) - 1][0], polygon.points[len(polygon.points) - 1][1], polygon.points[0][0], polygon.points[0][1], color)

    def circumference(screen, x_center, y_center, radius, color):
        c = Polygon()

        for angle in np.arange(0, 2 * np.pi, 0.25):
            c.insert_vertex(np.floor(x_center + radius * np.cos(angle)), np.floor(y_center + radius * np.sin(angle)))

        c.draw_polygon(screen, color)
        
    def __sign(x):
        if x < 0:
            return -1
        else:
            return 1


class Color:
    # TO DO: alterar
    def flood_fill(self, x, y, color, animation=False):
        initial_color = Color(Screen.get_pixel(x, y))

        if color == initial_color:
            return

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()

            if Color(Screen.get_pixel(x, y)) != initial_color:
                continue

            if animation:
                time.sleep(0.000001)
                pygame.display.update()

            Draw.set_pixel(x, y, color)

            if x + 1 < self.width:
                stack.append((x + 1, y))

            if x >= 1:
                stack.append((x - 1, y))

            if y + 1 < self.height:
                stack.append((x, y + 1))

            if y >= 1:
                stack.append((x, y - 1))

    # TO DO: alterar
    def boundary_fill(self, x, y, color, border_color=None):
        stack = [(x, y)]

        if not border_color:
            border_color = color

        while stack:
            x, y = stack.pop()

            color_aux = Color(Screen.get_pixel(x, y))

            if color_aux in [border_color, color]:
                continue

            Draw.set_pixel(x, y, color)

            if x + 1 < self.width:
                stack.append((x + 1, y))

            if x >= 1:
                stack.append((x - 1, y))

            if y + 1 < self.height:
                stack.append((x, y + 1))

            if y >= 1:
                stack.append((x, y - 1))

    def scanline_base(screen, polygon, color):
        y_min = polygon.y_min()
        y_max = polygon.y_max()

        for y in range(y_min, y_max + 1):
            intersections = []

            pix = polygon.points[0][0]
            piy = polygon.points[0][1]

            for p in range(1, len(polygon.points)):
                pfx = polygon.points[p][0]
                pfy = polygon.points[p][1]

                xi = Color.__intersection_base(y, [[pix, piy], [pfx, pfy]])

                if xi >= 0:
                    intersections.append(xi)

                pix = pfx
                piy = pfy

            pfx = polygon.points[0][0]
            pfy = polygon.points[0][1]

            xi = Color.__intersection_base(y, [[pix, piy], [pfx, pfy]])

            if xi >= 0:
                intersections.append(xi)

            for pi in range(0, len(intersections), 2):
                x1 = intersections[pi]
                x2 = intersections[pi + 1]

                if x2 < x1:
                    x1, x2 = x2, x1

                for xk in range(x1, x2 + 1):
                    Draw.set_pixel(screen, xk, y, color)

    def __intersection_base(y, segment):
        xi = segment[0][0]
        yi = segment[0][1]
        xf = segment[1][0]
        yf = segment[1][1]

            # Horizontal segment (has no intersection)
        if yi == yf:
            return -1

            # Secure starting point on top
        if yi > yf:
            xi, xf = xf, xi
            yi, yf = yf, yi

        t = (y - yi) / (yf - yi)

        return int(xi + t * (xf - xi)) if t > 0 and t <= 1 else -1


class Texture:
    def import_texture(img_name):
        cg_dir = os.getcwd()
        return np.asarray(Image.open(os.path.join(cg_dir, "resources", img_name)))

    def scanline_with_texture(screen, polygon, texture):
        y_min = polygon.y_min()
        y_max = polygon.y_max()

        for y in range(y_min, y_max + 1):
            intersections = []

            for p in range(len(polygon.points)):
                pi = polygon.points[p]
                pf = polygon.points[(p + 1) % len(polygon.points)]

                intersection = Texture.__intersection_with_texture(y, [pi, pf])

                if intersection[0] >= 0:
                    intersections.append(intersection)

            intersections.sort(key=lambda intersection: intersection[0])

            for pi in range(0, len(intersections), 2):
                p1 = intersections[pi]
                p2 = intersections[pi + 1]

                x1 = p1[0]
                x2 = p2[0]

                if x1 == x2:
                    continue

                if x2 < x1:
                    p1, p2 = p2, p1

                for xk in range(int(p1[0]), int(p2[0]) + 1):
                    pc = (xk - p1[0]) / (p2[0] - p1[0])

                    tx = p1[2] + pc * (p2[2] - p1[2])
                    ty = p1[3] + pc * (p2[3] - p1[3])

                    color = Screen.get_pixel_with_texture(texture, tx, ty)

                    Draw.set_pixel(screen, xk, y, color)

    def __intersection_with_texture(y, segment):
        pi = segment[0]
        pf = segment[1]

        # Horizontal segment (has no intersection)
        if pi[1] == pf[1]:
            return [-1, 0, 0, 0]

        # Secure starting point on top
        if pi[1] > pf[1]:
            pi, pf = pf, pi

        t = (y - pi[1]) / (pf[1] - pi[1])

        if t > 0 and t <= 1:
            x = pi[0] + t * (pf[0] - pi[0])

            tx = pi[2] + t * (pf[2] - pi[2])
            ty = pi[3] + t * (pf[3] - pi[3])

            return [x, y, tx, ty]

        return [-1, 0, 0, 0]

