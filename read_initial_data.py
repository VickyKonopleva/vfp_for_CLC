import pandas


class Data():
    def __init__(self):
        self.tubing_props = 0
        self.reservoir_props = 0
        self.fluids_props = 0
        self.rocks_props = 0
        self.calc_props = 0

def read_data_from_excel():
    #чтение исходных данных из excel-файла (колонны) формат:  {'Эксплутационная колонна': {'Внутренний диаметр, м': 0.199, 'Наружный диаметр, м': 0.219, 'Длина, м': 1241.0, 'λ': '-', 'Шероховатость, мм': 0.01}, 'НКТ': {'Внутренний диаметр, м': 0.15, 'Наружный диаметр, м': 0.168, 'Длина, м': 1142.18, 'λ': 0.0001, 'Шероховатость, мм': 0.02}, 'ЦЛК': {'Внутренний диаметр, м': 0.051, 'Наружный диаметр, м': 0.06, 'Длина, м': 1141.9, 'λ': 0.001, 'Шероховатость, мм': 0.02}}
    data_df = pandas.read_excel('Initial data.xlsx', sheet_name='Колонны',index_col=0)
    tubing_data_dict=data_df.to_dict('index')

    # #чтение исходных данных из excel-файла (характеристики пласта) формат: {'Середина интервала перфорации': 1136.0, 'Пластовая температура': 302.15, 'Текущее пластовое давление': 1.68, 'Коэффициент фильрационных сопротивлений A (линейный)': 0.0, 'Коэффициент фильрационных сопротивлений (квадратичный)': 0.007292468920470378, 'Поправочный коэффициент C0': 0.0}
    data_df = pandas.read_excel('Initial data.xlsx', sheet_name='Характеристики пласта', header=None, index_col=0)
    reservoir_data_dict=data_df.to_dict()[1]

    #чтение исходных данных из excel-файла (Характеристики флюидов) формат {'Критическая температура газа': 191.0, 'Критическое давление газа': 4.7, 'Плотность газа при ст. ус.': 0.56, 'Молярная масса газа': 16.04, 'Средняя теплоемкость газа по стволу, ккал/(кг∙°К)': 0.538, 'Среднее значение коэффициента Джоуля-Томпсона, °К/(кгс/см2)': 0.51, 'Плотность жидкости': 1000.0, 'Поверхностное натяжение на границе "газ/жидкость"': 0.07286, 'Обводненность потока по МКП, м3/тыс. м3': 0.0, 'Обводненность потока по ЦЛК, м3/тыс. м3': 0.0}
    data_df = pandas.read_excel('Initial data.xlsx', sheet_name='Характеристики флюидов', header=None, index_col=0)
    fluids_data_dict=data_df.to_dict()[1]

    #чтение исходных данных из excel-файла (Характеристики окружающих г.п.) формат {'Глубина подошвы ММП, м': 425.0, 'Теплоемкость пород ММП, ккал/(м3∙°К)': 0.000358509, 'Средняя теплопроводность пород ММП, ккал/(м∙ч∙°К)': 1.2, 'Глубина нейтрального слоя, м': 10.0, 'Температура нейтрального слоя, °К': 272.15, 'Теплоемкость горных пород ниже ММП, ккал/(м3∙°К)': 700.0, 'Средняя теплопроводность скелета породы ниже ММП, ккал/(м∙ч∙°К)': 2.3, 'Средняя теплопроводность заколонного цемента, ккал/(м∙ч∙°К)': 2.0}
    data_df = pandas.read_excel('Initial data.xlsx', sheet_name='Характеристики окружающих г.п.', header=None, index_col=0)
    rock_data_dict=data_df.to_dict()[1]

    # чтение исходных данных из excel-файла (Параметры расчета) формат {'Температура окружающей среды': 260.0, 'Минимальное ожидаемое шлейфовое давление': 0.75, 'Шаг депрессии': 0.01, 'Максимальная депрессия': 0.6}
    data_df = pandas.read_excel('Initial data.xlsx', sheet_name='Параметры расчета', header=None, index_col=0)
    calculation_data_dict = data_df.to_dict()[1]

    initial_data=Data()
    initial_data.rocks_props=rock_data_dict
    initial_data.calc_props=calculation_data_dict
    initial_data.fluids_props=fluids_data_dict
    initial_data.reservoir_props=reservoir_data_dict
    initial_data.tubing_props=tubing_data_dict

    return initial_data