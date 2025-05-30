from fastapi import UploadFile
from ..dtos.OcrResponse import OcrResponse
from ..model.ocr_process import OcrProcess
from .ocr_service import OcrService
from .groq_service import GroqService
from .upload_service import UploadService

class GatewayService:

    def __init__(self, ocr_service: OcrService, groq_service: GroqService, upload_service: UploadService):
        self.ocrService = ocr_service
        self.groqService = groq_service
        self.uploadService = upload_service
    
    async def ocrProcess(self,urlImage:str)-> OcrResponse:
        extractData:OcrProcess = await self.ocrService.doOcrFromImageUrl(urlImage)
        textFromGroq:str =  self.groqService.getJsonFromOcrText(extractData.text) 
        textToJson:dict = GroqService.extract_json_from_text(textFromGroq)
        imageId:str =  self.uploadService.upload_image(extractData.imageProccesed)["imageId"]
        
        return OcrResponse(imagePath=imageId,text=textToJson)
        
        
        