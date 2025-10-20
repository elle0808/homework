{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
# db/engine.py (確保這段邏輯存在)

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Vercel 需要明確指定驅動，這裡將 postgresql:// 替換為 postgresql+psycopg2://
    if DATABASE_URL.startswith("postgresql://"):
         DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)

    # 創建引擎
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    # ...
