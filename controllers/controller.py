from models.crud import Crud
from models.xml_adapter import XMLAdapter
from models.database import TeamType, PlayerPosition
from datetime import date


class Controller:
    def __init__(self, view):
        self.view = view
        self.current_page = 1
        self.records_per_page = 10
        self.all_players = []

    def load_data(self):
        self.all_players = Crud.get_data()
        total_pages = self.calculate_total_pages()
        if self.current_page > total_pages:
            self.current_page = total_pages
        self.update_view()

    def change_data_source(self, source: str):
        if source == "db":
            Crud.set_data_source("db")
            self.current_page = 1
            self.load_data()
        elif source == "xml":
            default_path = XMLAdapter().xml_file
            self.change_xml_file(str(default_path))

    def change_xml_file(self, file_path: str):
        if file_path:
            Crud.change_xml_file(file_path)
            Crud.set_data_source("xml")
            self.current_page = 1
            self.load_data()

    def update_view(self):
        total_pages = self.calculate_total_pages()
        page_players = self.get_current_page_data()
        self.view.update_table(
            players=page_players,
            current_page=self.current_page,
            total_pages=total_pages,
            total_records=len(self.all_players),
        )

    def calculate_total_pages(self):
        return max(
            1,
            (len(self.all_players) + self.records_per_page - 1)
            // self.records_per_page,
        )

    def get_current_page_data(self):
        start = (self.current_page - 1) * self.records_per_page
        end = start + self.records_per_page
        return self.all_players[start:end]

    def change_page(self, page: int):
        if 1 <= page <= self.calculate_total_pages():
            self.current_page = page
            self.update_view()

    def change_records_per_page(self, new_value: int) -> bool:
        if new_value < 1:
            return False
        self.records_per_page = new_value
        self.current_page = 1
        self.update_view()
        return True

    def first_page(self):
        self.change_page(1)

    def prev_page(self):
        self.change_page(self.current_page - 1)

    def next_page(self):
        self.change_page(self.current_page + 1)

    def last_page(self):
        self.change_page(self.calculate_total_pages())

    def validate_player_data(
        self,
        full_name: str,
        birth_date: date,
        team: str,
        city: str,
        team_type: str,
        position: str,
    ):
        errors = []

        if not full_name.strip():
            errors.append("ФИО обязательно для заполнения")
        if not birth_date:
            errors.append("Дата рождения обязательна")
        elif birth_date > date.today():
            errors.append("Дата рождения не может быть в будущем")
        if not team.strip():
            errors.append("Укажите футбольную команду")
        if not city.strip():
            errors.append("Укажите домашний город")

        try:
            TeamType(team_type)
        except ValueError:
            errors.append("Неверный тип состава команды")

        try:
            PlayerPosition(position)
        except ValueError:
            errors.append("Неверная позиция игрока")

        return errors if errors else None

    def add_player(
        self,
        full_name: str,
        birth_date: date,
        football_team: str,
        home_city: str,
        team_type: str,
        position: str,
    ):
        errors = self.validate_player_data(
            full_name, birth_date, football_team, home_city, team_type, position
        )

        if errors:
            self.view.open_error_window("\n".join(errors))
            return

        Crud.add_data(
            full_name=full_name,
            birth_date=birth_date,
            football_team=football_team,
            home_city=home_city,
            team_type=TeamType(team_type),
            position=PlayerPosition(position),
        )
        self.load_data()

    def search_by_name_birth(self, name_part=None, birth_date=None):
        name_part = name_part.strip() if name_part else None
        return Crud.search_by_name_or_birth(name_part, birth_date)

    def search_by_position_team_type(self, position=None, team_type=None):
        position = position.strip() if position else None
        team_type = team_type.strip() if team_type else None
        return Crud.search_by_position_or_team_type(
            PlayerPosition(position) if position else None,
            TeamType(team_type) if team_type else None,
        )

    def search_by_team_city(self, team=None, city=None):
        team = team.strip() if team else None
        city = city.strip() if city else None
        return Crud.search_by_team_or_city(team, city)

    def delete_by_name_birth(self, name_part=None, birth_date=None):
        name_part = name_part.strip() if name_part else None
        deleted_count = Crud.delete_by_name_or_birth(name_part, birth_date)
        self.handle_deletion_result(deleted_count)

    def delete_by_position_team_type(self, position=None, team_type=None):
        position = position.strip() if position else None
        team_type = team_type.strip() if team_type else None
        deleted_count = Crud.delete_by_position_or_team_type(
            PlayerPosition(position) if position else None,
            TeamType(team_type) if team_type else None,
        )
        self.handle_deletion_result(deleted_count)

    def delete_by_team_city(self, team=None, city=None):
        team = team.strip() if team else None
        city = city.strip() if city else None
        deleted_count = Crud.delete_by_team_or_city(team, city)
        self.handle_deletion_result(deleted_count)

    def handle_deletion_result(self, deleted_count):
        if deleted_count > 0:
            message = f"Удалено {deleted_count} игроков"
        else:
            message = "Игроки не найдены"
        self.view.open_deleted_count_window(message)
        self.load_data()
