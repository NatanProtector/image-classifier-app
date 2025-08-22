from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
import uuid

app = FastAPI(title="Image Classifier API", version="1.0.0")

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "server is working"}

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file and store it on the server
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        return {"error": "File must be an image"}
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIR / unique_filename
    
    try:
        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {
            "message": "Image uploaded successfully",
            "filename": unique_filename,
            "original_name": file.filename,
            "file_size": len(content),
            "file_path": str(file_path)
        }
    except Exception as e:
        return {"error": f"Failed to upload image: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
