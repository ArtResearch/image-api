from fastapi import FastAPI
from .routes.reverse_hash import router as reverse_hash_router
from .routes.image_processing import router as image_processing_router
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()  # Load environment variables
print("Loaded THUMBNAIL_BASE_URL:", os.getenv('THUMBNAIL_BASE_URL'))

app = FastAPI()

app.include_router(reverse_hash_router)
app.include_router(image_processing_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)