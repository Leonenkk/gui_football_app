import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime


class AddWindow:
    def __init__(self, gui):
        self.gui = gui
        self.controller = gui.controller

    def show(self):
        self.window = tk.Toplevel(self.gui.root)
        self.window.title("Добавление футболиста")
        self.window.geometry("450x400")

        main_frame = ttk.Frame(self.window)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Поля для ввода
        fields = [
            ("ФИО игрока", "entry"),
            ("Дата рождения", "date"),
            ("Футбольная команда", "entry"),
            ("Домашний город", "entry"),
            ("Состав", "combo"),
            ("Позиция", "combo"),
        ]

        self.entries = {}

        for i, (label, field_type) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(
                row=i, column=0, padx=5, pady=5, sticky="w"
            )

            if field_type == "entry":
                entry = ttk.Entry(main_frame, width=30)
                entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries[label] = entry

            elif field_type == "date":
                date_entry = DateEntry(
                    main_frame,
                    date_pattern="yyyy-mm-dd",
                    maxdate=datetime.today(),
                    width=27,
                )
                date_entry.grid(row=i, column=1, padx=5, pady=5)
                self.entries[label] = date_entry

            elif field_type == "combo":
                values = []
                if label == "Состав":
                    values = ["основной", "запасной", "n/a"]
                elif label == "Позиция":
                    values = ["Вратарь", "Защитник", "Полузащитник", "Нападающий"]

                combo = ttk.Combobox(
                    main_frame, values=values, state="readonly", width=27
                )
                combo.current(0)
                combo.grid(row=i, column=1, padx=5, pady=5)
                self.entries[label] = combo

        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields) + 1, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Добавить", command=self.add_player).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Закрыть", command=self.window.destroy).pack(
            side="left", padx=5
        )

    def add_player(self):
        data = {
            "full_name": self.entries["ФИО игрока"].get(),
            "birth_date": self.entries["Дата рождения"].get_date(),
            "football_team": self.entries["Футбольная команда"].get(),
            "home_city": self.entries["Домашний город"].get(),
            "team_type": self.entries["Состав"].get(),
            "position": self.entries["Позиция"].get(),
        }

        self.controller.add_player(**data)
        self.window.destroy()
