#!/usr/local/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Aditya Marathe'

import numpy as np

import labpy as lp


@lp.propagate_errors
def kinetic_energy(m, v):
    return 0.5 * m * v ** 2


val1 = lp.Quantity(22.5, 0.1)  # kg
val2 = lp.Quantity(5.5, 0.01)  # m/s

ans = kinetic_energy(m=val1.val, v=val2.val)
print(f'{ans = :0.1f} J')

ans = kinetic_energy(m=val1, v=val2)
print('ans = ' + ans.get_string(units='J'))

val1 = lp.Quantity(np.linspace(1.5, 22.5, 100), np.ones(100) * 0.1)  # kg
val2 = lp.Quantity(np.linspace(1.5, 5.5, 100), np.ones(100) * 0.01)  # m/s

ans = kinetic_energy(m=val1, v=val2)
print('ans = ' + ans.get_string(units='J'))
