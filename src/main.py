from fastapi import FastAPI

from src.notes.routers.adminRouter import router as admin_router
from src.notes.routers.userRouter import router as user_router

from src.auth.router import router as auth_router
app = FastAPI()

app.include_router(admin_router, prefix="/note/admin", tags =["note_admin"])
app.include_router(user_router, prefix="/note/user", tags=["user"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
