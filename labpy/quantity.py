from labpy.commons import NumArrType as _NumArrType


class Quantity:
    """Quantity object contains the measured value with its absolute uncertainty.

    Args:
    -----
    val: NumArrType
        Measured value.
    
    uncert: NumArrType
        Absolute uncertainty associated with the measured value.

    Attrs:
    ------
    value / v: NumArrType
        Measured value.
    
    uncertainty / u: NumArrType
        Absolute uncertainty associated with the measured value.

    Notes:
    ------
    - NumArrType := Union[int, float, numpy.ndarray]
    """

    __slots__ = ["_val", "_uncert"]

    def __init__(self, 
                 val: _NumArrType, 
                 uncert: _NumArrType) -> None:
        self._val: _NumArrType = val
        self._uncert: _NumArrType = uncert

    # Alternative Inits

    @classmethod
    def deterministic_quantity(cls, value: _NumArrType) -> "Quantity":
        return cls(val=value, uncert=0.)

    # Getters

    @property
    def value(self) -> _NumArrType:
        return self._val
    
    @property
    def v(self) -> _NumArrType:
        return self._val
    
    @property
    def uncertainty(self) -> _NumArrType:
        return self._uncert
    
    @property
    def u(self) -> _NumArrType:
        return self._uncert
    
    # Other Dunders

    def __str__(self) -> str:
        return "Quantity {} \xb1 {}".format(self.value, self.uncertainty)
    
    def __repr__(self) -> str:
        return str(self)
