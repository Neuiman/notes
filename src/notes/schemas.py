from datetime import datetime

from pydantic import BaseModel, Field


class NoteCreateSchema(BaseModel):

    title: str = Field(max_length=256, description="заголовок должен содержать не более 256 символов")
    body: str = Field(max_length=65536, description="тело заметки должно содержать не более 65536 символов")


class NoteCreatorSchema(NoteCreateSchema):
    created_by: int



class NoteSchema(BaseModel):
    id: int
    created_by: int
    title: str
    body: str
    created_at: datetime
    is_delete: bool


class NoteUpdateSchema(BaseModel):
    id: int
    title: str
    body: str


