from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.engine import get_db
from models.posts import PostDB
from schemas.posts import PostResponse

router = APIRouter(
   prefix='/api/posts',
   tags=['blog posts']
)

@router.get("", response_model=List[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    rows = (
        db.query(PostDB)
         .order_by(PostDB.id.asc())
         .all()
    )
    return rows

@router.get("/{slug}", response_model=PostResponse)
def get_post_by_slug(slug: str, db: Session = Depends(get_db)):
    post = db.scalar(select(PostDB).where(PostDB.slug == slug))
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post