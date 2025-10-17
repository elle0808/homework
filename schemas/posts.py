from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    """Post 的基本結構"""
    slug: str
    title: str
    author: str
    content: str
    image_url: str

class PostResponse(PostBase):
    """回應用的 Post 結構，包含 ID"""
    # 支援 ORM 模式
    model_config = ConfigDict(from_attributes=True)  
    
    id: int