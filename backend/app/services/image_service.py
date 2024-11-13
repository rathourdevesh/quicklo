"""Image Service."""
from fastapi import HTTPException, UploadFile
from io import BytesIO
from PIL import Image

from .base_service import BaseService
from app.models.image_model import Images
from app.core.logger_config import logger

class ImageService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def compress_image(self, image_file):
        image = Image.open(image_file)
        img_io = BytesIO()
        image.save(img_io, "JPEG", optimize=True, quality=50)
        return img_io.getvalue()

    async def upload_image(self, file: UploadFile) -> int:
        compressed_image = await self.compress_image(file.file)
        logger.info(f"upload image {file.filename}")
        db_image = Images(filename=file.filename, image_data=compressed_image)
        self.session.add(db_image)
        self.session.commit()
        self.session.refresh(db_image)
        return db_image.id

    async def get_image_by_id(self, image_id: int) -> BytesIO:
        db_image = self.session.query(Images).filter(Images.id == image_id).first()
        logger.info(f"upload image {db_image.filename}")
        if not db_image:
            raise HTTPException(status_code=400, detail="Image not found")

        # Decompress image
        image_data = BytesIO(db_image.image_data)
        return image_data

