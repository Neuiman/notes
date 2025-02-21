from typing import Annotated

from fastapi import Depends
from sqlalchemy import Select, Insert, Delete, Update

from src.database import connection

from src.notes.models import Note


class NoteRepository:

    @connection
    async def add_note(self, note: dict, session):

        stmt = Insert(Note).values(**note)
        result = await session.execute(stmt)
        await session.commit()

        return "add was successful"

    @connection
    async def get_note_by_id(self, note_id: int, session):

        stmt = Select(Note).where(Note.id == note_id)
        notes = await session.execute(stmt)

        note = [row[0] for row in notes.all()]

        return note

    @connection
    async def delete_restore_note(self, note_id: int, delete_status: dict, session):

        stmt = Update(Note).where(Note.id == note_id).values(**delete_status)

        await session.execute(stmt)


        await session.commit()

        return "delete was successful"

    @connection
    async def update_note(self, note: dict, session):
        stmt = (
            Update(Note).
            where(Note.id == note.get("id")).
            values(note).
            returning(Note)
        )
        result = await session.execute(stmt)
        await session.commit()

        changed_note = [row[0] for row in result.all()][0]
        # logging.info(result.first())
        return changed_note

    @connection
    async def get_all_notes(self, session):

        stmt = Select(Note)
        notes = await session.execute(stmt)

        notes = [row[0] for row in notes.all()]

        return notes

    @connection
    async def get_note_by_user_id(self, user_id: int, session):

        stmt = Select(Note).where(Note.created_by == user_id)
        notes = await session.execute(stmt)

        notes = [row[0] for row in notes.all()]

        return notes



async def get_repository() -> NoteRepository:
    return NoteRepository()

Repository = Annotated[NoteRepository, Depends(get_repository)]
