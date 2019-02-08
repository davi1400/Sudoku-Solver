#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import itemgetter
from numpy import where, array


# Se H é verdadeiro: Sorteia por saturação, se for falso por incidencia
def sorting(graph, color_dict, H=False):
    # Ordenar por saturacao
    if H:
        sat = dict()
        for v in graph.keys():
            sat.update({v: calculate_saturation_vertex(v, color_dict, graph)})
        sorted_x = sorted(sat.items(), key=itemgetter(1))
        return sorted_x[::-1]
    else:
        # ordenar por incidencia
        sat = dict()
        for v in graph.keys():
            sat.update({v: calculate_indence_vertex(v, color_dict, graph)})
        sorted_y = sorted(sat.items(), key=itemgetter(1))
        return sorted_y[::-1]


# retorna a quantidade de vizinhos coloridos
def calculate_indence_vertex(vertice, color, graph):
    neighbors = graph[vertice]
    count = 0
    for neighbor in neighbors:
        if color[neighbor] != 0:
            count += 1

    return count


# retorna a quantidade de cores diferentes nos vizinhos de um nó, se H é verdadeiro retorna o conjunto de cores jã usado
def calculate_saturation_vertex(vertice, color, graph, H=False):
    neighbors = graph[vertice]
    all_different_colors = list()
    for neighbor in neighbors:
        if color[neighbor] != 0 and (color[neighbor] not in all_different_colors):
            all_different_colors.append(color[neighbor])
    if H:
        return set(all_different_colors)

    return all_different_colors.__len__()


def create_all_blocks():
    # create blocks
    all_block = list()
    block1 = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    all_block.append(block1)
    del block1
    block2 = [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5)]
    all_block.append(block2)
    del block2
    block3 = [(0, 6), (0, 7), (0, 8), (1, 6), (1, 7), (1, 8), (2, 6), (2, 7), (2, 8)]
    all_block.append(block3)
    del block3
    block4 = [(3, 0), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2)]
    all_block.append(block4)
    del block4
    block5 = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)]
    all_block.append(block5)
    del block5
    block6 = [(3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8), (5, 6), (5, 7), (5, 8)]
    all_block.append(block6)
    del block6
    block7 = [(6, 0), (6, 1), (6, 2), (7, 0), (7, 1), (7, 2), (8, 0), (8, 1), (8, 2)]
    all_block.append(block7)
    del block7
    block8 = [(6, 3), (6, 4), (6, 5), (7, 3), (7, 4), (7, 5), (8, 3), (8, 4), (8, 5)]
    all_block.append(block8)
    del block8
    block9 = [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)]
    all_block.append(block9)
    del block9
    return all_block


def neighborhood(sudoku, line, column):  # O(n^2)

    neighbors = list()
    N_lines = sudoku.shape[0]
    N_columns = sudoku.shape[1]
    for k in range(N_columns):
        if (line, column) != (line, k):
            neighbors.append((line, k))
    for k in range(N_lines):
        if (line, column) != (k, column):
            neighbors.append((k, column))

    blocks = create_all_blocks()
    actual_block = list()
    for block in blocks:
        if (line, column) in block:
            actual_block = block.copy()
            break

    for i in actual_block:
        if i not in neighbors and i != (line, column):
            neighbors.append(i)

    return neighbors


def graph_generator(sudoku):  # O(n^2)
    color_dict = dict()
    Adj_list = dict()  # type:
    for line in range(sudoku.shape[0]):
        for column in range(sudoku.shape[1]):
            vizinhos = neighborhood(sudoku, line, column)
            Adj_list.update({(line, column): vizinhos})
            color_dict.update({(line, column): sudoku[line][column]})
    return Adj_list, color_dict


def get_color(v, sudoku):
    return sudoku[v[0]][v[1]]


def is_safe(c, vertice, graph, sudoku):
    neighbors = graph[vertice]
    all_different_colors = list()
    for neighbor in neighbors:
        if sudoku[neighbor[0]][neighbor[1]] != 0 and (sudoku[neighbor[0]][neighbor[1]] not in all_different_colors):
            all_different_colors.append(sudoku[neighbor[0]][neighbor[1]])
    if c not in all_different_colors:
        return True
    else:
        return False


def Back_coloring(sudoku, graph, i):
    if i == 81:
        return True
    Next_vertex = sorted(list(graph.keys()))[i]
    if len(sudoku == 0) == 0:
        return True
    if get_color(Next_vertex, sudoku) != 0:
        return Back_coloring(sudoku, graph, i + 1)

    for c in range(1, 10):

        if get_color(Next_vertex, sudoku) == 0:
            sudoku[Next_vertex[0]][Next_vertex[1]] = c

            if is_safe(c, Next_vertex, graph, sudoku):
                if Back_coloring(sudoku, graph, i + 1):
                    return True

            if len(sudoku == 0) == 0:
                return True

            sudoku[Next_vertex[0]][Next_vertex[1]] = 0

    return False


def sudoku_creator():
    sudoku = array([[0, 2, 0, 5, 0, 1, 0, 9, 0],
                    [8, 0, 0, 2, 0, 3, 0, 0, 6],
                    [0, 3, 0, 0, 6, 0, 0, 7, 0],
                    [0, 0, 1, 0, 0, 0, 6, 0, 0],
                    [5, 4, 0, 0, 0, 0, 0, 1, 9],
                    [0, 0, 2, 0, 0, 0, 7, 0, 0],
                    [0, 9, 0, 0, 3, 0, 0, 8, 0],
                    [2, 0, 0, 8, 0, 4, 0, 0, 7],
                    [0, 1, 0, 9, 0, 7, 0, 6, 0]])

    return sudoku


if __name__ == '__main__':
    sudoku = sudoku_creator()
    graph, color_dict = graph_generator(sudoku)
    if Back_coloring(sudoku, graph, 0):
        print('The solution was found: ')
        print(sudoku)
    else:
        print('Fail')