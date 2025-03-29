
from math import floor, log10, pi

def sig_figs(x: float, precision: int):
    """
    Rounds a number to number of significant figures
    Parameters:
    - x - the number to be rounded
    - precision (integer) - the number of significant figures
    Returns:
    - float
    """

    x = float(x)
    precision = int(precision)
    if x == 0:
        return 0
    return round(x, -int(floor(log10(abs(x)))) + (precision - 1))

print(sig_figs(0, 4))