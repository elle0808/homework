# db/engine.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker # 用於建立 SessionLocal
import os # 處理環境變數，解決 Vercel 上的 NameError

# ----------------------------------------------------
# 1. 引擎初始化：根據環境變數決定使用 Postgres 或 SQLite
# ----------------------------------------------------

# 嘗試從 Vercel 環境變數中獲取連線字串
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # 部署到 Vercel 時使用 PostgreSQL
    # SQLAlchemy 需要明確指定驅動 'postgresql+psycopg2'
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

    # 創建引擎
    engine = create_engine(
        DATABASE_URL, 
        pool_pre_ping=True,
        # Vercel 環境不需要 check_same_thread
    )
    print("Using PostgreSQL")
else:
    # 本地開發時使用 SQLite
    SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        # SQLite 專用參數：允許跨執行緒存取
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )
    print("Using SQLite")

# ----------------------------------------------------
# 2. 資料庫會話 (Session) 管理
# ----------------------------------------------------

# 創建本地會話工廠
# 這個工廠會使用上面定義的 engine 來建立新的 Session 實例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------------------------------------------
# 3. 依賴注入函數 (解決 ImportError: cannot import name 'get_db')
# ----------------------------------------------------

# FastAPI 依賴注入函數，用於每個請求建立/關閉資料庫連線
def get_db():
    """
    獲取一個新的資料庫 Session 實例並在請求完成後關閉它。
    """
    db = SessionLocal()
    try:
        # 將 Session 實例交給 FastAPI 路由函數
        yield db
    finally:
        # 確保連線被關閉，釋放資源
        db.close()

# 注意：當您部署到 Vercel 時，請確保已在 Vercel 環境變數中設置 DATABASE_URL，
# 並且您的 requirements.txt 中包含 psycopg2-binary。
