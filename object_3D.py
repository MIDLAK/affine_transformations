import pygame as pg
from matrix_functions import *

import time

class Object3D:
    def __init__(self, render):
        self.render = render
        # вершины объекта
        #self.vertexes = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1,0 ,1), (1, 0, 0, 1), 
        #                          (0 ,0, 1, 1), (0, 1 ,1 ,1), (1 ,1 ,1 ,1), (1 ,0 ,1 ,1)])  
        #self.vertexes = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), 
        #                          (0 ,0, 1, 1), (0, 1, 1 ,1), (1 ,1 ,1 ,1), (1 ,0 ,1 ,1)])  

        # пиромида
        self.vertexes = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 0, 0, 1)])
        self.vertexes_orig = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 0, 0, 1)])
        self.faces = np.array([(0, 1, 2), (2, 1, 3), (3, 0, 1), (0, 2, 3)])

        self.is_figure = False

        # грани объекта, описанные по индексам вершин 
        #self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6),
        #                       (1, 2, 6, 5), (0, 3, 7, 4)])

        # мировая система координат
        self.font = pg.font.SysFont('Aria', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, True
        self.label = ''

    def draw(self):
        '''Отрисовка объекта'''
        self.screen_projection()
        self.movement()

    def movement(self):
        '''Постоянно выполняющееся действие над объетом'''
        if self.movement_flag:
            self.rotate_y(pg.time.get_ticks() % 0.005)
            if self.is_figure:
                self.rotate_center(pg.time.get_ticks() % 0.005)

    def screen_projection(self):
        # перенос вершин в пространство камеры
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        # перенос вершин в пространство отсечения
        vertexes = vertexes @ self.render.projection.projection_matrix
        # нормализация координат вершин
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        # зануление вершин, выходящих за область видимости
        vertexes[(vertexes > 1) | (vertexes < -1)] = 0 
        # преобразование для вывода на экран
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        # взятие осей OX и OY
        vertexes = vertexes[:, :2]

        # отображение граней
        # for face in self.faces:
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertexes[face]
            if not np.any((polygon == self.render.H_WIDTH) | 
                          (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, color, polygon, 3)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        # отображение вершин
        if self.draw_vertexes:
            for vertex in vertexes:
                if not np.any((vertex == self.render.H_WIDTH) | 
                              (vertex == self.render.H_HEIGHT)):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 3)

    def translate(self, tx=0.0, ty=0.0, tz=0.0):
        '''Перемещение объекта'''
        self.vertexes = self.vertexes @ translate(tx=tx, ty=ty, tz=tz)

    def scale(self, sx=0.0, sy=0.0, sz=0.0):
        '''Масштабирование объекта'''
        self.vertexes = self.vertexes @ scale(sx=sx, sy=sy, sz=sz)

    def rotate_center(self, angle: float):
        '''Вращение вокург геометрического цента фигуры'''
        # вычисление геом. цента.
        center = np.mean(self.vertexes, axis=0)
        # смещение в начало мировой системы координат
        world_translated_vertexes = self.vertexes - center
        # поворот на угол angle
        rotated_vertexes = world_translated_vertexes @ rotate_y(angle=angle)
        # обратное смещение координат к исходной точке
        final_rotated_vertexes = rotated_vertexes + center
        self.vertexes = final_rotated_vertexes

    def rotate_x(self, angle: float):
        '''Вращение вокруг оси OX на угол angle'''
        self.vertexes = self.vertexes @ rotate_x(angle=angle)

    def rotate_y(self, angle: float):
        '''Вращение вокруг оси OY на угол angle'''
        self.vertexes = self.vertexes @ rotate_y(angle=angle)

    def rotate_z(self, angle: float):
        '''Вращение вокруг оси OZ на угол angle'''
        self.vertexes = self.vertexes @ rotate_z(angle=angle)



class Axes(Object3D):
    '''Для оборажения осей координат'''
    def __init__(self, render):
        super().__init__(render)
        self.vertexes = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('white')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertexes = False
        self.label = 'XYZ'
