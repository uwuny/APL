import sys
import PyQt5.QtWidgets
import matplotlib.pyplot
import matplotlib.backends.backend_qt5agg
import numpy

class Programma(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Колебания")
        self.setGeometry(100, 100, 600, 400)

        # Основное приложение
        application = PyQt5.QtWidgets.QWidget()
        self.setCentralWidget(application)
        plan = PyQt5.QtWidgets.QVBoxLayout(application)

        # Поля ввода
        input = PyQt5.QtWidgets.QHBoxLayout()

        self.amplituda_input = PyQt5.QtWidgets.QLineEdit("1")
        input.addWidget(PyQt5.QtWidgets.QLabel("Амплитуда (м):"))
        input.addWidget(self.amplituda_input)

        self.frequency_input = PyQt5.QtWidgets.QLineEdit("1")
        input.addWidget(PyQt5.QtWidgets.QLabel("Частота (Гц):"))
        input.addWidget(self.frequency_input)

        self.phase_input = PyQt5.QtWidgets.QLineEdit("0")
        input.addWidget(PyQt5.QtWidgets.QLabel("Фаза (градусы):"))
        input.addWidget(self.phase_input)

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
            # Имена для значений
            a = self.check_value(self.amplituda_input.text(), "Амплитуда", 0)  # Амплитуда
            f = self.check_value(self.frequency_input.text(), "Частота", 0.1)  # Частота
            p = self.check_value(self.phase_input.text(), "Фаза")  # Фаза

            # Переменные для графика
            t = numpy.linspace(0, 5, 100)  # Время: начало, конец, количество точек
            x = a * numpy.cos(2 * numpy.pi * f * t + p * numpy.pi / 180)  # Формула колебаний

            # Строим график
            self.axes.clear()
            self.axes.plot(t, x)
            self.axes.set_xlabel("Время (с)")
            self.axes.set_ylabel("Смещение (м)")
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
