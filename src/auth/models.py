from datetime import datetime


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.auth.enums import Rights
from src.auth.schemas import UserSchema

Base = declarative_base()


class User(Base):

    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    status: Mapped[Rights]
    email: Mapped[str]


    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id = self.id,
            name = self.name,
            status = self.status,
            email=self.email,
            hashed_password = self.hashed_password,
            created_at = self.created_at
        )




