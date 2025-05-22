import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
from controllers.search_controller import SearchResultsController
from views.search_results import SearchResultsView


class SearchWindow:
    def __init__(self, gui):
        self.gui = gui
        self.controller = gui.controller

    def show(self):
        self.window = tk.Toplevel(self.gui.root)
        self.window.title("Поиск футболистов")
        self.window.geometry("400x250")

        ttk.Button(
            self.window,
            text="Поиск по ФИО и дате рождения",
            command=self.search_by_name_birth,
        ).pack(pady=5)
        ttk.Button(
            self.window,
            text="Поиск по позиции или составу",
            command=self.search_by_position_team_type,
        ).pack(pady=5)
        ttk.Button(
            self.window,
            text="Поиск по команде или городу",
            command=self.search_by_team_city,
        ).pack(pady=5)
        ttk.Button(self.window, text="Закрыть", command=self.window.destroy).pack(
            pady=15
        )

    def create_results_window(self, results):
        results_window = tk.Toplevel(self.window)
        results_window.title("Результаты поиска")
        results_window.geometry("1200x600")

        search_controller = SearchResultsController(results)
        search_view = SearchResultsView(results_window, search_controller)
        search_controller.view = search_view
        search_controller.update_view()

    def search_by_name_birth(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("Поиск по ФИО/дате")
        input_window.geometry("300x150")

        ttk.Label(input_window, text="Часть ФИО (необязательно):").pack(pady=2)
        name_entry = ttk.Entry(input_window)
        name_entry.pack()

        ttk.Label(input_window, text="Дата рождения (необязательно):").pack(pady=2)
        date_entry = DateEntry(input_window, date_pattern="yyyy-mm-dd")
        date_entry.pack()

        def search():
            birth_date = date_entry.get_date() if date_entry.get() else None
            results = self.controller.search_by_name_birth(
                name_part=name_entry.get(), birth_date=birth_date
            )
            input_window.destroy()
            self.create_results_window(results)

        ttk.Button(input_window, text="Найти", command=search).pack(pady=5)
        ttk.Button(input_window, text="Закрыть", command=input_window.destroy).pack()

    def search_by_position_team_type(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("Поиск по позиции/составу")
        input_window.geometry("300x150")

        ttk.Label(input_window, text="Позиция:").pack(pady=2)
        position_combo = ttk.Combobox(
            input_window,
            values=["Вратарь", "Защитник", "Полузащитник", "Нападающий"],
            state="readonly",
        )
        position_combo.pack()

        ttk.Label(input_window, text="Состав:").pack(pady=2)
        team_type_combo = ttk.Combobox(
            input_window, values=["основной", "запасной", "n/a"], state="readonly"
        )
        team_type_combo.pack()

        def search():
            results = self.controller.search_by_position_team_type(
                position=position_combo.get(), team_type=team_type_combo.get()
            )
            input_window.destroy()
            self.create_results_window(results)

        ttk.Button(input_window, text="Найти", command=search).pack(pady=5)
        ttk.Button(input_window, text="Закрыть", command=input_window.destroy).pack()

    def search_by_team_city(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("Поиск по команде/городу")
        input_window.geometry("300x150")

        ttk.Label(input_window, text="Команда (необязательно):").pack(pady=2)
        team_entry = ttk.Entry(input_window)
        team_entry.pack()

        ttk.Label(input_window, text="Город (необязательно):").pack(pady=2)
        city_entry = ttk.Entry(input_window)
        city_entry.pack()

        def search():
            results = self.controller.search_by_team_city(
                team=team_entry.get(), city=city_entry.get()
            )
            input_window.destroy()
            self.create_results_window(results)

        ttk.Button(input_window, text="Найти", command=search).pack(pady=5)
        ttk.Button(input_window, text="Закрыть", command=input_window.destroy).pack()
