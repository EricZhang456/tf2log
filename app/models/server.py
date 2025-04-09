from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.utils.server_list import ServerRegions

class Server(db.Model):
    server_addr: Mapped[str] = mapped_column(primary_key=True)
    server_name: Mapped[str]
    location: Mapped[ServerRegions]
    max_players: Mapped[int]
    vanilla: Mapped[bool]
    mvm: Mapped[bool]
