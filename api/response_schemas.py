from pydantic import BaseModel
from typing import Dict, List, Optional


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class IntermediateConfidenceData(BaseModel):
    cluster: int
    images: List[str]

    class config:
        orm_mode = True

class UploadImageResponse(BaseModel):
    high_confidence: List[str]
    intermediate_confidence: Optional[Dict[int, IntermediateConfidenceData]]
    message: Optional[str]

    class config:
        orm_mode = True

class ClusterSamplesResponseData(BaseModel):
    cluster: int
    sample_url: str
    images: List[str]

    class config:
        orm_mode = True

ClusterSamplesResponse = Dict[int, ClusterSamplesResponseData]

class UserResultsResponse(BaseModel):
    image_urls: List[str]

    class Config:
        orm_mode = True