import math
import cv2 as cv
import numpy as np


def InCircle(point, center, radius):
    '''
    Проверяет, лежит ли точка point в окружности с центром center, радиусом radius
    :param point, center: Пары целых чисел
    :param radius: Целое число
    :return: boolean значение
    '''
    if (point[0] - center[0]) ^ 2 + (point[1] - center[1]) ^ 2 <= radius ^ 2:
        return True
    return False


def Inter(line1, line2):
    """
    Находит точку пересечения line1 и line2
    :param line1, line2: ndarray с shape(1,2)
    :return: Массив из 2 целых чисел
    """
    r1, f1 = line1[0]
    r2, f2 = line2[0]
    matrix = np.array([
        [np.cos(f1), np.sin(f1)],
        [np.cos(f2), np.sin(f2)]
    ])
    b = np.array([[r1], [r2]])
    if np.linalg.det(matrix) == 0:
        return -1
    x, y = np.linalg.solve(matrix, b)
    return int(np.round(x)), int(np.round(y))


def Allintersect(lines, graph):
    """
    Находит пересечения со всеми линиями, попарно перебирая их
    :param lines: Массив параметров прямых
    :param graph: Исходная картинка
    :return: Массив из пар координат всех найденных точек пересечений
    """

    intersect = []

    for first in range(lines.shape[0] - 1):
        for second in range(first + 1, lines.shape[0]):
            tmp = Inter(lines[first], lines[second])
            if tmp != -1 and 0 <= tmp[0] < graph.shape[0] and 0 <= tmp[1] < graph.shape[1]:
                intersect.append(tmp)
    return intersect


def PrepareGraph(file_name):
    '''
    Считывает png, проводит преобразование Хафа, находит прямые
    :param file_name: Название считываемого файла с графом
    :return: Массив с параметрами прямых
    '''
    graph = cv.imread(file_name, 0)
    dst = cv.Canny(graph, 50, 200)
    lines = cv.HoughLines(dst, 1, math.pi / 180.0, 45, np.array([]), 0, 0)
    return Allintersect(lines, graph)


def CountInter(intersect):
    '''
    :param intersect: Массив, состоящий из точек пересечения
    :return: Количество скоплений точек пересечения
    '''
    counter = 0
    while len(intersect) != 0:
        counter += 1
        used = [False] * len(intersect)
        used[0] = True
        for j in range(1, len(intersect)):
            if InCircle(intersect[0], intersect[j], 20):
                used[j] = True
        new_points = []
        for j in range(len(intersect)):
            if not used[j]:
                new_points.append(intersect[j])
        intersect = new_points
    return counter


file_name, vert_number = input().split()
intersect = PrepareGraph(file_name)
print(CountInter(intersect) - int(vert_number))
