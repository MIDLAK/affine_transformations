import pygame as pg
from matrix_functions import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        # начальная позиция камеры
        self.position = np.array([*position, 1.0])
        # нормализованныe векторa ориентации
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

        # вертикальная и горизонтальная области видимости камеры
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)

        # плоскости отсечения для камеры
        self.near_plane = 0.1
        self.far_plane = 100

        # скорость передвижения камеры
        self.moving_speed = 0.02 
        self.rotation_speed = 0.02

    def control(self):
        '''Перемещение (вращение) камеры по клавишам'''
        key = pg.key.get_pressed()

        # перемещение
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        # вращение
        if key[pg.K_LEFT]:
            self.control_rotate_y(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.control_rotate_y(self.rotation_speed)
        if key[pg.K_UP]:
            self.control_rotate_x(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.control_rotate_x(self.rotation_speed)

    def control_rotate_y(self, angle: float):
        '''Поворот камеры (векторов forward, right и up на угол angle) вокруг оси OY'''
        rotate = rotate_y(angle=angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def control_rotate_x(self, angle):
        '''Поворот камеры (векторов forward, right и up на угол angle) вокруг оси OX'''
        rotate = rotate_x(angle=angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def translate_matrix(self):
        '''Перемещение самеры в начало мировой системы координат'''
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
            ])

    def rotate_matrix(self):
        '''Правильное ориентирование камеры'''
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
            ])

    def camera_matrix(self):
        '''Правильное распложение камеры в пространстве'''
        return self.translate_matrix() @ self.rotate_matrix()
