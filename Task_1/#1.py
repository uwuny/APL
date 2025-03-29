import sys
import PyQt5.QtWidgets
import matplotlib.pyplot
import matplotlib.backends.backend_qt5agg
import numpy

class Programma(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Движение тела под углом")
        self.setGeometry(100, 100, 600, 400)

        # Основное приложение
        application = PyQt5.QtWidgets.QWidget()
        self.setCentralWidget(application)
        plan = PyQt5.QtWidgets.QVBoxLayout(application)

        # Поля ввода
        input = PyQt5.QtWidgets.QHBoxLayout()

        self.speed_input = PyQt5.QtWidgets.QLineEdit("10")
        input.addWidget(PyQt5.QtWidgets.QLabel("Скорость (м/с):"))
        input.addWidget(self.speed_input)

        self.angle_input = PyQt5.QtWidgets.QLineEdit("45")
        input.addWidget(PyQt5.QtWidgets.QLabel("Угол (градусы):"))
        input.addWidget(self.angle_input)

        plan.addLayout(input)

        # Кнопка
        self.button = PyQt5.QtWidgets.QPushButton("Построить траекторию")
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
            v = self.check_value(self.speed_input.text(), "Скорость", 0.1)
            angle = self.check_value(self.angle_input.text(), "Угол")

            # Ускорение свободного падения
            g = 9.81

            # Преобразуем угол в радианы
            angle_rad = angle * numpy.pi / 180

            # Вычисляем компоненты скорости
            v_x = v * numpy.cos(angle_rad)  # Горизонтальная скорость
            v_y = v * numpy.sin(angle_rad)  # Вертикальная скорость

            # Время полёта до высшей точки или до земли
            if abs(v_y) < 1e-10:  # Угол 0°, 180° и т.д. — горизонтальное движение
                t_total = 5  # Произвольное время для горизонтального движения
                t = numpy.linspace(0, t_total, 100)
                x = v_x * t
                y = numpy.zeros_like(t)
            elif abs(v_x) < 1e-10:  # Угол 90°, 270° и т.д. — вертикальное движение
                t_total = v_y / g  # Время до крайней точки
                t = numpy.linspace(0, 2 * t_total, 100)  # Полное время полёта
                x = numpy.zeros_like(t)  # Нет горизонтального движения
                y = v_y * t - 0.5 * g * t ** 2
            else:
                # Обычная траектория
                t_total = 2 * v_y / g  # Полное время полёта
                t = numpy.linspace(0, t_total, 100)
                x = v_x * t
                y = v_y * t - 0.5 * g * t ** 2

            # Делаем так, чтобы тело не уходило под землю
            y = numpy.where(y < 0, 0, y)

            # Строим график
            self.axes.clear()
            self.axes.plot(x, y)
            self.axes.set_xlabel("Расстояние (м)")
            self.axes.set_ylabel("Высота (м)")
            self.axes.grid(True)
            self.graffic.draw()

        except ValueError as e:
            PyQt5.QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def check_value(self, value, name, min_val=None):
        # Проверка введённых значений.
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