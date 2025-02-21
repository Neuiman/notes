from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.notes.schemas import NoteSchema

Base = declarative_base()


class Note(Base):

    __tablename__ = "note"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[int]
    title: Mapped[str]
    body: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    is_delete: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self):
        return NoteSchema(id = self.id,
        created_by = self.created_by,
        title = self.title,
        body = self.body,
        created_at = self.created_at,
        is_delete = self.is_delete)





