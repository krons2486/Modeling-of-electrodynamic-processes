import numpy as np
from scipy.special import spherical_jn, spherical_yn

class RCS:  
    def __init__(self, radius):
        self.radius = radius

    def calculate_rcs(self, frequency):
        wavelength = 3e8 / frequency
        k = 2 * np.pi / wavelength
        kr = k * self.radius

        def h_func(n, x):
            return spherical_jn(n, x) + 1j * spherical_yn(n, x)

        def a_func(n, kr):
            return spherical_jn(n, kr) / h_func(n, kr)

        def b_func(n, kr):
            b_numerator = kr * spherical_jn(n-1, kr) - n * spherical_jn(n, kr)
            b_denominator = kr * h_func(n-1, kr) - n * h_func(n, kr)
            return b_numerator / b_denominator

        result = 0
        for n in range(1, 30):
            term = ((-1) ** n) * (n + 0.5) * (b_func(n, kr) - a_func(n, kr))
            result += term

        return (wavelength ** 2 / np.pi) * (np.abs(result)**2)
