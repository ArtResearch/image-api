from fastapi import APIRouter, HTTPException
from ..models import ImageUrl
import requests
from PIL import Image
from io import BytesIO
from ..utils.hash_utils import compress_url
import os
from datetime import datetime
import logging

router = APIRouter()

# Configure logger
logger = logging.getLogger("uvicorn")

# Ensure required directories exist
os.makedirs("image-data/originals", exist_ok=True)
os.makedirs("image-data/200px", exist_ok=True)
os.makedirs("image-data/1000px", exist_ok=True)
os.makedirs("image-data/image-RDF-data", exist_ok=True)

@router.post("/process-image")
async def process_image(image_data: ImageUrl):
    image_url = image_data.image_url
    hashed_url = compress_url(image_url)
    date_processed = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    error_description = ""
    thumbnail_path = ""

    try:
        response = requests.get(image_url, allow_redirects=True)
        http_status_code = response.status_code
        logger.info(f"Response status code: {response.status_code}, Processing image: {image_url}, Hashed URL: {hashed_url}")

        if http_status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
            image = Image.open(BytesIO(response.content))
            image.save(f"image-data/originals/{hashed_url}.jpg")

            # Generate thumbnails
            for size, folder in [(200, "200px"), (1000, "1000px")]:
                thumbnail = image.copy()
                thumbnail.thumbnail((size, size))
                thumbnail.save(f"image-data/{folder}/{hashed_url}.jpg")
            
            thumbnail_base_url = os.getenv('THUMBNAIL_BASE_URL', 'default/base/url/if/not/set/in/env')
            thumbnail_path = f"<{image_url}> <https://artresearch.net/image-api/image-api:thumbnail> <{thumbnail_base_url}200px/{hashed_url}.jpg> ."

        else:
            error_description = f"Error in downloading image: HTTP status {http_status_code}. {response.reason}"

    except requests.exceptions.RequestException as e:
        http_status_code = 500  # Internal Server Error
        error_description = f"Request Exception: {str(e)}"

    # Generate RDF file
    rdf_error_line = f"<{image_url}> <https://artresearch.net/image-api/image-api:error-description> \"{error_description}\" ." if error_description else ""
    with open("data/image-data-model.nt", "r") as model_file:
        rdf_template = model_file.read()

    rdf_content = rdf_template.format(image_url=image_url, hashed_url=hashed_url, 
                                      date_processed=date_processed, http_status_code=http_status_code,
                                      thumbnail_path=thumbnail_path, error_description=rdf_error_line)

    with open(f"image-data/image-RDF-data/{hashed_url}.nt", "w") as rdf_file:
        rdf_file.write(rdf_content)

    if error_description:
        return {"status": "error", "code": http_status_code, "detail": error_description}
    else:
        return {"status": "success", "hashed_url": hashed_url}
