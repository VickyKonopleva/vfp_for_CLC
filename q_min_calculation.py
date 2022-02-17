import math


def calculate_q_min(fluids_props, Pbh, Tbh, z, tube, tubing_props):
    ro_liq=fluids_props["Плотность жидкости"]
    sigma=fluids_props['Поверхностное натяжение на границе "газ/жидкость"']
    # плотность газа на забое
    ro_gas_bh = fluids_props["Плотность газа при ст. ус."] * Pbh * 293.15 / (0.101325 * z * Tbh)
    # минимальная скорость на забое
    tochiginV = 3.3 * (9.81 * sigma * ro_liq ** 2 / (
                ro_gas_bh ** (2) * (ro_liq - ro_gas_bh))) ** 0.25
    d = tubing_props[tube]['Внутренний диаметр, м']
    # минимально дупостимый дебит на устье
    if tube == 'НКТ':
        d2 = tubing_props['ЦЛК']['Наружный диаметр, м']
        # мин дебит на устье для мкп площадь сечения другая
        tochiginQ = tochiginV * 3.1415926 * (d ** (2) / 4 - d2 ** (2) / 4 )* 86.4* Pbh * 293.15 / (0.101325 * z * Tbh)
    elif tube == 'ЦЛК':
        tochiginQ = tochiginV * 3.1415926 * d ** (2) / 4 * 86.4* Pbh * 293.15 / (0.101325 * z * Tbh)

    return tochiginQ
