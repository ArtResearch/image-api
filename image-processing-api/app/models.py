from pydantic import BaseModel

class ImageUrl(BaseModel):
    image_url: str
