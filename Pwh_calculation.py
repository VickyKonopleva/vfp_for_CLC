import math
from z_calculation import calculate_z
from lambda_calculation import calculaTe_lambda

def calculate_Pwh(Pbh, q, reservoir_props, fluids_props, tube, tubing_props, calculation_props, lgr):
    q=q/86.4
    L=tubing_props[tube]["Длина, м"]
    d=tubing_props[tube]["Внутренний диаметр, м"]
    Tbh=reservoir_props["Пластовая температура"]
    Twh=calculation_props["Температура окружающей среды"]
    n = int(L // 50)
    last_cell = L % 50
    pj = Pbh
    tj = Tbh
    a1 = 3.1934 / d - 16.666
    a2 = 6.1343 / d
    a3 = 0.119445 / d ** (8 / 3) + 0.000236
    a4 = 0.3553 / d ** (2) + 0.0014
    a5 = a3 * q ** (2 / 3) + a4
    fr2 = a1 * a5 + a2
    depth = L
    d = tubing_props[tube]['Внутренний диаметр, м']
    sigma=fluids_props['Поверхностное натяжение на границе "газ/жидкость"']
    liquid_density=fluids_props["Плотность жидкости"]

    # присвоение обычного и гидравлического диаметров в зависимости от того, по какой трубе расчет
    if tube == 'НКТ':
        d2 = tubing_props['ЦЛК']['Наружный диаметр, м']
        hd = d - d2
        LGR=0
        # LGR=fluids_props["Обводненность потока по МКП, м3/тыс. м3"]
    elif tube == 'ЦЛК':
        hd = d
        # LGR=fluids_props["Обводненность потока по ЦЛК, м3/тыс. м3"]
        LGR = lgr

    liquid_flowrate = q * LGR/1000

    for j in range(0, n+1):
        if j < n :
            dL = 50
        else:
            dL = last_cell
        zj = calculate_z(pj, tj, fluids_props)
        # пресчет дебита на поверхности на дебит газа в конкретной точке
        q_wc = q * zj * tj * 0.101325 / pj / 293.15
        # пересчет дебита жидкости по устьвому на конкретную точку
        liquid_flowrate=q_wc*LGR/1000
        lambda_coef = calculaTe_lambda(q_wc, pj, tj, fluids_props, tube, tubing_props, zj, liquid_flowrate, liquid_density)
        gas_density_wc = fluids_props["Плотность газа при ст. ус."] * pj / zj / tj * 293.15 / 0.101325
        # вычисление доли газа в водо-газовой смеси
        fi = q_wc / (q_wc + liquid_flowrate)
        # вычисление доли газа в водо-газовой смеси
        density_mix = gas_density_wc * fi + (1 - fi) * liquid_density
        # расчет скорости потока в зависимости от типа трубы
        if tube == 'НКТ':
            fluid_velocity = q_wc / (math.pi * (d ** (2) - d2 ** (2)) / 4)
        elif tube == 'ЦЛК':
            fluid_velocity = q_wc / (math.pi * d ** 2 / 4)
        gradP_el = density_mix * 9.81
        gradP_friction = lambda_coef *density_mix *fluid_velocity ** 2 / hd / 2
        gradP_liq = 9.6 * 2.52 * sigma ** (0.5) * liquid_density ** (0.5) * 9.81 ** (
                    1 / 6) / math.pi ** (2 / 3) * liquid_flowrate ** (2 / 3) / d ** (8 / 3)
        dP = (gradP_el + gradP_friction + gradP_liq) * dL
        pj = pj - dP * 10 ** (-6)
        t_loss = (Tbh - Twh) / L * dL
        tj = tj - t_loss
        depth = depth - dL
        # print(fluid_velocity, lambda_coef)
        # print(q_wc, zj, tj)
        # print(n,j, depth)
    return pj