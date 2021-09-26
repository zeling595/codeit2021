import logging
import json

from flask import request, jsonify

from codeitsuisse import app
import sys
import heapq

logger = logging.getLogger(__name__)

@app.route('/stock-hunter', methods=['POST'])
def evaluate_stock_hunter():
    data = request.get_json()
    logging.info("data length {}".format(len(data)))
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for test in data:
        dic = {}
        gridMap, minimumCost = solve_one_input(test)
        dic["gridMap"] = gridMap
        dic["minimumCost"] = minimumCost
        result.append(dic)
    # logging.info("result: {}".format(result))
    return jsonify(result)

def solve_one_input(input):
    # get all data
    entry_point = input['entryPoint']
    target_point = input['targetPoint']
    grid_depth = int(input['gridDepth'])
    grid_key = int(input['gridKey'])
    horizontal_stepper = int(input['horizontalStepper'])
    vertical_stepper = int(input['verticalStepper'])

    entry_x = int(entry_point['first'])
    entry_y = int(entry_point['second'])

    target_x = int(target_point['first'])
    target_y = int(target_point['second'])

    num_col = max(entry_x, target_x) + 1
    num_row = max(entry_y, target_y) + 1

    risk_level_array = [0 for j in range(num_col)]
    risk_level_map = [["" for j in range(num_col)] for i in range(num_row)]
    for i in range(num_row):
        for j in range(num_col):
            if i == 0 and j == 0:
                risk_index = 0
            elif i == 0:
                risk_index = j * horizontal_stepper
            elif j == 0:
                risk_index = i * vertical_stepper
            else:
                risk_index = risk_level_array[j] * risk_level_array[j - 1]
            
            # print("i: ", i)
            # print("j: ", j)
            # print("risk_index", risk_index)
            risk_level = calculate_risk_level(risk_index, grid_depth, grid_key)
            risk_level_array[j] = risk_level
            # risk_level_map[i][j] = risk_index
            risk_level_map[i][j] = get_risk_denotation(risk_level)

    cost = dijkstra((entry_y, entry_x), (target_y, target_x), num_row, num_col, risk_level_map)
    
    return risk_level_map, cost
    

def calculate_risk_level(risk_index, grid_depth, grid_key):
    risk_level = (risk_index + grid_depth) % grid_key
    # print("risk level: ", risk_level)
    return risk_level

def get_risk_denotation(risk_level):
    if risk_level % 3 == 0:
        # print("L")
        return "L"
    elif risk_level % 3 == 1:
        # print("M")
        return "M"
    else:
        # print("S")
        return "S"

def get_cost(s):
    if s == "L":
        return 3
    elif s == "M":
        return 2
    else:
        return 1


def get_min_point(q, relaxed_matrix):
    min = sys.maxsize
    min_ele = (-1, -1)
    for ele in q:
        if relaxed_matrix[ele[0]][ele[1]] < min:
            min = relaxed_matrix[ele[0]][ele[1]]
            min_ele = ele
    return min_ele

def dijkstra(src, target, num_row, num_col, matrix):
    
    # src [0,0]
    q = set()
    q.add(src)
    visited = set()

    relaxed_matrix = [[sys.maxsize for j in range(num_col)] for i in range(num_row)]
    relaxed_matrix[src[0]][src[1]] = 0

    while q:
        item = get_min_point(q, relaxed_matrix)
        q.remove(item)
        # print("item: ", item)
        curr_cell = item
        if curr_cell[0] == target[0] and curr_cell[1] == target[1]:
            # print(relaxed_matrix)
            return relaxed_matrix[target[0]][target[1]]
        visited.add(curr_cell)
        row = curr_cell[0]
        col = curr_cell[1]
        # up
        if row - 1 >= 0:
            p = (row - 1, col)
            if not p in visited:
                # print("p: ", p)
                if relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]]) < relaxed_matrix[p[0]][p[1]]:
                    relaxed_matrix[p[0]][p[1]] = relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]])
                    q.add(p)
                if not p in q:
                    q.add(p)
        # down
        if row + 1 < num_row:
            p = (row + 1, col)
            if not p in visited:
                # print("p: ", p)
                if relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]]) < relaxed_matrix[p[0]][p[1]]:
                    relaxed_matrix[p[0]][p[1]] = relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]])
                    q.add(p)
                if not p in q:
                    q.add(p)
        # left
        if col - 1 >= 0:
            p = (row, col - 1)
            if not p in visited:
                # print("p: ", p)
                if relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]]) < relaxed_matrix[p[0]][p[1]]:
                    relaxed_matrix[p[0]][p[1]] = relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]])
                    q.add(p)
                if not p in q:
                    q.add(p)
        # right
        if col + 1 < num_col:
            p = (row, col + 1)
            if not p in visited:
                # print("p: ", p)
                if relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]]) < relaxed_matrix[p[0]][p[1]]:
                    relaxed_matrix[p[0]][p[1]] = relaxed_matrix[curr_cell[0]][curr_cell[1]] + get_cost(matrix[p[0]][p[1]])
                    q.add(p)
                if not p in q:
                    q.add(p)
        # print("q: ", q)
        # print(relaxed_matrix)
    