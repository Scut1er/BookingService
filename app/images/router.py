from fastapi import UploadFile, APIRouter
import aiofiles

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Images loading"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file_to_upload: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    async with aiofiles.open(im_path, "wb+") as file_object:
        file = await file_to_upload.read()
        await file_object.write(file)
        process_pic.delay(im_path)
