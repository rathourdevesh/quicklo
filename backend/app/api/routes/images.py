from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import StreamingResponse

from app.db.conn import get_db_session
from app.services.image_service import ImageService

router = APIRouter()

@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    image_service: ImageService = Depends(lambda: ImageService(session=next(get_db_session())))
):
    """Upload image."""
    image_id: int = await image_service.upload_image(file)
    return {
        "success": True,
        "image_id": image_id,
        "message": "image uploaded successfully."
    }


@router.get("/view/{image_id}")
async def view_image(
    image_id: int,
    image_service: ImageService = Depends(lambda: ImageService(session=next(get_db_session())))
):
    """Find image by id."""
    image_data = await image_service.get_image_by_id(image_id)
    return StreamingResponse(image_data, media_type="image/jpeg")
