from typing import TypeAlias as _TypeAlias 
from typing import Union as _Union
from typing import Callable as _Callable
import numpy as _np


NumArrType: _TypeAlias = _Union[int, float, _np.ndarray]
MathFuncType: _TypeAlias = _Callable[..., NumArrType]
