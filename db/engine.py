# api/engine.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time # 假設您的引擎需要一些時間運行

# --------------------------
# 1. 定義應用程式入口點
# --------------------------
# Vercel 將尋找這個 'app' 變數來啟動您的應用程式
app = FastAPI()

# --------------------------
# 2. 定義輸入/輸出模型 (Pydantic)
# --------------------------
class EngineInput(BaseModel):
    prompt: str
    max_tokens: int = 100

class EngineOutput(BaseModel):
    status: str
    processed_text: str
    latency_ms: float
    model_version: str = "v1.0"


# --------------------------
# 3. 您的「引擎」核心邏輯
# --------------------------
def run_core_engine(input_data: EngineInput) -> str:
    """
    這裡實現您的主要業務邏輯。
    可以是模型推理、複雜計算、資料庫查詢等等。
    """
    
    if len(input_data.prompt) < 5:
        raise ValueError("Prompt too short!")

    # 模擬複雜計算
    processed = f"Engine processed: {input_data.prompt.upper()[:input_data.max_tokens]}..."
    
    return processed

# --------------------------
# 4. 定義 API 端點
# --------------------------

# 預設路徑 (可選)
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Engine on Vercel!"}

# 您的主要引擎 API 端點
@app.post("/api/run-engine", response_model=EngineOutput)
async def run_engine(input_data: EngineInput):
    start_time = time.time()
    
    try:
        # 運行核心邏輯
        processed_result = run_core_engine(input_data)
        
        end_time = time.time()
        latency = (end_time - start_time) * 1000 # 轉換為毫秒
        
        return EngineOutput(
            status="success",
            processed_text=processed_result,
            latency_ms=latency
        )
        
    except ValueError as e:
        # 處理邏輯中的錯誤
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 處理其他意外錯誤
        raise HTTPException(status_code=500, detail=f"Internal engine error: {str(e)}")


# --------------------------
# 5. ⚠️ 本地測試啟動方式 (Vercel 部署時無需執行)
# --------------------------
# 由於 Vercel 會自動處理服務器啟動，這個區塊在部署時會被忽略。
# 但它對於在本地使用 `uvicorn api.engine:app --reload` 進行測試非常有用。
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
