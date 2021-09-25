import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    data = request.get_json()['test_cases']
    logging.info("data sent for evaluation {}".format(data))
    result = []
    print(data)
    for test in data:
        dic = {}
        score, origin = calculate_score(test)
        dic["input"] = test
        dic["score"] = score
        dic["origin"] = origin
        result.append(dic)
    return jsonify(result)

def calculate_score(sizes):
    n = len(sizes)
    origin = 0
    block_len = 1
    max_score = 0
    optimal_origin = 0
    for i in range(n - 1):
        if sizes[i] == sizes[i + 1]:
            block_len += 1
        else:
            print("-----block_len: ", block_len)
            origin = i - block_len // 2
            print("i: ", i)
            print("origin: ", origin)
            block_len = 1
            score = expand(origin, sizes, n)
            print("score: ", score)
            if score > max_score:
                max_score = score
                optimal_origin = origin
    # last block
    print("~~ last")
    origin = n - 1 - block_len // 2
    score = expand(origin, sizes, n)
    print("score: ", score)
    if score > max_score:
        max_score = score
        optimal_origin = origin
    return max_score, optimal_origin

def expand(origin, sizes, n):
    score = 0
    num_destoryed = 1
    left = origin
    right = origin
    curr_size = sizes[origin]
    left_size = curr_size
    right_size = curr_size
    while left > 0 and right < n - 1:
        print("---while loop")
        print("left: ", left)
        print("right: ", right)
        print("curr_size: ", curr_size)
        print("num_destoryed: ", num_destoryed)
        if sizes[left] == curr_size:
            num_destoryed += 1
            left -= 1
        else:
            left_size = sizes[left]
            
        if sizes[right] == curr_size:
            num_destoryed += 1
            right += 1
        else:
            right_size = sizes[right]
        
        if left_size != curr_size and right_size != curr_size:
            multipler = get_multiplier(num_destoryed)
            score += num_destoryed * multipler
            if left_size == right_size:
                # continue destroy
                num_destoryed = 0
                curr_size = left_size
            else:
                # return res for this origin
                return score

    if left <= 0 and right < n - 1:
        while right < n - 1:
            if sizes[right] == curr_size:
                num_destoryed += 1
                right += 1
            else:
                break

    if left > 0 and right >= n - 1:
        while left > 0:
            if sizes[left] == curr_size:
                num_destoryed += 1
                left -= 1
            else:
                break
    
    multipler = get_multiplier(num_destoryed)
    score += num_destoryed * multipler
    return score

def get_multiplier(num):
    if num >= 10:
        return 2
    elif num >= 7:
        return 1.5
    else:
        return 1