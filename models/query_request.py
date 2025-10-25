from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    video_id: str