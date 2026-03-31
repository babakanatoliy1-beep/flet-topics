import flet as ft
import json
import os


class Task(ft.Column):
    def __init__(self, task_name, completed, app):
        super().__init__()
        self.app = app
        self.task_name = task_name

        self.display_task = ft.Checkbox(
            label=self.task_name,
            value=completed,
            expand=True,
            on_change=self.status_changed
        )

        self.edit_name = ft.TextField(expand=True)

        self.display_view = ft.Row(
            controls=[
                self.display_task,
                ft.IconButton(icon=ft.Icons.EDIT, on_click=self.edit_clicked),
                ft.IconButton(icon=ft.Icons.DELETE, on_click=self.delete_clicked),
            ]
        )

        self.edit_view = ft.Row(
            visible=False,
            controls=[
                self.edit_name,
                ft.IconButton(icon=ft.Icons.SAVE, on_click=self.save_clicked),
            ]
        )

        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        if self.edit_name.value.strip():
            self.task_name = self.edit_name.value
            self.display_task.label = self.task_name
            self.app.save_tasks()  # Зберігаємо зміни у файл

        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.app.confirm_delete(self)

    def status_changed(self, e):
        self.app.save_tasks()  # Зберігаємо стан Checkbox


class ToDoApp(ft.Column):
    def __init__(self, page):
        super().__init__()
        self._page = page

        self.new_task = ft.TextField(
            hint_text="Що потрібно зробити?",
            expand=True,
            on_submit=self.add_clicked
        )

        self.search = ft.TextField(
            hint_text="Пошук...",
            prefix_icon=ft.Icons.SEARCH,
            on_change=self.filter_tasks,
            expand=True
        )

        self.tasks_view = ft.Column()

        self.controls = [
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=self.add_clicked
                    ),
                ]
            ),
            self.search,
            self.tasks_view,
        ]

        # Спочатку додаємо елементи, потім завантажуємо дані
        self.load_tasks()

    def filter_tasks(self, e):
        search_text = self.search.value.lower()
        for task in self.tasks_view.controls:
            task.visible = search_text in task.task_name.lower()
        self.update()

    def save_tasks(self):
        data = []
        for task in self.tasks_view.controls:
            data.append({
                "name": task.task_name,
                "completed": task.display_task.value
            })
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_tasks(self):
        if not os.path.exists("tasks.json"):
            return
        try:
            with open("tasks.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                task = Task(item["name"], item["completed"], self)
                self.tasks_view.controls.append(task)
        except Exception as ex:
            print(f"Помилка завантаження: {ex}")

    def confirm_delete(self, task):
        # Функція закриття
        def close_dlg(e):
            # Використовуємо e.control.page — це найнадійніший шлях до поточної сторінки
            if hasattr(e.page, "close"):
                e.page.close(dialog)  # Для нових версій Flet
            else:
                dialog.open = False  # Для старих версій
                e.page.update()

        def yes_click(e):
            if task in self.tasks_view.controls:
                self.tasks_view.controls.remove(task)
                self.save_tasks()
                # Важливо оновити компонент ToDoApp, щоб список завдань перемалювався
                self.update()
            close_dlg(e)

        # Створюємо діалог
        dialog = ft.AlertDialog(
            title=ft.Text("Підтвердження"),
            content=ft.Text(f"Видалити '{task.task_name}'?"),
            actions=[
                ft.TextButton("Так", on_click=yes_click),
                ft.TextButton("Ні", on_click=close_dlg),
            ],
        )

        # Використовуємо сучасний метод відкриття
        self._page.show_dialog(dialog)

    def add_clicked(self, e):
        if self.new_task.value.strip():
            # Додано аргумент False для статусу completed
            task = Task(self.new_task.value, False, self)
            self.tasks_view.controls.append(task)
            self.new_task.value = ""
            self.save_tasks()  # Зберігаємо нове завдання
            self.update()


def main(page: ft.Page):
    page.title = "To-Do App 💾"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 600
    page.window_height = 600

    app = ToDoApp(page)
    page.add(app)


if __name__ == "__main__":
    ft.run(main)
