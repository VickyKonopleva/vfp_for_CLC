import math
def calculate_z(P, T, fluids_props):
    a1 = 0.3265
    a2 = -1.07
    a3 = -0.5339
    a4 = 0.01569
    a5 = -0.05165
    a6 = 0.5475
    a7 = -0.7361
    a8 = 0.1844
    a9 = 0.1056
    a10 = 0.6134
    a11 = 0.721
    z1 = 0.4
    e = 1
    Tcr=fluids_props['Критическая температура газа']
    Pcr=fluids_props['Критическое давление газа']
    Tpr=T/Tcr
    Ppr=P/Pcr
    b1 = a1 + a2 / Tpr + a3 / Tpr ** (3) + a4 / Tpr ** (4) + a5 / Tpr ** (5)
    b2 = a6 + a7 / Tpr + a8 / Tpr ** (2)
    b3 = a9 * (a7 / Tpr + a8 / Tpr ** (2))
    k = 0.27 * Ppr / Tpr
    b4 = a10 / Tpr ** (3)
    b5 = a10 * a11 / Tpr ** (3)

    while e > 0.001:
        z = z1
        f = z - b1 * k / z - b2 * k ** (2) / z ** (2) + b3 * k ** (5) / z ** (5) - b4 * k ** (2) *math.exp(
            -a11 * k ** (2) / z ** (2)) / z ** (2) - b5 * k ** (4) * math.exp(-a11 * k ** (2) / z ** (2)) / z ** (4) - 1
        derF = 1 + b1 * k / z ** (2) + 2 * b2 * k ** (2) / z ** (3) - 5 * b3 * k ** (5) / z ** (6) - 2 * a11 * k ** (
            4) * b4 *math.exp(-a11 * k ** (2) / z ** (2)) / z ** (5) + 2 * b4 * k ** (2) *math.exp(-a11 * k ** (2) / z ** (2)) / z ** (
                   3) - 2 * a11 * b5 * k ** (6) *math.exp(-a11 * k ** (2) / z ** (2)) / z ** (7) + 4 * b5 * k ** (4) *math.exp(
            -a11 * k ** (2) / z ** (2)) / z ** (5)
        z1 = z - f / derF
        e = abs(z1 - z)
    return z1