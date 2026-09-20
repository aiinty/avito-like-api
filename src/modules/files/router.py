from fastapi import APIRouter, Depends, UploadFile
from fastapi.concurrency import run_in_threadpool
from src.config import config
from src.modules.auth.schemas import CurrentUser
from src.modules.files.schemas import UploadResponse
from src.utils.auth import get_current_user
from src.utils.files import save_image_sync
from src.utils.exceptions import ValidationError


files_router = APIRouter(prefix="/upload", tags=["File Uploads"])

@files_router.post("", response_model=UploadResponse)
async def upload_image(
    file: UploadFile,
    current_user: CurrentUser = Depends(get_current_user),
) -> UploadResponse:
    if file.size > config.FILE_MAX_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File size is greater than {config.FILE_MAX_SIZE_MB} MB")
    
    url = await run_in_threadpool(
        save_image_sync, file.file, str(current_user.id)
    )
    return UploadResponse(url=url)
