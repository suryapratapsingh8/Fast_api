from fastapi import APIRouter, Depends, HTTPException
from typing import List
from blog import schemas, models, hashing
from sqlalchemy.orm import Session
from blog.database import get_db


router = APIRouter(tags = ["authentication"])

@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
         raise HTTPException(status_code=404, detail="User not found")

    # Verify the provided password against the stored hash
    if not hashing.Hash.verify(request.password, user.password):
         raise HTTPException(status_code=404, detail="Password is incorrect")

    return user