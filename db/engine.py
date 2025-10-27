import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ⚠️ 1. 設置資料庫連線 URL
# 在 Vercel 環境變數中設置 DATABASE_URL，用於連線到外部資料庫
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./app.db")

# ⚠️ 2. 確定連線器類型
# 為了讓 Vercel 穩定運行，我們強烈建議使用外部資料庫
if DATABASE_URL.startswith("sqlite"):
    # 如果是 SQLite，需要設置 check_same_thread=False
    # 但請注意，本地 SQLite 在 Vercel 上無法寫入
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # 針對 PostgreSQL, MySQL 等外部資料庫
    engine = create_engine(DATABASE_URL)

# 創建 SessionLocal 類別
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 為了讓 main.py 正常導入，確保 engine 變數被導出
__all__ = ["engine", "SessionLocal"]
