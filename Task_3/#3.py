import sys
import PyQt5.QtWidgets
import matplotlib.pyplot
import matplotlib.backends.backend_qt5agg
import numpy

class Programma(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Закон охлаждения Ньютона")
        self.setGeometry(100, 100, 600, 400)

        # Основное приложение
        application = PyQt5.QtWidgets.QWidget()
        self.setCentralWidget(application)
        plan = PyQt5.QtWidgets.QVBoxLayout(application)

        # Поля ввода
        input = PyQt5.QtWidgets.QHBoxLayout()

        self.t0_input = PyQt5.QtWidgets.QLineEdit("100")  # Начальная температура
        input.addWidget(PyQt5.QtWidgets.QLabel("T0 (°C):"))
        input.addWidget(self.t0_input)

        self.tenv_input = PyQt5.QtWidgets.QLineEdit("20")  # Температура среды
        input.addWidget(PyQt5.QtWidgets.QLabel("Tenv (°C):"))
        input.addWidget(self.tenv_input)

        self.k_input = PyQt5.QtWidgets.QLineEdit("0.1")  # Коэффициент теплообмена
        input.addWidget(PyQt5.QtWidgets.QLabel("k (1/с):"))
        input.addWidget(self.k_input)

        plan.addLayout(input)

        # Кнопка
        self.button = PyQt5.QtWidgets.QPushButton("Построить")
        self.button.clicked.connect(self.postroenie_graffic)
        plan.addWidget(self.button)

        # График
        self.graffic = matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg(matplotlib.pyplot.Figure())
        plan.addWidget(self.graffic)
        self.axes = self.graffic.figure.add_subplot(111)
        self.postroenie_graffic()

    def postroenie_graffic(self):
        try:
            # Получаем значения с проверкой
            t0 = self.check_value(self.t0_input.text(), "T0")  # Начальная температура
            tenv = self.check_value(self.tenv_input.text(), "Tenv")  # Температура среды
            k = self.check_value(self.k_input.text(), "k", 0.001)  # Коэффициент теплообмена

            # Проверяем, что k положительный и адекватный
            if k > 10:
                raise ValueError("Коэффициент k не может быть больше 10 (слишком большое значение).")

            # Время
            t = numpy.linspace(0, 100, 200)  # 0–100 секунд, 200 точек

            # Температура по закону Ньютона
            temp = tenv + (t0 - tenv) * numpy.exp(-k * t)

            # Строим график
            self.axes.clear()
            self.axes.plot(t, temp)
            self.axes.set_xlabel("Время (с)")
            self.axes.set_ylabel("Температура тела (°C)")
            self.axes.grid(True)
            self.graffic.draw()

        except ValueError as e:
            PyQt5.QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def check_value(self, value, name, min_val=None):
        # Проверка введённых значений
        try:
            num = float(value)
        except ValueError:
            raise ValueError(f"{name} должна быть числом.")
        if min_val is not None and num < min_val:
            raise ValueError(f"{name} не может быть меньше {min_val}.")
        return num

# Запуск
if __name__ == '__main__':
    proga = PyQt5.QtWidgets.QApplication(sys.argv)
    application = Programma()
    application.show()
    sys.exit(proga.exec_())