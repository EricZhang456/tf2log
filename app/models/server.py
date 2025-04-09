from app.extensions import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Server(db.Model):
    server_steam_id: Mapped[int] = mapped_column(primary_key=True)
    server_name: Mapped[str]
    server_map: Mapped[str]
    max_players: Mapped[int]
    vac: Mapped[bool]
    vanilla: Mapped[bool]
    sourcetv: Mapped[bool]
