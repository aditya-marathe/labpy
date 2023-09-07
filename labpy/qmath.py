from typing import Dict as _Dict 
from typing import Any as _Any
from typing import Optional as _Optional
from typing import Callable as _Callable
from functools import wraps as _func_wrapper
import numpy as _np

from labpy.commons import NumArrType as _NumArrType
from labpy.commons import MathFuncType as _MathFuncType
from labpy.quantity import Quantity as _Quantity


def differentiate(func: _MathFuncType,
                  func_kwargs: _Dict[str, _NumArrType],
                  target_param: _Optional[str] = None,
                  delta: float = 1E-5) -> _NumArrType:
    """Calculates the derivative of a given mathematical function using numerical methods.

    Args:
    -----
    func: MathFuncType

    func_kwargs: Dict[str, NumArrType]

    target_param: Optional[str] = None

    delta: float = 1E-5

    Returns:
    --------

    Formulas Used:
    --------------
    Parital differentiation from first principles

    ( del f ) / ( del x ) = ( f(x + h, y, ...) - f(x, y, ...) ) / h

    The above applies for small h (approx. zero).

    In code, this translates to: func := f, {x, y, ...} := func_kwargs, x := target_param, h := delta

    """
    if target_param is None:
        target_param = next(iter(func_kwargs))

    # Evaluate the function at the specified coords.
    func_eval = func(**func_kwargs)

    # Add the small delta
    delta_func_kwargs = func_kwargs  # --> Note: No need to make a copy here
    delta_func_kwargs[target_param] += delta
    
    return (func(**delta_func_kwargs) - func_eval) / delta


def relative_uncert(quantity: _Quantity) -> _NumArrType:
    """Calculates the relative uncertainty of the given Quantity. If the value of the Quantity is zero, the function returns its absolute uncertainty instead.

    Args:
    -----
    quantity: Quantity
        Target Quantity object.

    Returns:
    --------
    NumArrType
        The relative uncertainty of the given Quantity.

    Formulas Used:
    --------------
    relative uncertainty := ( uncertainty ) / ( measured value )

    Notes:
    ------
    - NumArrType := Union[int, float, numpy.ndarray]
    """
    if quantity.value:  # --> Avoids ZeroDivisionError
        return quantity.uncertainty / quantity.value
    
    return quantity.uncertainty
    

def propagate_uncert(func: _MathFuncType, delta: float = 1E-5) -> _Callable[..., _Any]:
    @_func_wrapper(func)
    def wrapper(*args, **kwargs) -> _Quantity:
        # Validation and data extraction

        if args:
            raise TypeError("The decorated function only accepts keyword arguments.")

        values_dict: _Dict[str, _NumArrType] = dict()

        for (param_name, param_val) in kwargs.items():
            if isinstance(param_val, _Quantity):
                values_dict[param_name] = param_val.value
            elif isinstance(param_val, _NumArrType):
                values_dict[param_name] = param_val
            else:
                raise TypeError("Unknown type '%s' in argument '%s', expected a 'labpy.Quantity' or 'labpy.NumArrType'.", type(param_val).__name__, param_name)
            
        # Propagate uncertainties

        calc_value = func(**values_dict)
        partial_diffs_dict: _Dict[str, _NumArrType] = dict()

        for (param_name, param_val) in kwargs.items():
            if isinstance(param_val, _Quantity):
                partial_diffs_dict[param_name] = differentiate(func=func,
                                                               func_kwargs=values_dict,
                                                               target_param=param_name,
                                                               delta=delta)
            else:
                partial_diffs_dict[param_name] = 0.

        uncertainty_squared = 0

        for (param_name, partial_diff_val) in partial_diffs_dict.items():
            if _np.all(partial_diff_val) != 0:
                uncertainty_squared += (partial_diffs_dict[param_name] * kwargs[param_name].uncertainty)**2

        return _Quantity(val=calc_value, uncert=_np.sqrt(uncertainty_squared))

    return wrapper
