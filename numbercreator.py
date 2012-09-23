# This Python file uses the following encoding: utf-8
import math
from operator import *
from sympy import simplify
import random
from collections import deque


CONSTANTS = {
    u'π': math.pi,
    u'e': math.e,
    u'g': 9.80665,
    u'ϕ': 1.61803398875,
    u'c': 299792458.0
}

OPERATORS = (mul, div, add, sub, pow)


def rewrite_number(target, tolerance=0.001, max_tries=100000):
    """
    Attempts to rewrite the target number in terms of the CONSTANTS
    and OPERATORS.  Tries to find a result within tolerance percent,
    but will increase if max_tries is hit.
    """
    combination = find_combination(target, tolerance, max_tries)
    result = eval_attempt(combination)
    output = print_combination(combination)
    try:
        return simplify(output), result
    except:
        return output, result


def eval_attempt(attempt_list):
    current = 1
    try:
        for pair in attempt_list:
            current = pair[1](current, pair[0][1])
    except:
        current = 0
    return current


def find_combination(target, tolerance, max_tries):
    target = float(target)
    queue = deque()
    num_tried = 0
    closest = ([], 1)
    for name, constant in random.sample(CONSTANTS.items(), len(CONSTANTS)):
        queue.append([((name, constant), mul)])

    while True:
        while queue and num_tried <= max_tries:
            num_tried += 1
            attempt = queue.popleft()
            result = eval_attempt(attempt)

            difference = abs((result - target) / target)
            if difference < closest[1]:
                closest = (attempt, difference)
            if difference < tolerance:
                break
            for name, constant in random.sample(CONSTANTS.items(), len(CONSTANTS)):
                for o in random.sample(OPERATORS, len(OPERATORS)):
                    queue.append(attempt + [((name, constant), o)])
        if num_tried >= max_tries:
            num_tried = 0
            tolerance *= 10
        else:
            break
    return closest[0]


def print_combination(combo):
    pmap = {mul: "*", div: "/", add: "+", sub: "-", pow: "^"}
    output = "%s" % combo.pop(0)[0][0]
    for step in combo:
        output = "(%s %s %s)" % (output, pmap[step[1]], step[0][0])
    return output
