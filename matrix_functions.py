import math
import numpy as np

def translate(tx=0.0, ty=0.0, tz=0.0) -> np.ndarray:
    '''Матрица перемещения'''
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [tx, ty, tz, 1],
        ])

def rotate_x(angle: float) -> np.ndarray:
    '''Матрица поворота на угол angle вокруг оси OX'''
    return np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle), math.sin(angle), 0],
        [0, -math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1],
        ])

def rotate_y(angle: float) -> np.ndarray:
    '''Матрица поворота на угол angle вокруг оси OY'''
    return np.array([
        [math.cos(angle), 0, -math.sin(angle), 0],
        [0, 1, 0, 0],
        [math.sin(angle), 0, math.cos(angle), 0],
        [0, 0, 0, 1],
        ])

def rotate_z(angle: float) -> np.ndarray:
    '''Матрица поворота на угол angle вокруг оси OZ'''
    return np.array([
        [math.cos(angle), math.sin(angle), 0, 0],
        [-math.sin(angle), math.cos(angle), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        ])

def scale(sx=0.0, sy=0.0, sz=0.0) -> np.ndarray:
    '''Матрица масштабирования вдоль осей OX, OY и OZ на коэф-ты sx, sy и sz'''
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1],
        ])

