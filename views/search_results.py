import tkinter as tk
from tkinter import ttk
from datetime import date


class SearchResultsView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.controller.view = self

        self.tree = ttk.Treeview(
            root,
            columns=(
                "ФИО игрока",
                "Дата рождения",
                "Команда",
                "Город",
                "Состав",
                "Позиция",
            ),
            show="headings",
        )

        columns = {
            "ФИО игрока": 200,
            "Дата рождения": 120,
            "Команда": 150,
            "Город": 120,
            "Состав": 100,
            "Позиция": 120,
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(expand=True, fill="both")

        # Пагинация
        self.pagination_frame = tk.Frame(root)
        self.pagination_frame.pack(side="bottom", fill="x", pady=10)

        self.records_label = tk.Label(
            self.pagination_frame, text="Записей на странице:"
        )
        self.records_label.pack(side="left", padx=5)

        self.records_var = tk.StringVar(value=str(self.controller.records_per_page))
        self.records_entry = tk.Entry(
            self.pagination_frame, textvariable=self.records_var, width=5
        )
        self.records_entry.pack(side="left", padx=5)
        self.records_entry.bind(
            "<Return>",
            lambda e: self.controller.change_records_per_page(self.records_var.get()),
        )

        self.total_pages_label = tk.Label(self.pagination_frame, text="")
        self.total_pages_label.pack(side="left", padx=10)

        # Кнопки навигации
        nav_buttons = [
            ("<<", self.controller.first_page),
            ("<", self.controller.prev_page),
            (">", self.controller.next_page),
            (">>", self.controller.last_page),
        ]

        for text, command in nav_buttons:
            btn = tk.Button(self.pagination_frame, text=text, command=command)
            btn.pack(side="left", padx=2)
            if text == "<":
                self.prev_btn = btn
            elif text == ">":
                self.next_btn = btn

        self.page_label = tk.Label(self.pagination_frame, text="1/1")
        self.page_label.pack(side="left", padx=5)

    def update_table(self, players, current_page, total_pages, total_records):
        # Очистка предыдущих данных
        self.tree.delete(*self.tree.get_children())

        # Добавление новых записей
        for player in players:
            self.tree.insert(
                "",
                "end",
                values=(
                    player.full_name,
                    player.birth_date.strftime("%d.%m.%Y"),
                    player.football_team,
                    player.home_city,
                    player.team_type.value,
                    player.position.value,
                ),
            )

        self.update_pagination_controls(current_page, total_pages, total_records)

    def update_pagination_controls(self, current_page, total_pages, total_records):
        self.page_label.config(text=f"{current_page}/{total_pages}")
        self.total_pages_label.config(text=f"Всего игроков: {total_records}")
        self.records_var.set(str(self.controller.records_per_page))

        self.prev_btn.config(state="normal" if current_page > 1 else "disabled")
        self.next_btn.config(
            state="normal" if current_page < total_pages else "disabled"
        )

    def open_error_window(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Ошибка")
        error_window.geometry("400x150")

        tk.Label(
            error_window, text="Произошла ошибка:", font=("Arial", 12, "bold")
        ).pack(pady=5)
        tk.Label(error_window, text=message, wraplength=350).pack(pady=5)
        tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=10)
