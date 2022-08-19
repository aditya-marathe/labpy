#!/usr/local/bin/python
# -*- coding: utf-8 -*-

__all__ = ('propagate_errors',
           'partial_derivative',
           'DELTA',
           'ARRAY_SIZE',
           'InvalidPropagateFunctionError')
__version__ = '1.1'
__author__ = 'Aditya Marathe'

from functools import wraps
from typing import Callable
from typing import Union
from typing import Dict

import numpy as np

from .quantity import *

DELTA = 0.1
ARRAY_SIZE = 100


class InvalidPropagateFunctionError(Exception):
    pass


def _pd_helper_func(
        f: Callable,
        **parameters
) -> Dict[str, float]:
    output = dict()
    for parameter, value in parameters.items():
        o_parameters = parameters.copy()
        o_parameters[parameter] = np.linspace(value - DELTA, value + DELTA, ARRAY_SIZE)
        dx = o_parameters[parameter][1] - o_parameters[parameter][0]
        output[parameter] = np.gradient(f(**o_parameters), dx)[ARRAY_SIZE // 2]

    return output


def partial_derivative(
        f: Callable,
        **parameters
) -> Dict[str, Union[float, list]]:
    _n_parameters = len(parameters)
    _parameter_names = list(parameters.keys())
    _parameter_values = list(parameters.values())

    # Validate inputs
    if not isinstance(f, Callable):
        raise TypeError('Invalid type passed to `f`. Expected a callable, '
                        f'but got a {type(f).__name__} type.')

    if not (_n_parameters > 0):
        raise TypeError(f'Missing function `parameters`.')

    # Calculation
    if isinstance(_parameter_values[0], np.ndarray):
        # Calculate the partial derivative: if NumPy array
        result = {key: [] for key in _parameter_names}
        for i in range(len(_parameter_values[0])):
            new_values = [value[i] for value in _parameter_values]
            new_parameters = dict(zip(_parameter_names, new_values))
            pd_result = _pd_helper_func(f, **new_parameters)
            for key in _parameter_names:
                result[key].append(pd_result[key])

        return result

    elif isinstance(_parameter_values[0], Union[int, float]):
        # Calculate the partial derivative: if number
        return _pd_helper_func(f, **parameters)

    raise TypeError('Invalid `parameter` types.')


def propagate_errors(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*a, **kw) -> Union[int, float, np.ndarray, Quantity]:
        if len(a):
            raise RuntimeError('Function only allows use of keyword arguments.')

        _kwarg_values = list(kw.values())

        if all(isinstance(val, Quantity) for val in _kwarg_values):
            quantity_values = dict()
            quantity_errors = dict()

            for q_name, q in list(kw.items()):
                quantity_values[q_name] = q.val
                quantity_errors[q_name] = q.err

            input_values = list(quantity_values.values())[0]
            output_values = f(**quantity_values)

            # Check for a reasonable output:
            # - f(num) -> num
            # - f(arr) -> arr

            if not isinstance(output_values, type(input_values)):
                raise InvalidPropagateFunctionError('Output type must match input type.')

            if isinstance(output_values, np.ndarray):
                input_shape = output_values.shape
                output_shape = input_values.shape
                if output_shape != input_shape:
                    raise InvalidPropagateFunctionError('Input and output array shapes do not match.'
                                                        f'Got: `input.shape = {input_shape}` and '
                                                        f'`output.shape = {output_shape}`.')

            # Calculations
            df_d = partial_derivative(f, **quantity_values)
            df_d_values = list(df_d.values())

            if isinstance(df_d_values[0], Union[list, np.ndarray]):
                list_of_squares = np.zeros(len(df_d_values[0]))
            else:
                list_of_squares = 0

            for var_name, var_value in list(df_d.items()):
                list_of_squares += (var_value * quantity_errors[var_name]) ** 2

            return Quantity(output_values, np.sqrt(list_of_squares))

        elif all(isinstance(val, Union[int, float, np.ndarray]) for val in _kwarg_values):
            return f(**kw)

    return wrapper
