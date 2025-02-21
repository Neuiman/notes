from fastapi import APIRouter, Depends

from src.auth.enums import Rights
from src.auth.token_heandlers import get_current_user
from src.notes.exceptions import access_exception
from src.notes.services import Service, AdminService

from src.auth.service import UserService

"""
- Восстановить удаленную заметку; 
- Получить конкретную заметку; 
- Получить список всех заметок; 
- Получить список всех заметок конкретного пользователя;"""

router = APIRouter()


@router.get("/user/{user_id}")
async def get_notes_by_user(user_id: int,
                            service: AdminService,
                            user_service: UserService,
                            current_user_id: int = Depends(get_current_user)):

    status = await user_service.get_user_status_by_id(current_user_id)

    is_admin = status == Rights.admin

    if not is_admin:
        return access_exception

    return await service.get_note_list_by_user(user_id, current_user_id)


@router.get("/{note_id}")
async def get_note_by_id(note_id: int, service: AdminService,
                         user_service: UserService,
                         current_user_id: int = Depends(get_current_user) ):

    status = await user_service.get_user_status_by_id(current_user_id)

    is_admin = status == Rights.admin

    if not is_admin:
        return access_exception

    return await service.get_note_by_id(note_id, current_user_id)

@router.patch("/{note_id}")
async def restore_note_by_id(note_id: int,
                             service: AdminService,
                             user_service: UserService,
                             current_user_id: int = Depends(get_current_user)
                             ):

    status = await user_service.get_user_status_by_id(current_user_id)

    if not status == Rights.admin:
        return access_exception

    return await service.restore_note(note_id, current_user_id)

@router.get("/")
async def get_all_notes(service: AdminService,
                        user_service: UserService,
                        current_user_id: int = Depends(get_current_user)
                        ):
    status = await user_service.get_user_status_by_id(current_user_id)

    if not status == Rights.admin:
        return access_exception

    return await service.get_all_notes(current_user_id)

