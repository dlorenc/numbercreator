numbercreator
=============

Library for making constants look awesome by writing them in terms of physical constants

Usage
-----
>>> from numbercreator import rewrite_number
>>> rewrite_number(17.8)
'((1 * g) + number of bits in a byte) = 17.81'

>>> rewrite_number(911, tolerance=0.1)
'((1 * e) * number of days in a year) = 992.172867388'