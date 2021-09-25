import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluate_asteroid():
    data = request.get_json()['test_cases']
    logging.info("data length {}".format(len(data)))
    logging.info("data sent for evaluation {}".format(data))
    result = []
    # print(data)
    for test in data:
        dic = {}
        score, origin = calculate_score(test)
        dic["input"] = test
        dic["score"] = score
        dic["origin"] = origin
        result.append(dic)
    # logging.info("result: {}".format(result))
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
            # print("-----block_len: ", block_len)
            origin = i - block_len // 2
            # print("origin: ", origin)
            score = expand(origin, sizes, n, block_len)
            # print("score: ", score)
            if score > max_score:
                max_score = score
                optimal_origin = origin
            block_len = 1
    # last block
    # print("~~ last")
    # print("block_len: ", block_len)
    origin = n - 1 - block_len // 2
    score = expand(origin, sizes, n, block_len)
    if score > max_score:
        max_score = score
        optimal_origin = origin
    return max_score, optimal_origin

def expand(origin, sizes, n, block_len):
    # only odd block len enter
    num_destoryed = block_len
    score = get_score(num_destoryed)
    num_destoryed = 0
    if block_len % 2 == 0:
        left = origin - block_len // 2 + 1
    else:
        left = origin - block_len // 2
    right = origin + block_len // 2 

    while left > 0 and right < n - 1:
        # print("---while loop")
        # print("left: ", left)
        # print("right: ", right)
        # print("curr_size: ", curr_size)
        # print("num_destoryed: ", num_destoryed)
        if sizes[left - 1] == sizes[right + 1]:
            # count left
            left -= 1
            right += 1
            num_destoryed += 2
            while left > 0:
                if sizes[left] == sizes[left - 1]:
                    num_destoryed += 1
                    left -= 1
                else:
                    break
            # count right
            while right < n - 1:
                if sizes[right] == sizes[right + 1]:
                    num_destoryed += 1
                    right += 1
                else:
                    break
            score += get_score(num_destoryed)
            num_destoryed = 0
        else:
            score = get_score(block_len)
            return score
  
    return score

def get_multiplier(num):
    if num >= 10:
        return 2
    elif num >= 7:
        return 1.5
    else:
        return 1

def get_score(num):
    mul = get_multiplier(num)
    score = num * mul
    return score