import tkinter as tk
from tkinter import ttk, filedialog
from controllers.controller import Controller
from views.add import AddWindow
from views.delete import DeleteWindow
from views.search import SearchWindow


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление футболистами")
        self.root.geometry("1920x1080")
        self.view_mode = "table"
        self.create_widgets()
        self.controller = Controller(self)
        self.setup_pagination()
        self.controller.load_data()

    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Панель кнопок
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="top", anchor="nw", padx=10, pady=10)

        buttons = [
            ("Добавить игрока", self.open_add_window),
            ("Поиск игроков", self.open_search_window),
            ("Удалить игроков", self.open_delete_window),
            ("Источник данных", self.open_change_data_source_window),
            ("Вид отображения", self.toggle_view_mode),
        ]

        for i, (text, cmd) in enumerate(buttons):
            btn = tk.Button(self.button_frame, text=text, command=cmd)
            btn.grid(row=0, column=i, padx=5, pady=5)

        self.data_container = tk.Frame(self.root)
        self.data_container.pack(expand=True, fill="both")

        self.setup_table()
        self.setup_treeview()

    def setup_table(self):
        """Настройка табличного представления"""
        self.tree = ttk.Treeview(
            self.data_container,
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

        columns_config = {
            "ФИО игрока": 250,
            "Дата рождения": 120,
            "Команда": 150,
            "Город": 120,
            "Состав": 100,
            "Позиция": 120,
        }

        for col, width in columns_config.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        self.tree.pack(expand=True, fill="both")

    def setup_treeview(self):
        """Настройка древовидного представления"""
        self.treeview = ttk.Treeview(self.data_container, show="tree")
        self.treeview.pack_forget()

    def setup_pagination(self):
        """Настройка пагинации"""
        self.pagination_frame = tk.Frame(self.root)
        self.pagination_frame.pack(side="bottom", fill="x", pady=10)

        self.records_label = tk.Label(
            self.pagination_frame, text="Записей на странице:"
        )
        self.records_label.pack(side="left", padx=5)

        self.records_var = tk.StringVar()
        self.records_entry = tk.Entry(
            self.pagination_frame,
            textvariable=self.records_var,
            width=5,
            validate="key",
            validatecommand=(self.root.register(self.validate_int), "%P"),
        )
        self.records_entry.pack(side="left", padx=5)
        self.records_entry.bind("<Return>", self.handle_records_change)

        self.total_pages_label = tk.Label(self.pagination_frame, text="")
        self.total_pages_label.pack(side="left", padx=10)

        # Кнопки навигации
        self.first_btn = tk.Button(
            self.pagination_frame,
            text="<<",
            command=self.controller.first_page,
            state="disabled",
        )
        self.first_btn.pack(side="left", padx=2)

        self.prev_btn = tk.Button(
            self.pagination_frame,
            text="<",
            command=self.controller.prev_page,
            state="disabled",
        )
        self.prev_btn.pack(side="left", padx=2)

        self.page_label = tk.Label(self.pagination_frame, text="1/1")
        self.page_label.pack(side="left", padx=5)

        self.next_btn = tk.Button(
            self.pagination_frame,
            text=">",
            command=self.controller.next_page,
            state="disabled",
        )
        self.next_btn.pack(side="left", padx=2)

        self.last_btn = tk.Button(
            self.pagination_frame,
            text=">>",
            command=self.controller.last_page,
            state="disabled",
        )
        self.last_btn.pack(side="left", padx=2)

        self.records_var.set(str(self.controller.records_per_page))

    def validate_int(self, value):
        """Валидация целочисленного ввода"""
        return value.isdigit() or value == ""

    def handle_records_change(self, event=None):
        """Обработка изменения количества записей"""
        if self.records_var.get().isdigit():
            new_value = int(self.records_var.get())
            if new_value > 0:
                self.controller.change_records_per_page(new_value)
        else:
            self.records_var.set(str(self.controller.records_per_page))

    def update_table(self, players, current_page, total_pages, total_records):
        """Обновление данных в таблице"""
        for widget in [self.tree, self.treeview]:
            for item in widget.get_children():
                widget.delete(item)

        if self.view_mode == "table":
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
        else:
            for player in players:
                player_node = self.treeview.insert(
                    "",
                    "end",
                    text=f"{player.full_name} ({player.birth_date})",
                    open=True,
                )
                fields = [
                    ("Команда", player.football_team),
                    ("Город", player.home_city),
                    ("Состав", player.team_type.value),
                    ("Позиция", player.position.value),
                ]
                for field, value in fields:
                    self.treeview.insert(player_node, "end", text=f"{field}: {value}")

        self.update_pagination_controls(current_page, total_pages, total_records)

    def update_pagination_controls(self, current_page, total_pages, total_records):
        """Обновление элементов управления пагинацией"""
        self.page_label.config(text=f"{current_page}/{total_pages}")
        self.total_pages_label.config(text=f"Всего игроков: {total_records}")

        # Обновление состояния кнопок
        nav_buttons = [self.first_btn, self.prev_btn, self.next_btn, self.last_btn]

        states = [
            current_page > 1,
            current_page > 1,
            current_page < total_pages,
            current_page < total_pages,
        ]

        for btn, state in zip(nav_buttons, states):
            btn.config(state="normal" if state else "disabled")

    def toggle_view_mode(self):
        window = tk.Toplevel(self.root)
        window.title("Способ отображения")
        window.geometry("300x150")
        ttk.Button(window, text="Таблица", command=self.change_to_table).pack(pady=5)
        ttk.Button(window, text="Дерево", command=self.change_to_tree).pack(pady=5)
        ttk.Button(window, text="Закрыть", command=window.destroy).pack(pady=5)

    def change_to_table(self):
        self.view_mode = "table"
        self.treeview.pack_forget()
        self.tree.pack(expand=True, fill="both")
        self.controller.update_view()

    def change_to_tree(self):
        self.view_mode = "tree"
        self.tree.pack_forget()
        self.treeview.pack(expand=True, fill="both")
        self.controller.update_view()

    def open_error_window(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Ошибка")
        error_window.geometry("400x150")
        ttk.Label(error_window, text=message).pack(pady=10)
        ttk.Button(error_window, text="OK", command=error_window.destroy).pack()

    def open_deleted_count_window(self, message):
        window = tk.Toplevel(self.root)
        window.title("Результат удаления")
        window.geometry("400x150")
        ttk.Label(window, text=message).pack(pady=10)
        ttk.Button(window, text="OK", command=window.destroy).pack()

    def open_change_data_source_window(self):
        window = tk.Toplevel(self.root)
        window.title("Источник данных")
        window.geometry("300x200")
        ttk.Button(
            window,
            text="База данных",
            command=lambda: self.controller.change_data_source("db"),
        ).pack(pady=5)
        ttk.Button(
            window,
            text="XML (файл по умолчанию)",
            command=lambda: self.controller.change_data_source("xml"),
        ).pack(pady=5)
        ttk.Button(
            window, text="Выбрать XML файл...", command=self.open_xml_file_dialog
        ).pack(pady=5)
        ttk.Button(window, text="Закрыть", command=window.destroy).pack(pady=5)

    def open_xml_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            self.controller.change_xml_file(file_path)

    def open_add_window(self):
        AddWindow(self).show()

    def open_delete_window(self):
        DeleteWindow(self).show()

    def open_search_window(self):
        SearchWindow(self).show()
