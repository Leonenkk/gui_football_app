import enum
import os
from sqlalchemy import create_engine, Column, Integer, String, Enum, Date
from sqlalchemy.orm import sessionmaker, declarative_base

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "football_players.db")

engine = create_engine(f"sqlite:///{db_path}", echo=True)
Base = declarative_base()


class PlayerPosition(enum.Enum):
    GOALKEEPER = "Вратарь"
    DEFENDER = "Защитник"
    MIDFIELDER = "Полузащитник"
    FORWARD = "Нападающий"


class TeamType(enum.Enum):
    MAIN = "основной"
    RESERVE = "запасной"
    NA = "n/a"


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    birth_date = Column(Date, nullable=False)
    football_team = Column(String(100))
    home_city = Column(String(50))
    team_type = Column(Enum(TeamType))
    position = Column(Enum(PlayerPosition))


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
