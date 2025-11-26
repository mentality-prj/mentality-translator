from translate_pb2 import TranslateResponse
from translate_pb2_grpc import TranslatorServicer

class TranslatorService(TranslatorServicer):
    async def Translate(self, request, context):
        text = request.text
        lang = request.target_lang

        # TODO: тут виклик моделі
        result = f"{text} -> translated to {lang}"

        return TranslateResponse(translated_text=result)
