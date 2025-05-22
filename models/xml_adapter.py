import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from models.database import Player, TeamType, PlayerPosition


class XMLAdapter:
    def __init__(self, file_name: str = "models/players.xml"):
        self.xml_file = Path(file_name)

    def set_file(self, file_path: str):
        self.xml_file = Path(file_path)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.xml_file.exists():
            root = ET.Element("players")
            tree = ET.ElementTree(root)
            tree.write(self.xml_file, encoding="utf-8", xml_declaration=True)

    def player_to_dict(self, player: Player) -> dict:
        return {
            "id": str(player.id),
            "full_name": player.full_name,
            "birth_date": player.birth_date.isoformat(),
            "football_team": player.football_team,
            "home_city": player.home_city,
            "team_type": player.team_type.value if player.team_type else "",
            "position": player.position.value if player.position else "",
        }

    def dict_to_player(self, data: Dict) -> Player:
        return Player(
            full_name=data.get("full_name"),
            birth_date=datetime.strptime(data["birth_date"], "%Y-%m-%d").date(),
            football_team=data.get("football_team"),
            home_city=data.get("home_city"),
            team_type=TeamType(data["team_type"]) if data.get("team_type") else None,
            position=PlayerPosition(data["position"]) if data.get("position") else None,
        )

    def add_data(self, player: Player) -> None:
        self._ensure_file_exists()
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        player_elem = ET.SubElement(root, "player")
        for key, value in self.player_to_dict(player).items():
            elem = ET.SubElement(player_elem, key)
            elem.text = str(value)

        tree.write(self.xml_file, encoding="utf-8", xml_declaration=True)

    def get_data(self) -> List[Player]:
        self._ensure_file_exists()
        tree = ET.parse(self.xml_file)
        return [
            self.dict_to_player({child.tag: child.text for child in elem})
            for elem in tree.findall("player")
        ]

    def search(self, **filters) -> List[Player]:
        players = self.get_data()
        return [p for p in players if self._matches_filters(p, filters)]

    def _matches_filters(self, player: Player, filters: dict) -> bool:
        for key, value in filters.items():
            if value is None:
                continue

            if key == "full_name_part":
                if value.lower() not in player.full_name.lower():
                    return False
            elif key == "birth_date":
                if player.birth_date != value:
                    return False
            elif key == "position_or_team_type":
                if not (player.position == value or player.team_type == value):
                    return False
            elif key == "team_or_city":
                if not (player.football_team == value or player.home_city == value):
                    return False
            else:
                if str(getattr(player, key, "")).lower() != str(value).lower():
                    return False
        return True

    def delete(self, **filters) -> int:
        self._ensure_file_exists()
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        to_keep = []
        deleted_count = 0

        for player_elem in root.findall("player"):
            player = self.dict_to_player(
                {child.tag: child.text for child in player_elem}
            )

            if self._matches_filters(player, filters):
                deleted_count += 1
            else:
                to_keep.append(player_elem)

        new_root = ET.Element("players")
        for elem in to_keep:
            new_root.append(elem)

        ET.ElementTree(new_root).write(
            self.xml_file, encoding="utf-8", xml_declaration=True
        )
        return deleted_count
