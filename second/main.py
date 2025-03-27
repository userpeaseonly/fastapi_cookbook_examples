import shutil
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, field_validator



app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    field_validator("age")
    def check_age(cls, value):
        if value < 18 or value > 100:
            raise ValueError("Age must be between 18 and 100")
        return value
    

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.post("/download-file/{filename}", response_class=FileResponse)
async def upload_file(filename: str):
    if not Path(f"uploads/{filename}").exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(f"uploads/{filename}")