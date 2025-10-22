# db/engine.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os # 處理環境變數

# ----------------------------------------------------
# 1. 引擎初始化：使用最可靠的連線字串處理
# ----------------------------------------------------

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Vercel 部署到 PostgreSQL
    
    # 確保 SQLAlchemy 使用 psycopg2 驅動，這是 Vercel 上最可靠的方式。
    # 這裡只替換協議頭，不檢查 postgres:// 或 postgresql://
    if "://" in DATABASE_URL:
        # 將協議頭 (如 postgres://) 替換為 postgresql+psycopg2://
        driver, url = DATABASE_URL.split("://", 1)
        DATABASE_URL = f"postgresql+psycopg2://{url}"

    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True
    )
    print("Using PostgreSQL")
else:
    # 本地開發時使用 SQLite
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
    print("Using SQLite")

# ----------------------------------------------------
# 2. 資料庫會話 (Session) 管理 (這部分不變)
# ----------------------------------------------------

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
