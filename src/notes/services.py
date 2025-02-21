from typing import Annotated

from fastapi import Depends

from src.logger import logger
from src.notes.exceptions import access_exception, not_found_exception
from src.notes.repository import Repository
from src.notes.schemas import NoteCreateSchema, NoteUpdateSchema, NoteCreatorSchema


class NoteService:

    def __init__(self, repository: Repository):
        self.repository = repository

    async def get_all_notes(self, user_id: int):

        notes = await self.repository.get_all_notes()
        note_list = [row.to_read_model() for row in notes if row.to_read_model().created_by == user_id
                     and not row.to_read_model().is_delete]

        logger.info(f"пользователь с id = {user_id} просмотрел все свои заметки")

        return note_list

    async def add_note(self, note: NoteCreateSchema, user_id: int):

        new_note = NoteCreatorSchema(**note.model_dump(), created_by=user_id).model_dump()

        result = await self.repository.add_note(new_note)

        logger.info(f"пользователь с id = {user_id} добавил заметку")

        return result

    async def update_note(self, change_note: NoteUpdateSchema, user_id: int):

        updated_note = change_note.model_dump()

        note = await self.repository.get_note_by_id(updated_note["id"])

        note = note[0].to_read_model()

        if not note or note.is_delete:
            return not_found_exception

        if note.created_by == user_id:
            result = await self.repository.update_note(updated_note)

            logger.info(f"пользователь с id = {user_id} отредактировал свою заметку с id = {note.id}")

            return result

        return not_found_exception

    async def delete_note(self, note_id: int, user_id: int):

        delete_status = {"is_delete": True}

        note = await self.repository.get_note_by_id(note_id)

        if not note:
            return not_found_exception

        note = note[0].to_read_model()

        if note.is_delete:
            return not_found_exception

        if note.created_by == user_id:
            result = await self.repository.delete_restore_note(note_id, delete_status)

            logger.info(f"пользователь с id = {user_id} удалил заметку с id = {note.id}")

            return result

        return access_exception



    async def get_note_by_id(self, note_id: int, user_id: int):

        note = await self.repository.get_note_by_id(note_id)

        if not note:
            return not_found_exception

        note = note[0].to_read_model()

        if note.is_delete:
            return not_found_exception


        if note.created_by == user_id:

            result = await self.repository.get_note_by_id(note_id)

            logger.info(f"пользователь с id = {user_id} добавил заметку с id = {note_id}")

            return result

        return access_exception


class NoteServiceAdmin:

    def __init__(self, repository: Repository):
        self.repository = repository

    async def get_all_notes(self, user_id: int):

        notes = await self.repository.get_all_notes()

        note_list = [row.to_read_model() for row in notes]

        logger.info(f"администратор с id = {user_id} просмотрел все заметки")

        return note_list


    async def restore_note(self, note_id: int, user_id: int):

        delete_status = {"is_delete": False}

        note = await self.repository.get_note_by_id(note_id)

        if not note:
            return not_found_exception

        note = note[0].to_read_model()

        if not note.is_delete:
            return {"статус": "сообщение не было удалено"}

        result = await self.repository.delete_restore_note(note_id, delete_status)

        logger.info(f"администратор с id = {user_id} востановил заметку id = {note_id}")

        return result


    async def get_note_by_id(self, note_id: int, user_id: int):

        note = await self.repository.get_note_by_id(note_id)

        if not note:
            return not_found_exception

        result = await self.repository.get_note_by_id(note_id)

        logger.info(f"администратор с id = {user_id} просмотрел заметку id = {note_id}")

        return result

    async def get_note_list_by_user(self, user_id: int, current_user_id: int):

        logger.info(f"администратор с id = {current_user_id} просмотрел все заметки пользователя {user_id}")

        return await self.repository.get_note_by_user_id(user_id)




async def get_service(repository: Repository) -> NoteService:

    return NoteService(repository)

Service = Annotated[NoteService, Depends(get_service)]

async def get_admin_service(repository: Repository) -> NoteServiceAdmin:

    return NoteServiceAdmin(repository)

AdminService = Annotated[NoteServiceAdmin, Depends(get_admin_service)]