from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models, hashing
from blog.database import engine, SessionLocal
from typing import List


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", tags=["blogs"])
def create_blog(request: schemas.BlogCreate, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete("/blog/{id}", tags=["blogs"])
def remove_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted successfully"}

@app.put("/blog/{id}", tags=["blogs"])
def update_blog(id: int, request: schemas.BlogCreate, db: Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with id {id} not found")
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return {"detail": "Blog updated successfully"}

@app.get("/blog", response_model=List[schemas.Blog], tags=["blogs"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", response_model=schemas.Blog, tags=["blogs"])
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.post("/User", tags=["users"])
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/User", response_model=List[schemas.User], tags=["users"])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/User/{id}", response_model=schemas.User, tags=["users"])
def show_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/User/{id}", tags=["users"])
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}

# delecting all blog at oncec
@app.delete("/blog", tags=["blogs"])
def delete_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=404, detail="No blogs found")
    db.delete(blogs)
    db.commit()
    return {"detail": "All blogs deleted successfully"}
