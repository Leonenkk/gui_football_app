from models.database import Session, Player, TeamType, PlayerPosition
from models.xml_adapter import XMLAdapter
from sqlalchemy import and_, or_
from datetime import date


class Crud:
    data_source = "db"
    xml_adapter = XMLAdapter()

    @staticmethod
    def set_data_source(source: str):
        Crud.data_source = source

    @staticmethod
    def change_xml_file(file_path: str):
        Crud.xml_adapter = XMLAdapter(file_path)

    @staticmethod
    def add_data(
        full_name: str,
        birth_date: date,
        football_team: str,
        home_city: str,
        team_type: TeamType,
        position: PlayerPosition,
    ):
        new_player = Player(
            full_name=full_name,
            birth_date=birth_date,
            football_team=football_team,
            home_city=home_city,
            team_type=team_type,
            position=position,
        )

        if Crud.data_source == "db":
            with Session() as session:
                session.add(new_player)
                session.commit()
        else:
            Crud.xml_adapter.add_data(new_player)

    @staticmethod
    def get_data():
        if Crud.data_source == "db":
            with Session() as session:
                return session.query(Player).all()
        else:
            return Crud.xml_adapter.get_data()

    @staticmethod
    def search_by_name_or_birth(name_part: str = None, birth_date: date = None):
        if Crud.data_source == "db":
            with Session() as session:
                query = session.query(Player)
                filters = []

                if name_part:
                    filters.append(Player.full_name.ilike(f"%{name_part}%"))
                if birth_date:
                    filters.append(Player.birth_date == birth_date)

                if filters:
                    query = query.filter(or_(*filters))
                return query.all()
        else:
            filters = {}
            if name_part:
                filters["full_name_part"] = name_part
            if birth_date:
                filters["birth_date"] = birth_date
            return Crud.xml_adapter.search(**filters)

    @staticmethod
    def search_by_position_or_team_type(
        position: PlayerPosition = None, team_type: TeamType = None
    ):
        if Crud.data_source == "db":
            with Session() as session:
                query = session.query(Player)
                filters = []

                if position:
                    filters.append(Player.position == position)
                if team_type:
                    filters.append(Player.team_type == team_type)

                if filters:
                    query = query.filter(or_(*filters))
                return query.all()
        else:
            return Crud.xml_adapter.search(position_or_team_type=position or team_type)

    @staticmethod
    def search_by_team_or_city(team: str = None, city: str = None):
        if Crud.data_source == "db":
            with Session() as session:
                query = session.query(Player)
                filters = []

                if team:
                    filters.append(Player.football_team.ilike(f"%{team}%"))
                if city:
                    filters.append(Player.home_city.ilike(f"%{city}%"))

                if filters:
                    query = query.filter(or_(*filters))
                return query.all()
        else:
            return Crud.xml_adapter.search(team_or_city=team or city)

    @staticmethod
    def delete_by_name_or_birth(name_part: str = None, birth_date: date = None):
        if not name_part and not birth_date:
            return 0

        if Crud.data_source == "db":
            with Session() as session:
                query = session.query(Player)
                filters = []

                if name_part:
                    filters.append(Player.full_name.ilike(f"%{name_part}%"))
                if birth_date:
                    filters.append(Player.birth_date == birth_date)

                if filters:
                    query = query.filter(or_(*filters))
                    deleted_count = query.delete(synchronize_session=False)
                    session.commit()
                    return deleted_count
                return 0
        else:
            filters = {}
            if name_part:
                filters["full_name_part"] = name_part
            if birth_date:
                filters["birth_date"] = birth_date
            return Crud.xml_adapter.delete(**filters)

    @staticmethod
    def delete_by_position_or_team_type(
        position: PlayerPosition = None, team_type: TeamType = None
    ):
        if not position and not team_type:
            return 0

        if Crud.data_source == "db":
            with Session() as session:
                query = session.query(Player)
                filters = []

                if position:
                    filters.append(Player.position == position)
                if team_type:
                    filters.append(Player.team_type == team_type)

                if filters:
                    query = query.filter(or_(*filters))
                    deleted_count = query.delete(synchronize_session=False)
                    session.commit()
                    return deleted_count
                return 0
        else:
            return Crud.xml_adapter.delete(position_or_team_type=position or team_type)

    @staticmethod
    def delete_by_team_or_city(team: str = None, city: str = None):
        if not team and not city:
            return 0

        if Crud.data_source == "db":
            with Session() as session:
                query = session.query(Player)
                filters = []

                if team:
                    filters.append(Player.football_team.ilike(f"%{team}%"))
                if city:
                    filters.append(Player.home_city.ilike(f"%{city}%"))

                if filters:
                    query = query.filter(or_(*filters))
                    deleted_count = query.delete(synchronize_session=False)
                    session.commit()
                    return deleted_count
                return 0
        else:
            return Crud.xml_adapter.delete(team_or_city=team or city)
