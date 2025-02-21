from fastapi import APIRouter, Depends

from src.auth.token_heandlers import get_current_user
from src.notes.schemas import NoteCreateSchema, NoteSchema, NoteUpdateSchema
from src.notes.services import Service

router = APIRouter()

"""
- Cоздать заметку;
- Изменить заметку;
- Удалить заметку;
- Получать список всех заметок;
- Получать конкретную заметку;"""

@router.post("/")
async def add_new_note(note: NoteCreateSchema, service: Service, user_id: int = Depends(get_current_user)):
    saved_note = await service.add_note(note, user_id)

    return saved_note


@router.put("/")
async def update_note(note: NoteUpdateSchema,service: Service, user_id: int = Depends(get_current_user)):

    return await service.update_note(note, user_id)

@router.delete("/")
async def delete_note(note_id: int, service: Service, user_id = Depends(get_current_user)):

    return await service.delete_note(note_id, user_id)


@router.get("/")
async def get_all_notes(service: Service, user_id = Depends(get_current_user)):
    return await service.get_all_notes(user_id)


@router.get("/{note_id}")
async def get_note_by_id(note_id: int, service: Service, user_id = Depends(get_current_user)):

    return await service.get_note_by_id(note_id, user_id)
