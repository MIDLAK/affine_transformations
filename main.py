import pygame as pg
from camera import *
from projection import *
from object_3D import *

class Render:
    def __init__(self):
        '''Настройки Pygame'''
        pg.init()
        # разрешение
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900  
        # поверхность для отрисовки
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT //2    
        # желаемый FPS
        self.FPS = 60 
        # создание графического окна с разрешением RES
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        '''Создание экземпляра объекта'''
        # создание камеры и задание ей положения
        self.camera = Camera(self, [0.5, 1, -4])
        # созадние проекции и фигуры
        self.projection = Projection(self)
        self.object = Object3D(self)
        # для фигуры будет особое действие
        self.object.is_figure = True

        #действия над объектом
        self.object.translate(tx=0.2, ty=0.4, tz=0.2)
        #self.object.rotate_y(angle=math.pi/6)

        # создание локальной и мировой систем координат
        self.local_axes = Axes(self)
        #self.local_axes.translate(tx=0.7, ty=0.9, tz=0.7)
        center = np.mean(self.object.vertexes, axis=0)
        self.local_axes.translate(tx=center[0], ty=center[1], tz=center[2])
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        #self.world_axes.scale(1)
        self.world_axes.translate(tx=0.0001, ty=0.0001, tz=0.0001)

    def draw(self):
        '''Отрисовка'''
        # цвет фона окна
        self.screen.fill(pg.Color('darkslategray'))
        # отрисовка осей
        self.world_axes.draw()
        self.local_axes.draw()
        # отрисовка объекта
        self.object.draw()

    def run(self):
        '''Зацикливание приложения'''
        while True:
            self.draw()
            # возможность управления камерой
            self.camera.control()
            # проверка на выход из приложения
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            # отображение производительности
            pg.display.set_caption(str(self.clock.get_fps())) 
            # обновление экрана
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    app = Render()
    app.run()
