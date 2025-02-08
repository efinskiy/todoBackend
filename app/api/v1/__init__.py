from fastapi import APIRouter
from .auth.router import router as auth
from .task.router import router as tasks

router = APIRouter(prefix="/api/v1")

router.include_router(auth)
router.include_router(tasks)
