
from pydantic import BaseModel

class OcrResponse(BaseModel):
    imagePath:str
    text:dict