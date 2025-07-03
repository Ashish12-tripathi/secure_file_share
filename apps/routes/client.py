from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from .. import models, database, auth, utils
import os
from fastapi.responses import FileResponse

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/client/signup")
def signup(email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = models.User(email=email, password=password, role="client")
    db.add(new_user)
    db.commit()
    utils.mock_send_email(email)
    encrypted = utils.encrypt_url(new_user.id)
    return {"encrypted_url": f"/client/download-file/{encrypted}"}

@router.get("/client/verify-email")
def verify_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified"}

@router.post("/client/login")
def login(email: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=email, password=password, role="client").first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = auth.create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token}

@router.get("/client/list-files")
def list_files(token: str, db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    if not payload or payload["role"] != "client":
        raise HTTPException(status_code=403, detail="Access denied")
    files = db.query(models.File).all()
    return {"files": [f.filename for f in files]}

@router.get("/client/download-file/{encrypted_id}")
def download_file(encrypted_id: str, token: str, db: Session = Depends(get_db)):
    payload = auth.verify_token(token)
    if not payload or payload["role"] != "client":
        raise HTTPException(status_code=403, detail="Access denied")
    file_id = utils.decrypt_url(encrypted_id)
    file = db.query(models.File).filter_by(id=file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(os.path.join("files", file.filename))