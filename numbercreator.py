# This Python file uses the following encoding: utf-8
import math
from operator import *
from sympy import simplify
import random
from collections import deque, namedtuple


Constant = namedtuple('Constant', ['symbol', 'value', 'fake_symbol'])
CONSTANTS = (
    Constant(u'π', math.pi, 'p'),
    Constant(u'e', math.e, 'e'),
    #Constant(u'g', 9.80665, 'g'),
    Constant(u'ϕ', 1.61803398875, 'f'),
    Constant(u'c', 299792458.0, 'c'),
)

Operator = namedtuple('Operator', ['operator', 'symbol'])
OPERATORS = (
    Operator(operator=mul, symbol="*"),
    Operator(operator=div, symbol="/"),
    Operator(operator=add, symbol="+"),
    Operator(operator=sub, symbol="-"),
    Operator(operator=pow, symbol="^"),
)

Step = namedtuple('Step', ['value', 'operator'])


def rewrite_number(target, tolerance=0.001, max_tries=10000):
    """
    Attempts to rewrite the target number in terms of the CONSTANTS
    and OPERATORS.  Tries to find a result within tolerance percent,
    but will increase if max_tries is hit.
    """
    exponent = 0
    if target < 0:
        negative = True
        target = -target
    else:
        negative = False
    while target > max([c.value for c in CONSTANTS]):
        target /= 100.0
        exponent += 2
    while target < min([c.value for c in CONSTANTS]):
        target *= 100.0
        exponent -= 2
    combination = find_combination(target, tolerance, max_tries)
    result = eval_steps(combination) * (10 ** exponent)
    result *= -1 if negative else 1
    output = print_combination(combination, exponent, negative)
    for constant in CONSTANTS:
        output = output.replace(constant.symbol, constant.fake_symbol)
    try:
        output = str(simplify(output))
        for constant in CONSTANTS:
            output = output.replace(constant.fake_symbol, constant.symbol)
    except:
        print 'Unable to simplify %s' % output
    output = output.replace('**', '^')
    return output, result


def eval_steps(attempt_list):
    current = 1
    try:
        for pair in attempt_list:
            current = pair.operator.operator(current, pair.value.value)
    except:
        current = 0
    return current


def find_combination(target, tolerance, max_tries):
    target = float(target)
    queue = deque()
    num_tried = 0
    closest = ([], 1)
    for constant in random.sample(CONSTANTS, len(CONSTANTS)):
        queue.append([Step(constant, Operator(mul, '*'))])

    while True:
        while queue and num_tried <= max_tries:
            num_tried += 1
            attempt = queue.popleft()
            result = eval_steps(attempt)

            difference = abs((result - target) / target)
            if difference < closest[1]:
                closest = (attempt, difference)
            if difference < tolerance:
                break
            if len(attempt) <= 4:
                for constant in random.sample(CONSTANTS, len(CONSTANTS)):
                    for o in random.sample(OPERATORS, len(OPERATORS)):
                        queue.append(attempt + [Step(constant, o)])
            num_tried = 0
            tolerance *= 10
        else:
            break
    return closest[0]


def print_combination(combo, exponent, negative):
    output = "%s" % combo.pop(0).value.symbol
    for step in combo:
        output = "(%s %s %s)" % (output, step.operator.symbol, step.value.symbol)

    if exponent:
        output = "(%s * 10 ^ %s)" % (output, exponent)
    if negative:
        output = "-%s" % output
    return output
