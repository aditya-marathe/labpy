# LabPy
###### Beta release (v1.0)

---

### Introduction

Hi! Let me give you a quick introduction to using this Python package. I have coded this package to be used in Physics labs, with the intention of creating tools to help Physics students during labs.

At the moment, this package only features an error (or uncertainty) propagation system. The idea behind creating this is very simple: I have created a function that allows me to modify a **decorated** function. Then, I have created a simple class which can hold a value with its associated error.

Please note that this release is for **Python 3.10** or above - may not work as expected on lower versions.

### How to use

#### Error propagation and Quantity

After downloading the package in your working directory, you can import the module like so:
```
import labpy

```

Next, create a code implementation of the **mathematical function** (must have integer, float or array type inputs and outputs) as shown below - make sure to include all the variables in the function parameters. Then above your function, add the `labpy.propagate_errors` decorator.

```
@labpy.propagate_errors
def kinetic_energy(m, v):
    """
    Calculates the kinetic energy.
    
    Params
    ------
    
        m: int | float | np.ndarray | Quantity
            Mass of the object.
        
        v: int | float | np.ndarray | Quantity
            Velocity of the object.
            
    Returns
    -------
        
        int | float | np.ndarray | Quantity: The kinetic energy of the object.
    
    """
    return 0.5 * m * v ** 2

```

The great thing about this is that, you can use the function as normal otherwise. The only thing you will need to remember to do is to **use keyword arguments only**! For example:

```
kinetic_energy(m=22.5, v=5.5)

```

Output: `340.3125`

Then, we can initialise two `labpy.Quantity` objects, which hold the value and uncertainty.

```
measured_mass = labpy.Quantity(22.5, 0.1)     # kg
measured_velocity = labpy.Quantity(5.5, 0.1)  # m/s
```

You can access the value and error stored in this class by `measured_mass.val` and `measured_mass.err` respectively.

Now, we can pass these to the function.

```
kinetic_energy(m=measured_mass, v=measured_velocity)
```

Output: `(340.0 ± 2.0)`

Notice that the output (string representation) has been rounded. The error, by convention, is rounded to one significant figure and the value is rounded to the same number of decimal places as the error. But, sometimes additional zeros might be missing from the value!

It is also possible, to pass a NumPy array like so:
```
import numpy as np

measured_mass = labpy.Quantity(np.linspace(1.5, 22.5, 100), np.ones(100) * 0.1)      # kg
measured_velocity = labpy.Quantity(np.linspace(1.5, 5.5, 100), np.ones(100) * 0.01)  # m/s

kinetic_energy(m=measured_mass, v=measured_velocity)

```

Output: `[ (17.0 ± 1.0) × 10⁻¹     (20.0 ± 1.0) × 10⁻¹      ...    (332.0 ± 2.0)   (340.0 ± 2.0)    ]`

Since the output is a `Quantity` you can still use `.val` and `.err` to get the value and its error!

**Quantity methods**:

1. `Quantity.relative_err()`: Calculates the relative error of the quantity.
2. `Quantity.get_string(units='')`: Returns the string representation of the quantity. It is also possible to specify the units.

### Limitations and future improvements
- The program can be slow - depends on the size of the input or number of parameters.
- Allow the use of non-keyword arguments for functions decorated with `propagate_err`.
- In `Quantity` class, make `_SUPER_NUMS` a class variable instead of an instance variable.
