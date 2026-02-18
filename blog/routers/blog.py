from fastapi import APIRouter, Depends, HTTPException
from typing import List
from blog import schemas, models
from sqlalchemy.orm import Session
from blog.OAuth2 import get_current_user
from blog.database import get_db

router = APIRouter(
    prefix= '/blog',
    tags=["blogs"])

@router.get("/", response_model=List[schemas.Blog])
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post("/")
def create_blog(request: schemas.BlogCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete("/{id}")
def remove_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted successfully"}

@router.put("/{id}")
def update_blog(id: int, request: schemas.BlogCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return {"detail": "Blog updated successfully"}

@router.get("/{id}", response_model=schemas.Blog)
def show(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog