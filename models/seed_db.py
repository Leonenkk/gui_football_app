# seed_db.py

from faker import Faker
from random import choice
from datetime import date, timedelta
from models.database import Session, Player, TeamType, PlayerPosition


def random_birthdate(start_year=1985, end_year=2007):
    """Вернёт случайную дату между 1 января start_year и 31 декабря end_year."""
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta_days = (end - start).days
    return start + timedelta(days=Faker().random_int(min=0, max=delta_days))


def main(n=100):
    fake = Faker("ru_RU")  # русская локализация для ФИО
    teams = [
        "Динамо",
        "Спартак",
        "Зенит",
        "Рубин",
        "ЦСКА",
        "Локомотив",
        "Урал",
        "Ростов",
        "Ахмат",
        "Оренбург",
    ]
    cities = [
        "Минск",
        "Брест",
        "Новолукомль" "Москва",
        "Санкт-Петербург",
        "Казань",
        "Самара",
        "Ростов-на-Дону",
        "Краснодар",
        "Уфа",
        "Челябинск",
        "Волгоград",
        "Нижний Новгород",
    ]
    session = Session()

    for _ in range(n):
        full_name = fake.name()

        player = Player(
            full_name=full_name,
            birth_date=random_birthdate(1985, 2007),
            football_team=choice(teams),
            home_city=choice(cities),
            team_type=choice(list(TeamType)),
            position=choice(list(PlayerPosition)),
        )
        session.add(player)

    session.commit()
    print(f"Добавлено {n} записей в таблицу players")


if __name__ == "__main__":
    main(50)
