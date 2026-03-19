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


class BackspaceButton(CalcButton):
    def __init__(self, value, on_click):
        super().__init__(value, on_click, ft.Colors.RED_800, ft.Colors.WHITE)


class CalculatorApp(ft.Container):

    def __init__(self):
        super().__init__()

        self.reset()

        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = 20
        self.padding = 20

        self.history_list = ft.ListView(expand=True, spacing=4, width=220)

        self.expression = ft.Text(value="", color=ft.Colors.GREY, size=16)
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=40)

        self.content = ft.Column(
            controls=[

                ft.Row([self.expression], alignment=ft.MainAxisAlignment.END),
                ft.Row([self.result], alignment=ft.MainAxisAlignment.END),

                ft.Row(
                    controls=[
                        ExtraButton("AC", self.button_clicked),
                        BackspaceButton("⌫", self.button_clicked),
                        ExtraButton("+/-", self.button_clicked),
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

    def add_to_history(self, text):

        def on_click(e):
            value = text.split("= ")[-1]
            self.result.value = value
            self.new_operand = True
            self.update()

        self.history_list.controls.insert(
            0,
            ft.TextButton(
                content=ft.Text(text),
                on_click=on_click
            )
        )

        if len(self.history_list.controls) > 10:
            self.history_list.controls.pop()

        self.history_list.update()

    def button_clicked(self, e):

        data = e.control.value

        if data == "⌫":
            if self.new_operand:
                return

            if self.result.value == "Error":
                self.result.value = "0"

            elif len(self.result.value) > 1:
                self.result.value = self.result.value[:-1]
            else:
                self.result.value = "0"

        elif data == "AC":
            self.result.value = "0"
            self.expression.value = ""
            self.reset()

        elif data in "0123456789":

            if self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                if self.result.value == "0":
                    self.result.value = data
                else:
                    self.result.value += data

        elif data == ".":

            if self.new_operand:
                return

            if "." not in self.result.value:
                self.result.value += "."

        elif data in "+-*/":

            operand2 = float(self.result.value)
            result = self.calculate(self.operand1, operand2, self.operator)

            self.expression.value += f"{self.format_number(operand2)} {data} "
            self.result.value = str(result)

            self.operand1 = float(result)
            self.operator = data
            self.new_operand = True

        elif data == "=":

            operand2 = float(self.result.value)

            full_expr = f"{self.expression.value}{self.format_number(operand2)} ="

            result = self.calculate(self.operand1, operand2, self.operator)

            self.result.value = str(result)
            self.expression.value = full_expr

            self.add_to_history(f"{full_expr} {result}")

            self.reset()

        elif data == "+/-":
            value = float(self.result.value) * -1
            self.result.value = str(self.format_number(value))

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

    calc = CalculatorApp()

    history_panel = ft.Container(
        width=220,
        bgcolor=ft.Colors.BLACK,
        padding=10,
        content=ft.Column(
            controls=[
                ft.Text("Історія", color=ft.Colors.WHITE, size=20),
                calc.history_list,
                ft.TextButton(
                    content=ft.Text("Очистити"),
                    on_click=lambda e: (
                        calc.history_list.controls.clear(),
                        calc.history_list.update()
                    )
                )
            ]
        )
    )

    page.add(
        ft.Row(
            controls=[
                calc,
                history_panel
            ]
        )
    )


ft.run(main)
