from fastapi import APIRouter, HTTPException
from ..utils.hash_utils import decompress_url

router = APIRouter()

@router.get("/reverse-hash-image-URL/{hash}")
async def reverse_hash_image_url(hash: str):
    try:
        # Check for '.jpg' suffix and remove it if present
        if hash.endswith(".jpg"):
            hash = hash[:-4]

        original_url = decompress_url(hash)
        return {"url": original_url}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid hash")
