from random import randint
from math import pi
import pygame
import numpy
import math
import os


def x_center_rectangle(x, lenght_arc):
    return x - lenght_arc / 2


def y_center_rectangle(y, height_arc):
    return y - height_arc / 2


def coordinate_creator_bombs(list_coordinate: list = [], number=10):
    for i in range(number):
        list_coordinate.append(randint(50, 950))
    return list_coordinate


def sizes_creator_bombs(list_size: list, number=10):
    for i in range(number):
        list_size.append(randint(10, 50))
    return list_size


class PacMan:

    def __init__(self, name, x_position, y_position, source_image, speed):
        self.name = name
        self.x_position = x_position
        self.y_position = y_position
        self.image = pygame.image.load(source_image)
        self.speed = speed

    def __del__(self):
        return None

    def print_it(self, screen):
        position = self.image.get_rect(center=(self.x_position, self.y_position))
        screen.blit(self.image, position)

    def move_right(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.x_position += self.speed

    def move_left(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.x_position -= self.speed

    def move_up(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.y_position -= self.speed

    def move_down(self):
        self.image = pygame.transform.flip(self.image, True, False)
        self.y_position += self.speed


class Bomb(PacMan):

    def __init__(self, name, x_position, y_position, source_image, speed=20):
        PacMan.__init__(self, name, x_position, y_position, source_image, speed)

    def print_it(self, screen):
        PacMan.print_it(self, screen)

    def move(self):
        self.x_position += randint(-self.speed, self.speed)
        self.y_position += randint(-self.speed, self.speed)


# Creator bombs
def set_bombs(number_of_bombs):
    list_bombs = []
    list_x_pos_bombs = []
    coordinate_creator_bombs(list_x_pos_bombs, number_of_bombs)
    list_y_pos_bombs = []
    coordinate_creator_bombs(list_y_pos_bombs, number_of_bombs)

    for i in range(number_of_bombs):
        list_bombs.append(Bomb(i, list_x_pos_bombs[i], list_y_pos_bombs[i], 'images'+os.sep+'bomb.png'))

    return list_bombs


# Algorithm calculation encounter two circle objects x, y - center coordinate, size - radius
def boom(first_x_pos, first_y_pos, first_size, second_x_pos, second_y_pos, second_size):
    list_edge_circle_x = []
    list_edge_circle_y = []
    booms = False
    for i in numpy.arange(0, 2 * pi, 2 * pi / 360):
        x = first_x_pos + first_size * math.cos(i)
        y = first_y_pos - first_size * math.sin(i)  # Minus because we have rotated y coordinate
        list_edge_circle_x.append(x)
        list_edge_circle_y.append(y)

    for i in range(len(list_edge_circle_x)):
        if ((list_edge_circle_x[i] - second_x_pos)**2) + ((list_edge_circle_y[i] - second_y_pos)**2) <= second_size**2:
            booms = True

    return booms







