#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)

class Vec2d:
    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y
    def __add__(self, other):
        res = Vec2d(self.x + other.x, self.y + other.y)
        return res
    def __sub__(self, other):
        res = Vec2d(self.x - other.x, self.y - other.y)
        return res
    def __mul__(self, multiplyer):
        res = Vec2d(self.x * multiplyer, self.y * multiplyer)
        return res
    def len(self):
        return ((self.x ** 2 + self.y ** 2) ** 0.5)
    def int_pair(self):
        return ((self.x, self.y))

class Polyline:
    steps = 35
    width = 3
    color = pygame.Color(0)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def __init__(self):
        self.points = []
        self.speeds = []
    def addPoint(self, point : Vec2d, velocity : Vec2d):
        self.points.append(point)
        self.speeds.append(velocity)
    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].int_pair()[0] > SCREEN_DIM[0] or self.points[p].int_pair()[0] < 0:
                self.speeds[p] = Vec2d(- self.speeds[p].int_pair()[0], self.speeds[p].int_pair()[1])
            if self.points[p].int_pair()[1] > SCREEN_DIM[1] or self.points[p].int_pair()[1] < 0:
                self.speeds[p] = Vec2d(self.speeds[p].int_pair()[0], -self.speeds[p].int_pair()[1])
    def draw_points(self):
        for p in self.points:
            pygame.draw.circle(gameDisplay, (255, 255, 255), (int(p.int_pair()[0]), int(p.int_pair()[1])), self.width)

class Knot(Polyline):
    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn, self.steps))
        return res

    def set_points(self):
        super().set_points()
        self.get_knot()

    def draw_points(self):
        super().draw_points()
        points = self.get_knot()
        for p_n in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, self.color, (int(points[p_n].int_pair()[0]), int(points[p_n].int_pair()[1])), (int(points[p_n + 1].int_pair()[0]), int(points[p_n + 1].int_pair()[1])), self.width)

def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))



if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True
    polyline = Knot()

    hue = 0

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    polyline = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    polyline.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    polyline.steps -= 1 if polyline.steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                polyline.addPoint(Vec2d(*event.pos), Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        polyline.color.hsla = (hue, 100, 50, 100)
        polyline.draw_points()
        if show_help:
            draw_help()
        pygame.display.flip()
        if not pause:
            polyline.set_points()

    pygame.display.quit()
    pygame.quit()
    exit(0)
