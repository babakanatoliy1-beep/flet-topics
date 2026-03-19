import flet as ft


class CalcButton(ft.Button):
    def __init__(self, value, on_click, bgcolor, color=ft.Colors.WHITE, expand=1):
        super().__init__(
            expand=expand,
            bgcolor=bgcolor,
            on_click=on_click,
            content=ft.Text(value, size=20, color=color),
        )
        self.value = value


class DigitButton(CalcButton):
    def __init__(self, value, on_click, expand=1):
        super().__init__(value, on_click, ft.Colors.WHITE24, ft.Colors.WHITE, expand)


class ActionButton(CalcButton):
    def __init__(self, value, on_click):
        super().__init__(value, on_click, ft.Colors.ORANGE, ft.Colors.WHITE)


class ExtraButton(CalcButton):
    def __init__(self, value, on_click):
        super().__init__(value, on_click, ft.Colors.BLUE_GREY_100, ft.Colors.BLACK)


class CalculatorApp(ft.Container):

    def __init__(self):
        super().__init__()

        self.reset()

        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = 20
        self.padding = 20

        self.expression = ft.Text(
            value="",
            color=ft.Colors.GREY,
            size=16
        )

        self.result = ft.Text(
            value="0",
            color=ft.Colors.WHITE,
            size=40
        )

        self.content = ft.Column(
            controls=[

                ft.Row(
                    controls=[self.expression],
                    alignment=ft.MainAxisAlignment.END
                ),

                ft.Row(
                    controls=[self.result],
                    alignment=ft.MainAxisAlignment.END
                ),

                ft.Row(
                    controls=[
                        ExtraButton("AC", self.button_clicked),
                        ExtraButton("+/-", self.button_clicked),
                        ExtraButton("%", self.button_clicked),
                        ActionButton("/", self.button_clicked),
                    ]
                ),

                ft.Row(
                    controls=[
                        DigitButton("7", self.button_clicked),
                        DigitButton("8", self.button_clicked),
                        DigitButton("9", self.button_clicked),
                        ActionButton("*", self.button_clicked),
                    ]
                ),

                ft.Row(
                    controls=[
                        DigitButton("4", self.button_clicked),
                        DigitButton("5", self.button_clicked),
                        DigitButton("6", self.button_clicked),
                        ActionButton("-", self.button_clicked),
                    ]
                ),

                ft.Row(
                    controls=[
                        DigitButton("1", self.button_clicked),
                        DigitButton("2", self.button_clicked),
                        DigitButton("3", self.button_clicked),
                        ActionButton("+", self.button_clicked),
                    ]
                ),

                ft.Row(
                    controls=[
                        DigitButton("0", self.button_clicked, expand=2),
                        DigitButton(".", self.button_clicked),
                        ActionButton("=", self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):

        data = e.control.value

        # Очистити
        if data == "AC":
            self.result.value = "0"
            self.expression.value = ""
            self.reset()

        # Цифри
        elif data in "0123456789":

            if self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                if self.result.value == "0":
                    self.result.value = data
                else:
                    self.result.value += data

        # Крапка
        elif data == ".":

            if self.new_operand:
                return

            if "." not in self.result.value:
                self.result.value += "."

        # Оператори
        elif data in "+-*/":

            operand2 = float(self.result.value)

            result = self.calculate(self.operand1, operand2, self.operator)

            self.expression.value += f"{self.format_number(operand2)} {data} "

            self.result.value = str(result)

            self.operand1 = float(result)
            self.operator = data
            self.new_operand = True

        # Рівно
        elif data == "=":

            operand2 = float(self.result.value)

            self.expression.value += f"{self.format_number(operand2)} ="

            result = self.calculate(self.operand1, operand2, self.operator)

            self.result.value = str(result)

            self.reset()

        # Плюс мінус
        elif data == "+/-":

            value = float(self.result.value) * -1
            self.result.value = str(self.format_number(value))

        # Відсотки
        elif data == "%":

            value = float(self.result.value) / 100
            self.result.value = str(self.format_number(value))

        self.update()

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True

    def format_number(self, number):

        if number % 1 == 0:
            return int(number)

        return number

    def calculate(self, a, b, op):

        if op == "+":
            return self.format_number(a + b)

        if op == "-":
            return self.format_number(a - b)

        if op == "*":
            return self.format_number(a * b)

        if op == "/":

            if b == 0:
                return "Error"

            return self.format_number(a / b)


def main(page: ft.Page):

    page.title = "Калькулятор"
    page.bgcolor = ft.Colors.BLACK
    page.window_width = 400
    page.window_height = 520

    calc = CalculatorApp()

    page.add(calc)


ft.run(main)
