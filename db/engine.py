import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. 確保從環境變數中讀取 DATABASE_URL
# 如果 Vercel 中設定了 DATABASE_URL，則使用它；否則回退到一個預設值（例如本地 SQLite）
# 注意：在 Vercel 上，這個變數必須指向外部資料庫
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # ⚠️ 警告：如果在 Vercel 上沒有設置，這將導致失敗。
    # 這是為了本地開發而設置的 SQLite 備份。
    DATABASE_URL = "sqlite:///./app.db"
    
    # 如果是本地 SQLite，需要設置 check_same_thread=False
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    print("Warning: Using local SQLite database.") # 這行會出現在 Runtime Logs if it's run
else:
    # 針對 Supabase (PostgreSQL) 外部資料庫
    # SQLAlchemy 的連線字串需要使用 'postgresql' 作為驅動，
    # 確保連線字串是正確的格式，例如：postgresql://...
    engine = create_engine(DATABASE_URL)
    print(f"Connecting to external database using: {DATABASE_URL[:20]}...")

# 創建 SessionLocal 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    """產生資料庫 Session，供 FastAPI Dependency 使用"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

__all__ = ["engine", "SessionLocal", "get_db"]

