from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import models, database, auth
import shutil, os
from ..config import UPLOAD_DIR

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ops/create-user")
def create_user(db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter_by(email="ops@example.com").first()
    if existing_user:
        return {"message": "User already exists"}
    new_user = models.User(
        email="ops@example.com",
        password="1234",     # plain password
        role="ops",
        is_verified=True
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@router.post("/ops/login")
def login(email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=email, password=password, role="ops").first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = auth.create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token}

@router.post("/ops/upload")
def upload_file(token: str = Form(), file: UploadFile = File(...), db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    if not payload or payload["role"] != "ops":
        raise HTTPException(status_code=403, detail="Not allowed")
    if file.filename.split(".")[-1] not in ["docx", "pptx", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    db_file = models.File(filename=file.filename, owner_id=int(payload["sub"]))
    db.add(db_file)
    db.commit()
    return {"message": "File uploaded"}











