import math
from typing import List

import pygame

from HexGrid import HexGrid


def get_color(idx, shade=125):
    return (shade * (idx % 3 == 0), shade * (idx % 3 == 1), shade * (idx % 3 == 2))


AXIAL_DIRECTIONS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]


class HexGridStorage(HexGrid):

    def __init__(self, screen_size, surface, rings):
        super().__init__(screen_size, int((screen_size[0] / 4) / rings), surface)
        self.rings = rings
        self.hover = None
        self.grid = [[0 for _ in range(rings * 2 + 1)] for _ in range(rings * 2 + 1)]
        self.set((0, 0), 1)
        self.fill = 1
        self.highlights = []
        self.hover_ring = False

    def draw(self):
        self.draw_storage()
        self.set_hover()
        if self.hover:
            if self.hover_ring:
                self.draw_hex_ring_hover(int(self.ring(self.hover)))
            else:
                self.draw_hover(self.hover)

        self.fill_hex(self.rings, (0, 0, 0), width=1)
        for highlight in self.highlights:
            self.draw_hex_axial((200, 0, 0), highlight, 3)

    def clear(self):
        self.grid = [[0 for _ in range(self.rings * 2 + 1)] for _ in range(self.rings * 2 + 1)]

    def draw_hover(self, coords, color=(100, 100, 100)):
        if self.get(coords):
            self.draw_hex_axial((100, 50, 50), coords)
        else:
            self.draw_hex_axial(color, coords)

    def draw_hex_ring_hover(self, dist):
        # s is dists
        for q in range(-dist, 0):
            r = -dist - q
            self.draw_hover((q, r))
        # s is -dist
        for r in range(0, dist):
            q = dist - r
            self.draw_hover((q, r))

        # r is dist
        for q in range(-dist + 1, 1):
            r = dist
            self.draw_hover((q, r))
        # r is -dist
        for q in range(0, dist):
            r = -dist
            self.draw_hover((q, r))

        # q is dist
        for r in range(-dist, 0):
            q = dist
            self.draw_hover((q, r))
        # q is -dist
        for r in range(1, dist + 1):
            q = -dist
            self.draw_hover((q, r))

    def draw_storage(self):
        for col in range(self.rings * 2 + 1):
            for row in range(self.rings * 2 + 1):
                if self.grid[col][row] == 1:
                    self.draw_hex_axial((50, 0, 0), self.storage_to_axial((col, row)))

    def storage_to_axial(self, coords):
        return coords[0] - self.rings, coords[1] - self.rings

    @staticmethod
    def static_storage_to_axial(coords, rings):
        return coords[0] - rings, coords[1] - rings

    def axial_to_storage(self, coords):
        return coords[0] + self.rings, coords[1] + self.rings

    @staticmethod
    def static_axial_to_storage(coords, rings):
        return coords[0] + rings, coords[1] + rings

    def set(self, coords, value):
        if self.ring(coords) <= self.rings:
            col, row = self.axial_to_storage(coords)
            self.grid[col][row] = value

    def get(self, coords):
        if self.ring(coords) <= self.rings:
            col, row = self.axial_to_storage(coords)
            return self.grid[col][row]

    def toggle(self, coords):
        if self.ring(coords) <= self.rings:
            col, row = self.axial_to_storage(coords)
            self.grid[col][row] = 1 if not self.grid[col][row] else 0

    def set_hover(self):
        coords = self.pixel_to_hex(pygame.mouse.get_pos())
        if self.ring(coords) <= self.rings:
            self.hover = coords
        else:
            self.hover = None

    def handle(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = self.pixel_to_hex(pygame.mouse.get_pos())
                self.fill = not self.get(coords)
                self.set(coords, self.fill)
            if event.type == pygame.MOUSEMOTION and any(pygame.mouse.get_pressed()):
                coords = self.pixel_to_hex(pygame.mouse.get_pos())
                self.set(coords, self.fill)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.clear()
                if event.key == pygame.K_j:
                    self.shift(0, 1)
                if event.key == pygame.K_n:
                    self.shift(5, 1)
                if event.key == pygame.K_b:
                    self.shift(4, 1)
                if event.key == pygame.K_g:
                    self.shift(3, 1)
                if event.key == pygame.K_y:
                    self.shift(2, 1)
                if event.key == pygame.K_u:
                    self.shift(1, 1)
                if event.key == pygame.K_SPACE:
                    self.scan()
                if event.key == pygame.K_HOME:
                    self.center()
                if event.key == pygame.K_r:
                    self.hover_ring = not self.hover_ring
                if event.key == pygame.K_LEFT:
                    self.rotate(True)
                if event.key == pygame.K_RIGHT:
                    self.rotate(False)

    def scan(self):
        self.highlights = [None, None, None, None, None, None]
        maxes = [-self.rings, -self.rings, -self.rings]
        mins = [self.rings, self.rings, self.rings]
        for col in range(self.rings * 2 + 1):
            for row in range(self.rings * 2 + 1):
                if self.grid[col][row] == 1:
                    q, r = self.storage_to_axial((col, row))
                    s = -(q + r)
                    if q > maxes[0]:
                        maxes[0] = q
                        self.highlights[0] = (q, r)
                    if q < mins[0]:
                        mins[0] = q
                        self.highlights[3] = (q, r)

                    if r > maxes[1]:
                        maxes[1] = r
                        self.highlights[1] = (q, r)
                    if r < mins[1]:
                        mins[1] = r
                        self.highlights[4] = (q, r)

                    if s > maxes[2]:
                        maxes[2] = s
                        self.highlights[2] = (q, r)

                    if s < mins[2]:
                        mins[2] = s
                        self.highlights[5] = (q, r)
        print(self.highlights)
        print("Q Max:%d R Max:%d S Max:%d" % tuple(maxes))
        print("Q Min:%d R Min:%d S Min:%d" % tuple(mins))

        directions = [(max_ + min_) for max_, min_ in zip(maxes, mins)]

        print(directions)
        vec1 = [2, 0, -2]  # Axis 0
        vec2 = [2, -2, 0]  # Axis 1

        v1_high = -math.ceil(directions[2] / vec1[2])
        v1_low = -math.floor(directions[2] / vec1[2])
        v2_high = -math.ceil(directions[1] / vec2[1])
        v2_low = -math.floor(directions[1] / vec2[1])
        print("v1 high:%d v1 low:%d v2 high:%d v2 low:%d" % (v1_high, v1_low, v2_high, v2_low))

        def calc(v1, v2):
            return [directions[i] + v2 * vec2[i] + v1 * vec1[i] for i in range(3)]

        def score(v1, v2):
            return max(map(abs, calc(v1, v2)))

        if v1_high != v1_low:
            if v2_high != v2_low:
                v1, v2 = min([(v1, v2) for v1 in [v1_low, v1_high] for v2 in [v2_low, v2_high]],
                             key=lambda v: score(v[0], v[1]))
            else:
                v2 = v2_high
                v1 = min([v1_low, v1_high], key=lambda v1: score(v1, v2))
        else:
            v1 = v1_high
            if v2_high != v2_low:
                v2 = min(v2_low, v2_high, key=lambda v2: score(v1, v2))
            else:
                v2 = v2_high
        print("v1:%d v2:%d" % (v1, v2))
        print("Score", calc(v1, v2))
        if not all(self.highlights):
            self.highlights = []

    def center(self):
        maxes = [-self.rings, -self.rings, -self.rings]
        mins = [self.rings, self.rings, self.rings]
        for col in range(self.rings * 2 + 1):
            for row in range(self.rings * 2 + 1):
                if self.grid[col][row] == 1:
                    q, r = self.storage_to_axial((col, row))
                    s = -(q + r)
                    if q > maxes[0]:
                        maxes[0] = q
                    if q < mins[0]:
                        mins[0] = q
                    if r > maxes[1]:
                        maxes[1] = r
                    if r < mins[1]:
                        mins[1] = r
                    if s > maxes[2]:
                        maxes[2] = s
                    if s < mins[2]:
                        mins[2] = s

        directions = [(max_ + min_) for max_, min_ in zip(maxes, mins)]

        print(directions)
        vec1 = [2, 0, -2]  # Axis 0
        vec2 = [2, -2, 0]  # Axis 1

        v1_high = -math.ceil(directions[2] / vec1[2])
        v1_low = -math.floor(directions[2] / vec1[2])
        v2_high = -math.ceil(directions[1] / vec2[1])
        v2_low = -math.floor(directions[1] / vec2[1])
        print("v1 high:%d v1 low:%d v2 high:%d v2 low:%d" % (v1_high, v1_low, v2_high, v2_low))

        def calc(v1, v2):
            return [directions[i] + v2 * vec2[i] + v1 * vec1[i] for i in range(3)]

        def score(v1, v2):
            return max(map(abs, calc(v1, v2)))

        if v1_high != v1_low:
            if v2_high != v2_low:
                v1, v2 = min([(v1, v2) for v1 in [v1_low, v1_high] for v2 in [v2_low, v2_high]],
                             key=lambda v: score(v[0], v[1]))
            else:
                v2 = v2_high
                v1 = min([v1_low, v1_high], key=lambda v1: score(v1, v2))
        else:
            v1 = v1_high
            if v2_high != v2_low:
                v2 = min(v2_low, v2_high, key=lambda v2: score(v1, v2))
            else:
                v2 = v2_high
        print("v1:%d v2:%d" % (v1, v2))
        print("Score", calc(v1, v2))
        self.shift(0, v1)
        self.shift(1, v2)

        # def scan(self):
        #     self.highlights = []
        #     maxes = []
        #     mins = []
        #     for dir_vec in AXIAL_DIRECTIONS:
        #         q_w, r_w = dir_vec
        #         s_w = -(q_w + r_w)
        #         max_ = None
        #         max_dist = 0
        #         for col in range(self.rings * 2 + 1):
        #             for row in range(self.rings * 2 + 1):
        #                 if self.grid[col][row] == 1:
        #                     q, r = self.storage_to_axial((col, row))
        #                     s = -(q + r)
        #                     dist = q * q_w + r * r_w + s * s_w
        #                     if max_dist < dist:
        #                         max_dist = dist
        #                         max_ = (q, r)
        #         if max_:
        #             self.highlights.append(max_)

    # def rebalance(self):
    #     done = False
    #     print("Start Balance")
    #     while not done:
    #         self.scores = [0, 0, 0, 0, 0, 0]
    #         for idx in range(len(AXIAL_DIRECTIONS)):
    #             q_w, r_w = AXIAL_DIRECTIONS[idx]
    #             s_w = -(q_w + r_w)
    #             max_dist = -self.rings
    #             for col in range(self.rings * 2 + 1):
    #                 for row in range(self.rings * 2 + 1):
    #                     if self.grid[col][row] == 1:
    #                         q, r = self.storage_to_axial((col, row))
    #                         s = -(q + r)
    #                         dist = (q * q_w + r * r_w + s * s_w) // 2
    #                         max_dist = max(max_dist, dist)
    #             self.scores[idx] = max_dist
    #
    #         # self.magnitudes = [ for idx in range(3)]
    #         idx = self.scores.index(max(self.scores, key=abs))
    #         magnitude = int(-(self.scores[idx] - self.scores[(idx + 3) % 6]) / 2)
    #         done = magnitude == 0
    #
    #         print(self.scores)
    #         print(AXIAL_DIRECTIONS[idx], magnitude, self.scores[idx], self.scores[(idx + 3) % 6])
    #
    #         if not done:
    #             self.shift(idx, magnitude)
    #     self.highlights = []
    #     print("Balanced")
    def rotate(self, clockwise=True):
        def get_rotated(coord):
            q, r = self.storage_to_axial(coord)
            if clockwise:
                coord = -r, (q + r)
            else:
                coord = (q + r), -q
            col, row = self.axial_to_storage(coord)
            return self.grid[col][row]

        self.grid = [[get_rotated((q, r)) if
                      self.ring(self.storage_to_axial((q, r))) <= self.rings else 0 for
                      r in
                      range(self.rings * 2 + 1)] for q in range(self.rings * 2 + 1)]

    def shift(self, direction, magnitude):
        q_shift, r_shift = AXIAL_DIRECTIONS[direction]
        q_shift *= magnitude
        r_shift *= magnitude
        self.grid = [[self.grid[q - q_shift][r - r_shift] if
                      self.ring(self.storage_to_axial(((q - q_shift), (r - r_shift)))) <= self.rings else 0 for
                      r in
                      range(self.rings * 2 + 1)] for q in range(self.rings * 2 + 1)]

    @staticmethod
    def static_shift(grid, direction, magnitude, rings):
        q_shift, r_shift = AXIAL_DIRECTIONS[direction]
        q_shift *= magnitude
        r_shift *= magnitude
        return [[grid[q - q_shift][r - r_shift] if
                 HexGridStorage.ring(
                     HexGridStorage.static_storage_to_axial(((q - q_shift), (r - r_shift)))) <= rings else 0
                 for
                 r in
                 range(rings * 2 + 1)] for q in range(rings * 2 + 1)]
