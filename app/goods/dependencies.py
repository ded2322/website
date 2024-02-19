import shutil

from fastapi import UploadFile
def upload_image(file:UploadFile)->str:
    file_location = f"/static/images/{file.filename}"
    with open(f"app/static/images/{file.filename}","wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    return file_location