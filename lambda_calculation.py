import math
from z_calculation import calculate_z

def calculaTe_lambda(q_wc, P, T, fluids_props, Tube, Tubing_props, z, liquid_flowrate, liquid_density):
    if q_wc == 0:
        lambda_coeff = 0
    else:
        molar_mass = fluids_props['Молярная масса газа']
        d = Tubing_props[Tube]['Внутренний диаметр, м']
        #проверка, по какому пространству считать потери
        if Tube=='НКТ':
            d2=Tubing_props['ЦЛК']['Наружный диаметр, м']
            hd = d-d2
            # скорость потока в рассматриваемой точке (v=v0/(ro/ro0)) для мкп площадь сечения другая 
            v = q_wc / (math.pi * (d ** (2)-d2 ** (2)) / 4)
        elif Tube=='ЦЛК':
            hd = d
            # скорость потока в рассматриваемой точке (v=v0/(ro/ro0))
            v = q_wc / (math.pi * d ** (2) / 4)
        e = Tubing_props[Tube]['Шероховатость, мм']/1000
        gas_spec_gravity = fluids_props['Плотность газа при ст. ус.'] / 1.2041

    
        T_fahr = (T - 273.15) * 9 / 5 + 32

        #плотность газа в столбе в рассматриваемой точке колонны
        density_G_wc = fluids_props['Плотность газа при ст. ус.'] * P * 293.15 / (0.101325 * z * T)
        if q_wc == 0 or liquid_flowrate==0:
            density_mix = density_G_wc
            spec_gravity=gas_spec_gravity
        else:
            fi = q_wc / (q_wc + liquid_flowrate)
            density_mix = density_G_wc * fi + (1 - fi) * liquid_density
            liquid_gas_mix_spec_gravity =density_mix*T/P*(0.101325/298.15)/1.2041
            spec_gravity=liquid_gas_mix_spec_gravity



        x = 2.57 + (1914.5 / T_fahr) + 0.275 * spec_gravity
        y = 1.11 + 0.04 * x
        k = (7.77 + 0.183 * spec_gravity) * (T_fahr + 460) ** (1.5) / (
                    122.4 + 373.6 * spec_gravity + T_fahr + 460) * 10 ** (-4)
        m = k * math.exp(x * (density_mix / 1000) ** (y)) * 10 ** (-3)
        #число Рейнольдса
        re = v * hd * density_mix / m
        # print(v, m, re, hd, density_mix)
        #расчет лямбда в зависимости от того, какая труба (для МКП числа Рейнольдса меньше и поэтому формула другая)
        if Tube=="ЦЛК":
            if re < 2320:
                # Зона гидравлически гладких труб
                lambda_coeff = 64 / re
            elif re < 6000:
                # формула Л.А.Вулиса - И.П.Гинзбурга для переходной зоны между ламинарным и турбулентным режимом
                gamma = 1 - math.exp(-0.002 * (re - 2320))
                lambda_coeff =  (64 / re * (1 - gamma) + 0.3164 / (re) ** 0.25 * gamma)
            elif re < 40000:
                # Формула Блазиуса 6000<re<40000
                lambda_coeff =  0.3164 / (re) ** 0.25

            elif re < 200000:
                # Формула Альтшуля 40000<re<200000
                lambda_coeff = 0.11 * (e / d + 68 / re) ** 0.25

            else:
                lambda_coeff = (-2 * math.log10(
                    2 * e / d / 3.7 - 5.02 / re * math.log10(2 * e / d / 3.7 - 13 / re))) ** (-2)

        elif Tube=="НКТ":
            # коэффициент kn учитывает кольцевое сечение трубы при эксплуатации по МКП
            kn=1.05
            if re<2320:
                # Зона гидравлически гладких труб
                lambda_coeff=64*kn/re
            elif re<6000:
                # формула Л.А.Вулиса - И.П.Гинзбурга для переходной зоны между ламинарным и турбулентным режимом
                gamma=1-math.exp(-0.002*(re-2320))
                lambda_coeff=kn*(64/re*(1-gamma)+0.3164/(re)**0.25*gamma)
            elif re<40000:
                # Формула Блазиуса 6000<re<40000
                lambda_coeff=kn*0.3164/(re)**0.25

            elif re<200000:
                # Формула Альтшуля 40000<re<200000
                lambda_coeff=kn*0.11*(e/d+68/re)**0.25

            else:
                lambda_coeff = kn*(-2 * math.log10(
                    2 * e / d / 3.7 - 5.02 / re * math.log10(2 * e / d / 3.7 - 13 / re))) ** (-2)



        # print(re, lambda_coeff)
    return lambda_coeff
