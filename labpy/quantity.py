#!/usr/local/bin/python
# -*- coding: utf-8 -*-

__all__ = ('Quantity',
           'NUM_ARR_TYPE',
           'DISPLAY_ITEM_LIMIT',
           'QuantityReassignmentError')
__version__ = '1.1'
__author__ = 'Aditya Marathe'

from typing import List
from typing import Tuple
from typing import Union

import numpy as np

# 3.10 Typing
# NUM_ARR_TYPE = int | float | list[int | float] | np.ndarray

NUM_ARR_TYPE = Union[int, float, List[Union[int, float]], np.ndarray]
DISPLAY_ITEM_LIMIT = 2

_SUPER_NUMS = list('⁰¹²³⁴⁵⁶⁷⁸⁹')


class QuantityReassignmentError(Exception):
    def __int__(self):
        super().__init__('Cannot reassign this variable.')


class Quantity:
    __slots__ = ('_val', '_err')

    def __init__(self,
                 val: NUM_ARR_TYPE,
                 err: NUM_ARR_TYPE
                 ):
        self._val = self._validate_input(val)
        self._err = self._validate_input(err)

        self._validate_types()
        self._validate_array()

    def relative_err(self) -> NUM_ARR_TYPE:
        return self.err / self.val

    @staticmethod
    def _round_to_sf(number: float, sf: int = 1) -> float:
        return float(f'%.{int(sf)}g' % number)

    @staticmethod
    def _get_scientific(number: float) -> Tuple[float, int]:
        value, _, exp = f'{number:E}'.rpartition('E')
        return float(value), int(exp)

    @staticmethod
    def _get_superscript(number: int) -> str:
        str_num = str(abs(number))
        for i in range(10):
            str_num = str_num.replace(str(i), _SUPER_NUMS[i])

        if abs(number) == number:
            sign = '\u207a'
        else:
            sign = '\u207b'

        return f'{sign}{str_num}'

    def _get_string(self, val, err) -> str:
        rounded_err = self._round_to_sf(err)
        rounded_err, err_order = self._get_scientific(rounded_err)
        output = f'({round(val, -err_order) / (10 ** err_order)} \xb1 {rounded_err})'
        if err_order:
            output += f' \u00d7 10{self._get_superscript(err_order)}'

        return output

    def get_string(self, units: str = '') -> str:
        if isinstance(self.val, float):
            return self._get_string(self.val, self.err) + ' ' + units

        output = '[\t'
        for i, val in np.ndenumerate(self.val[:DISPLAY_ITEM_LIMIT]):
            output += self._get_string(val, self.err[i]) + '\t'

        output += ' ... \t'
        for i, val in np.ndenumerate(self.val[-DISPLAY_ITEM_LIMIT:]):
            output += self._get_string(val, self.err[(-(i[0] + 1),)]) + '\t'

        return output + ' ]' + ' ' + units

    @staticmethod
    def _validate_input(input_) -> NUM_ARR_TYPE:
        if (isinstance(input_, int) or
                isinstance(input_, float)):
            return float(input_)

        elif isinstance(input_, list):
            return np.array(input_)

        elif isinstance(input_, np.ndarray):
            return input_

        raise TypeError('Expected input of type: int or float or numpy.ndarray. '
                        f'Got {type(input_).__name__} type instead.')

    def _validate_types(self) -> None:
        if not isinstance(self.val, type(self.err)):
            raise TypeError('Value and error must be of the same type. Got types '
                            f'`{type(self.val).__name__}` and `{type(self.err).__name__}`.')

    def _validate_array(self) -> None:
        if isinstance(self.val, np.ndarray):
            if self.val.shape != self.err.shape:
                raise ValueError('Both arrays must be of the same shape. '
                                 f'Got {self.val.shape} and {self.err.shape}.')

            try:
                self.val.shape[1]
            except IndexError:
                pass
            else:
                raise ValueError('Expected 1d NumPy array inputs. '
                                 f'Got {self.val.shape[1]}d array.')

    @property
    def val(self) -> NUM_ARR_TYPE:
        return self._val

    @property
    def err(self) -> NUM_ARR_TYPE:
        return self._err

    def __str__(self):
        return self.get_string()
