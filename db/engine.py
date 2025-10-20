# db/engine.py (修改後)

from sqlalchemy import create_engine
import os # 需要導入 os 模組

# 檢查環境變數
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # 部署到 Vercel 時使用 Postgres
    # 注意：SQLAlchemy 需要將 postgresql:// 轉換為 postgresql+psycopg2://
    if DATABASE_URL.startswith("postgresql://"):
         DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
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

# 注意：這裡的 print 語句只是為了在 Vercel Log 中確認使用哪個資料庫
