import pygame


def get_color(idx, shade=125):
    return (shade * (idx % 3 == 0), shade * (idx % 3 == 1), shade * (idx % 3 == 2))


class HexGrid:
    def __init__(self, screen_size, radius, surface):
        self.screen_size = screen_size
        self.radius = radius
        self.surface = surface

    def draw_hex(self, color, coords, width=0):
        x, y = coords
        x = x * 2 * self.radius + self.screen_size[0] / 2
        y = -y * 2 * self.radius + self.screen_size[1] / 2
        top = (x, y - self.radius)
        bottom = (x, y + self.radius)
        top_left = (x - self.radius, y - self.radius / 2)
        bottom_left = (x - self.radius, y + self.radius / 2)
        top_right = (x + self.radius, y - self.radius / 2)
        bottom_right = (x + self.radius, y + self.radius / 2)
        pygame.draw.polygon(self.surface, color, [top, top_right, bottom_right, bottom, bottom_left, top_left],
                            width=width)

    def fill_square(self):
        for x in range(-int((self.screen_size[0] / 2) // (self.radius * 2)) - 1,
                       int((self.screen_size[0] / 2) // (self.radius * 2)) + 1):
            for y in range(-int(self.screen_size[1] // (self.radius * 2) * 4 / 3),
                           int(self.screen_size[1] // (self.radius * 2) * 4 / 3)):
                self.draw_hex([0, 0, 0], [x + (y % 2) * 0.5, y * 0.75], width=1)

    def pointy_hex_to_pixel(self, coords):
        q, r = coords
        x = int(self.radius * (2 * q + r) + self.screen_size[0] / 2)
        y = int((self.radius * 1.5) * r + self.screen_size[1] / 2)
        return (x, y)

    def pixel_to_hex(self, coords):
        x, y = coords
        r = round((y-self.screen_size[1] / 2)/(1.5*self.radius))

        q = round((2 * x - self.screen_size[0] - 2 * self.radius * r) / (4 * self.radius))
        return (q, r)

    @staticmethod
    def dist(coords1, coords2):
        q1, r1 = coords1
        s1 = -(q1 + r1)
        q2, r2 = coords1
        s2 = -(q2 + r2)
        return (abs(q1 - q2) + abs(r1 - r2) + abs(s1 - s2)) / 2

    @staticmethod
    def ring(coords):
        q, r = coords
        s = -(q + r)
        return (abs(q) + abs(r) + abs(s)) / 2

    def fill_hex_axial(self):
        for q in range(-5, 6):
            for r in range(-5, 6):
                self.draw_hex_axial(get_color(q + 2 * r), (q, r))

    def fill_hex(self, dist, color=(0, 0, 0), width=1):
        for d in range(dist + 1):
            self.draw_hex_ring(d, color, width)

    def draw_hex_ring(self, dist, color, width=0):
        # s is dists
        for q in range(-dist, 0):
            r = -dist - q
            self.draw_hex_axial(color, (q, r), width)
        # s is -dist
        for r in range(0, dist):
            q = dist - r
            self.draw_hex_axial(color, (q, r), width)

        # r is dist
        for q in range(-dist + 1, 1):
            r = dist
            self.draw_hex_axial(color, (q, r), width)
        # r is -dist
        for q in range(0, dist):
            r = -dist
            self.draw_hex_axial(color, (q, r), width)

        # q is dist
        for r in range(-dist, 0):
            q = dist
            self.draw_hex_axial(color, (q, r), width)
        # q is -dist
        for r in range(1, dist + 1):
            q = -dist
            self.draw_hex_axial(color, (q, r), width)

    def draw_hex_axial(self, color, coords, width=0):
        # print("%d, %d" % (coords[0], coords[1]))
        x, y = self.pointy_hex_to_pixel(coords)
        top = (x, y - self.radius)
        bottom = (x, y + self.radius)
        top_left = (x - self.radius, y - self.radius / 2)
        bottom_left = (x - self.radius, y + self.radius / 2)
        top_right = (x + self.radius, y - self.radius / 2)
        bottom_right = (x + self.radius, y + self.radius / 2)
        pygame.draw.polygon(self.surface, color, [top, top_right, bottom_right, bottom, bottom_left, top_left],
                            width=width)
