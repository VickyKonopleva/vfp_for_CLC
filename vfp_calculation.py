from read_initial_data import read_data_from_excel
from z_calculation import calculate_z
from q_min_calculation import calculate_q_min
from q_calculation import calculate_q
from Pwh_calculation import calculate_Pwh
import numpy as np

# Считывание начальных данных
data=read_data_from_excel()

P_res=data.reservoir_props['Текущее пластовое давление']
Pbhmin=P_res-data.calc_props['Максимальная депрессия']
step_Pbh=data.calc_props['Шаг депрессии']
n=int((P_res-Pbhmin)//step_Pbh)

# массив со значениями забойного давления
Pbh=[Pbhmin+step_Pbh*i for i in range(n+1)]

# забойные давления по убыванию
# Pbh=Pbh[::-1]
Pmin=15000
# массив со значениями дебита
Q=[15, 20, 30, 50, 80, 110, 150, 180]
# массив со значениями обводненности
LGR=[0, 0.1, 0.5, 1, 1.5]

result=[]
res_NKT=[]


def define_vfp():
    # создание 3-х мерного массива обводненность(k)-забойное давление(i)-дебит(j)
    m=np.zeros(shape=(len(LGR), len(Pbh), len(Q)))
    # обнуление счетчика по обводненностям
    k = 0
    # ----------------------------------------------
    # цикл расчета устьевого давления для каждого из значений обводненности
    for lgr in LGR:
        # обнуление счетчика по забойныйм давлениям
        i = 0
        # ----------------------------------------------
        # цикл расчета устьевого давления для каждого из значений забойного давления при заданной обводненности
        for p in Pbh:
            # обнуление счетчика по дебитам
            j = 0
            # рассчет сверхсжимаемости
            z = calculate_z(p, data.reservoir_props["Пластовая температура"], data.fluids_props)
            # расчет минимального дебита по ЦЛК при текущем забойном (Точигин)
            q_min_ZLK = calculate_q_min(fluids_props=data.fluids_props, Pbh=p,
                                        Tbh=data.reservoir_props['Пластовая температура'],
                                        z=z,
                                        tube='ЦЛК', tubing_props=data.tubing_props)

            # расчет минимального дебита по МКП при текущем забойном (Точигин)
            q_min_NKT = calculate_q_min(fluids_props=data.fluids_props, Pbh=p,
                                        Tbh=data.reservoir_props['Пластовая температура'],
                                        z=z,
                                        tube='НКТ', tubing_props=data.tubing_props)
            # ----------------------------------------------
            # расчет суммарного дебита, исходя из текущего забойного давления
            # q = calculate_q(data.reservoir_props["Коэффициент фильрационных сопротивлений A (линейный)"],
            #                   data.reservoir_props["Коэффициент фильрационных сопротивлений (квадратичный)"],
            #                   data.reservoir_props["Поправочный коэффициент C0"],
            #                   data.reservoir_props["Текущее пластовое давление"],
            #                   p)

            #----------------------------------------------

            # цикл расчета устьевого давления для каждого из значений дебита при заданных обводненности и забойном давлении
            for q in Q:
                # эксплаутация только по МКП
                if q>q_min_NKT:
                    print(f"Скважина эксплуатируется только по МКП при Pbh={'%.2f' %p}МПа, т.к. Q({'%.2f' %q}тыс.м3/сут)>Qмкп(min)({'%.2f' %q_min_NKT}тыс.м3/сут)")
                    Pwh_nkt = calculate_Pwh(p, q, data.reservoir_props, data.fluids_props, "НКТ", data.tubing_props,
                                            data.calc_props, lgr)
                    # массив для вывода
                    result.append({"Труба": 'НКТ',
                                   "Pbh": '%.2f' % p,
                                   "Q": '%.2f' % q,
                                   "Pwh": '%.2f' % Pwh_nkt})

                    Pwh=Pwh_nkt

                # совместная эксплаутация по МКП и ЦЛК
                elif q>q_min_ZLK:
                    # расчет устьевого давления на ЦЛК
                    Pwh_zlk=calculate_Pwh(p, q_min_ZLK, data.reservoir_props, data.fluids_props, "ЦЛК", data.tubing_props, data.calc_props, lgr)
                    # расчет устьевого давления на МКП
                    Pwh_nkt = calculate_Pwh(p, q-q_min_ZLK, data.reservoir_props, data.fluids_props, "НКТ", data.tubing_props,
                                            data.calc_props, lgr)

                # сравнение устьевых и выбор минимального
                    if Pwh_zlk<Pwh_nkt:
                        tube='ЦЛК'
                        Pwh=Pwh_zlk

                    else:
                        tube='НКТ'
                        Pwh=Pwh_nkt

                    result.append({"Труба": tube,
                                   "Pbh":'%.2f' %p,
                                   "Q":'%.2f' % q,
                                   "Pwh":'%.2f' % Pwh})

                    # res_NKT.append({"Труба": 'НКТ',
                    #                "Pbh":'%.2f' %p,
                    #                "Q":'%.2f' % q,
                    #                "Pwh": '%.2f' % Pwh_nkt})
                # нерабочий режим
                else:
                    print(f"Нерабочий режим для забойного давления > {'%.2f' % p} МПа, т.к. Q({'%.2f' %q} тыс.м3/сут)<Qцлк(min)({'%.2f' %q_min_ZLK} тыс.м3/сут)")
                    break
                # заполнения массива встьевых давлений 
                m[k][i][j] = "%.2f" % Pwh
                # увеличение номера элемента в массиве дебитов
                j = j + 1
                # ----------------------------------------------
            # увеличение номера элемента в массиве забойных давлений
            i = i + 1
            # ----------------------------------------------
        # увеличение номера элемента в массиве обводненностей
        k = k + 1
        # ----------------------------------------------

    print(result)
    # print(m)
    vfp_res=[]
    # вывод vfp - таблицы
    for k in range(1, len(LGR)+1):
        vfp=[f'{i} 1 {k} 1 {str(m[k-1][i-1])}' for i in range(1, len(Pbh)+1)]
        vfp_res.append(vfp)
    print(vfp_res)



