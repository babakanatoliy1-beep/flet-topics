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
    def __init__(self, value, on_click):
        super().__init__(value, on_click, ft.Colors.WHITE24)


class ActionButton(CalcButton):
    def __init__(self, value, on_click):
        super().__init__(value, on_click, ft.Colors.ORANGE)


class ExtraButton(CalcButton):
    def __init__(self, value, on_click):
        super().__init__(value, on_click, ft.Colors.BLUE_GREY_100, ft.Colors.BLACK)


class BackspaceButton(CalcButton):
    def __init__(self, value, on_click):
        super().__init__(value, on_click, ft.Colors.RED_800, ft.Colors.WHITE)


def main(page: ft.Page):
    page.title = "Calculator"
    page.bgcolor = ft.Colors.BLACK

    operand1 = ""
    operand2 = ""
    operator = ""
    new_operand = False

    expression_text = ft.Text(
        value="",
        size=18,
        color=ft.Colors.WHITE38
    )

    result = ft.Text(
        value="0",
        size=40,
        color=ft.Colors.WHITE
    )

    def update_expression():
        if operator == "":
            expression_text.value = operand1
        elif operand2 == "":
            expression_text.value = f"{operand1} {operator}"
        else:
            expression_text.value = f"{operand1} {operator} {operand2}"

    def button_click(e):
        nonlocal operand1, operand2, operator, new_operand
        value = e.control.value

        if value == "AC":
            operand1 = ""
            operand2 = ""
            operator = ""
            result.value = "0"
            expression_text.value = ""
            new_operand = False

        elif value == "⌫":

            if new_operand:
                return

            if operator == "":
                operand1 = operand1[:-1]
                result.value = operand1 if operand1 else "0"

            else:
                operand2 = operand2[:-1]
                result.value = operand2 if operand2 else "0"

            update_expression()

        elif value in ["+", "-", "*", "/"]:

            if operand1 == "":
                return

            operator = value
            new_operand = False
            update_expression()

        elif value == "=":

            if operand1 and operator and operand2:
                try:
                    expression = f"{operand1}{operator}{operand2}"
                    answer = str(eval(expression))

                    expression_text.value = f"{operand1} {operator} {operand2} ="
                    result.value = answer

                    operand1 = answer
                    operand2 = ""
                    operator = ""

                    new_operand = True

                except:
                    result.value = "Error"
                    expression_text.value = ""
                    operand1 = ""
                    operand2 = ""
                    operator = ""

        else:

            if new_operand:
                operand1 = ""
                operand2 = ""
                operator = ""
                result.value = "0"
                expression_text.value = ""
                new_operand = False

            if operator == "":
                operand1 += value
                result.value = operand1
            else:
                operand2 += value
                result.value = operand2

            update_expression()

        page.update()

    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.Colors.BLACK,
            border_radius=20,
            padding=20,
            content=ft.Column(
                controls=[

                    ft.Row([expression_text], alignment=ft.MainAxisAlignment.END),

                    ft.Row([result], alignment=ft.MainAxisAlignment.END),

                    ft.Row([
                        ExtraButton("AC", button_click),
                        BackspaceButton("⌫", button_click),
                        ExtraButton("%", button_click),
                        ActionButton("/", button_click),
                    ]),

                    ft.Row([
                        DigitButton("7", button_click),
                        DigitButton("8", button_click),
                        DigitButton("9", button_click),
                        ActionButton("*", button_click),
                    ]),

                    ft.Row([
                        DigitButton("4", button_click),
                        DigitButton("5", button_click),
                        DigitButton("6", button_click),
                        ActionButton("-", button_click),
                    ]),

                    ft.Row([
                        DigitButton("1", button_click),
                        DigitButton("2", button_click),
                        DigitButton("3", button_click),
                        ActionButton("+", button_click),
                    ]),

                    ft.Row([
                        DigitButton("0", button_click),
                        ActionButton("=", button_click),
                    ]),
                ]
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
