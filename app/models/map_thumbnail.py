from app.extensions import db
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class map_thumbnail(db.Model):
    map_name: Mapped[str] = mapped_column(primary_key=True)
    map_thumbnail_url: Mapped[str] = mapped_column()
