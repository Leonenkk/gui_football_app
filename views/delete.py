import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date


class DeleteWindow:
    def __init__(self, gui):
        self.gui = gui
        self.controller = gui.controller

    def show(self):
        self.window = tk.Toplevel(self.gui.root)
        self.window.title("Удаление футболистов")
        self.window.geometry("400x250")

        ttk.Button(
            self.window,
            text="Удалить по ФИО и дате рождения",
            command=self.delete_by_name_birth,
        ).pack(pady=5)
        ttk.Button(
            self.window,
            text="Удалить по позиции или составу",
            command=self.delete_by_position_team_type,
        ).pack(pady=5)
        ttk.Button(
            self.window,
            text="Удалить по команде или городу",
            command=self.delete_by_team_city,
        ).pack(pady=5)
        ttk.Button(self.window, text="Закрыть", command=self.window.destroy).pack(
            pady=15
        )

    def delete_by_name_birth(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("Удаление по ФИО/дате")
        input_window.geometry("300x200")

        ttk.Label(input_window, text="Часть ФИО (необязательно):").pack(pady=5)
        name_entry = ttk.Entry(input_window)
        name_entry.pack()

        ttk.Label(input_window, text="Дата рождения (необязательно):").pack(pady=5)
        date_entry = DateEntry(input_window, date_pattern="yyyy-mm-dd")
        date_entry.pack()

        def delete():
            birth_date = date_entry.get_date() if date_entry.get() else None
            self.controller.delete_by_name_birth(
                name_part=name_entry.get(), birth_date=birth_date
            )
            input_window.destroy()

        ttk.Button(input_window, text="Удалить", command=delete).pack(pady=10)
        ttk.Button(input_window, text="Закрыть", command=input_window.destroy).pack()

    def delete_by_position_team_type(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("Удаление по позиции/составу")
        input_window.geometry("300x150")

        ttk.Label(input_window, text="Позиция:").pack(pady=5)
        position_combo = ttk.Combobox(
            input_window,
            values=["Вратарь", "Защитник", "Полузащитник", "Нападающий"],
            state="readonly",
        )
        position_combo.pack()

        ttk.Label(input_window, text="Состав:").pack(pady=5)
        team_type_combo = ttk.Combobox(
            input_window, values=["основной", "запасной", "n/a"], state="readonly"
        )
        team_type_combo.pack()

        def delete():
            self.controller.delete_by_position_team_type(
                position=position_combo.get(), team_type=team_type_combo.get()
            )
            input_window.destroy()

        ttk.Button(input_window, text="Удалить", command=delete).pack(pady=10)
        ttk.Button(input_window, text="Закрыть", command=input_window.destroy).pack()

    def delete_by_team_city(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("Удаление по команде/городу")
        input_window.geometry("300x150")

        ttk.Label(input_window, text="Команда (необязательно):").pack(pady=5)
        team_entry = ttk.Entry(input_window)
        team_entry.pack()

        ttk.Label(input_window, text="Город (необязательно):").pack(pady=5)
        city_entry = ttk.Entry(input_window)
        city_entry.pack()

        def delete():
            self.controller.delete_by_team_city(
                team=team_entry.get(), city=city_entry.get()
            )
            input_window.destroy()

        ttk.Button(input_window, text="Удалить", command=delete).pack(pady=10)
        ttk.Button(input_window, text="Закрыть", command=input_window.destroy).pack()
