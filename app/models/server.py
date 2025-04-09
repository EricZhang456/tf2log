from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.utils.server_list import ServerRegions

class Server(db.Model):
    server_steam_id: Mapped[int] = mapped_column(primary_key=True)
    server_ip = Mapped[str]
    server_port = Mapped[int]
    server_name: Mapped[str]
    server_map: Mapped[str]
    location: Mapped[ServerRegions]
    max_players: Mapped[int]
    vac: Mapped[bool]
    vanilla: Mapped[bool]
    sourcetv: Mapped[bool]
