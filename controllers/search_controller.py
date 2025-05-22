class SearchResultsController:
    def __init__(self, search_results):
        self.search_results = search_results  # Теперь список Player
        self.current_page = 1
        self.records_per_page = 10
        self.view = None

    def calculate_total_pages(self):
        return max(
            1,
            (len(self.search_results) + self.records_per_page - 1)
            // self.records_per_page,
        )

    def get_current_page_data(self):
        start_idx = (self.current_page - 1) * self.records_per_page
        end_idx = min(start_idx + self.records_per_page, len(self.search_results))
        return self.search_results[start_idx:end_idx]

    def change_page(self, page):
        if 1 <= page <= self.calculate_total_pages():
            self.current_page = page
            self.update_view()

    def first_page(self):
        self.change_page(1)

    def prev_page(self):
        self.change_page(self.current_page - 1)

    def next_page(self):
        self.change_page(self.current_page + 1)

    def last_page(self):
        self.change_page(self.calculate_total_pages())

    def change_records_per_page(self, new_value):
        try:
            value = int(new_value)
            if value <= 0:
                raise ValueError("Введите положительное число больше нуля")

            self.records_per_page = value
            self.current_page = 1
            self.update_view()
            return True
        except ValueError as e:
            if self.view:
                self.view.open_error_window(f"Ошибка ввода: {str(e)}")
            return False

    def update_view(self):
        if self.view:
            page_data = self.get_current_page_data()
            self.view.update_table(
                players=page_data,  # Изменено с athletes на players
                current_page=self.current_page,
                total_pages=self.calculate_total_pages(),
                total_records=len(self.search_results),
            )
