from abc import ABCMeta, abstractmethod, abstractproperty


class HazardSubstance():
    __metaclass__ = ABCMeta

    @abstractmethod
    def move(self):
        """Переместить объект"""

    @abstractproperty
    def name(self):
        """Название вещества"""

    @abstractproperty
    def form(self):
        """формула вещества"""

    @abstractproperty
    def gas_density(self):
        """Плотность газа"""

    @abstractproperty
    def liquid_density(self):
        """Плотность жидкости"""

    @abstractproperty
    def boiling_t(self):
        """Температура кипения"""

    @abstractproperty
    def k1(self):
        """коэффициент, зависящий от условий хранения АХОВ, для сжатых газов К1 ="""

    @abstractproperty
    def k2(self):
        """коэффициент, зависящий от физико-химических свойств АХОВ, удельная скорость испарения"""

    @abstractproperty
    def k3(self):
        """коэффициент, равный отношению пороговой токсодозы хлора к пороговой токсодозе другого АХОВ"""

    @abstractproperty
    def k7_1(self):
        """коэффициент, учитывающий влияние температуры воздуха, вычисляется для 1 облака"""

    @abstractproperty
    def k7_1_f(self):
        """функция для нахождения k7_1"""

    @abstractproperty
    def k7_2(self):
        """коэффициент, учитывающий влияние температуры воздуха, вычисляется для 1 облака"""

    @abstractproperty
    def k7_2_f(self):
        """функция для нахождения k7_2"""


