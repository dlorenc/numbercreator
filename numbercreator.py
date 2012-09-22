import math
from operator import *
from collections import deque

CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'g': 9.81,
    'golden ratio': 1.618,
    'number of bits in a byte': 8.0,
    'number of days in a year': 365.0,
    'c': 299792458.0
}

OPERATORS = (mul, div, add, sub, pow)


def rewrite_number(target, tolerance=0.001, max_tries=100000):
    """
    Attempts to rewrite the target number in terms of the CONSTANTS
    and OPERATORS.  Tries to find a result within tolerance percent,
    but will increase if max_tries is hit.
    """
    combination = find_combination(target, tolerance, max_tries)
    return print_combination(combination)


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
    for name, constant in CONSTANTS.items():
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
            for name, constant in CONSTANTS.items():
                for o in OPERATORS:
                    queue.append(attempt + [((name, constant), o)])
        if num_tried >= max_tries:
            num_tried = 0
            tolerance *= 10
        else:
            break
    return closest[0]


def print_combination(combo):
    pmap = {mul: "*", div: "/", add: "+", sub: "-", pow: "^"}
    output = "1"
    for step in combo:
        output = "(%s %s %s)" % (output, pmap[step[1]], step[0][0])
    return "%s = %s" % (output, eval_attempt(combo))
