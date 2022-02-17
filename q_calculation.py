import math

def calculate_q(a, b, c, Pr, Pbh):
    Pr=Pr*10/0.980665
    Pbh=Pbh*10/0.980665
    c=-c+Pbh**2-Pr**2
    discr = a ** 2 - 4 * b * c

    if discr > 0:
        q1 = (-a+ math.sqrt(discr)) / (2 * b)
        q2 = (-a - math.sqrt(discr)) / (2 * b)
        if q1>=0:
            return q1
        else:
            return q2
    elif discr == 0:
        q = -a / (2 * b)
        if q>0:
            return q
    else:
        return print("Нет вещественного дебита")