from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select

from db.engine import get_db
from models.posts import PostDB
from schemas.posts import PostResponse, LikeAction, CommentCreate

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

@router.post("/{slug}/like")
def toggle_like(
    slug: str,
    action_data: LikeAction, # 接收前端傳來的 { "action": "like" }
    db: Session = Depends(get_db)
):
    # 1. 查找文章
    post = db.scalar(select(PostDB).where(PostDB.slug == slug))
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 2. 處理點讚邏輯
    if action_data.action == "like":
        # 假設您的 PostDB 有 likes 欄位
        post.likes = (post.likes or 0) + 1 
    elif action_data.action == "unlike":
        post.likes = max(0, (post.likes or 0) - 1) # 確保 likes 不會小於 0

    db.commit() # 儲存變更
    db.refresh(post) # 刷新物件以獲取最新的計數

    # 必須返回 likes 計數
    return {"likes": post.likes} 


# ----------------------------------------------------
## 留言 (Comment) 路由
# ----------------------------------------------------
@router.post("/{slug}/comment")
def add_comment(
    slug: str, 
    comment_data: CommentCreate, # 接收前端傳來的 { "user": "...", "content": "..." }
    db: Session = Depends(get_db)
):
    # 1. 查找文章 (確保文章存在，也可以順便獲取該文章的留言列表)
    post = db.scalar(select(PostDB).where(PostDB.slug == slug))
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 2. 【TODO】這裡應該是新增留言到資料庫的邏輯
    # 為了測試前端，我們暫時返回一個模擬的成功數據
    
    # 3. 必須返回完整的 comments 列表，以供前端渲染
    # 由於您可能還沒有留言模型，這裡返回一個包含新留言的模擬列表
    # 假設您的 postData JSON 結構中，留言是 comments 列表
    
    # 請根據您實際的數據庫模型來獲取最新的留言列表
    # 這裡返回一個包含新留言的模擬列表給前端
    updated_comments = [
        {"user": comment_data.user, "content": comment_data.content, "date": "剛剛"},
        # 【重要】這裡應該是從資料庫獲取所有現有留言
    ]
    
    # 注意：您的前端要求返回的數據中包含 likes 和 comments
    # 所以我們返回一個包含兩者的結構，或者只返回 comments 讓前端自己更新
    
    # 為了符合前端的 data.comments 和 data.likes 邏輯，我們返回完整結構：
    return {
        "likes": post.likes or 0, 
        "comments": updated_comments # 替換成從資料庫獲取的所有留言
    }