import numpy as np
import labpy as lp


@lp.propagate_uncert
def kinetic_energy(m, v):
    return 0.5 * m * v ** 2


val1 = lp.Quantity(22.5, 0.1)  # kg
val2 = lp.Quantity(5.5, 0.01)  # m/s

ans = kinetic_energy(m=val1.v, v=val2.v)
print(f"{ans = }")

ans = kinetic_energy(m=val1, v=val2)
print(f"{ans = }")

val1 = lp.Quantity(np.linspace(1.5, 22.5, 100), np.ones(100) * 0.1)  # kg
val2 = lp.Quantity(np.linspace(1.5, 5.5, 100), np.ones(100) * 0.01)  # m/s

ans = kinetic_energy(m=val1, v=val2)
print(f"{ans = }")
