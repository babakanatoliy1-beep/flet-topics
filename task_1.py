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


def main(page: ft.Page):
    page.title = "Calculator"
    page.bgcolor = ft.Colors.BLACK

    expression = ""

    # рядок виразу
    expression_text = ft.Text(
        value="",
        size=18,
        color=ft.Colors.WHITE38
    )

    # результат
    result = ft.Text(
        value="0",
        size=40,
        color=ft.Colors.WHITE
    )

    def button_click(e):
        nonlocal expression
        value = e.control.value

        if value == "AC":
            expression = ""
            result.value = "0"
            expression_text.value = ""

        elif value == "=":
            try:
                expression_text.value = expression + " ="
                expression = str(eval(expression))
                result.value = expression
            except:
                result.value = "Error"
                expression = ""
                expression_text.value = ""

        else:
            expression += value
            result.value = expression
            expression_text.value = expression

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
                        ExtraButton("%", button_click),
                        ExtraButton(".", button_click),
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
