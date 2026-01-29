#from multiprocessing import context
#from concurrent import futures

from transformers import pipeline, MarianMTModel, MarianTokenizer

class TranslatorService:
    def __init__(self, model_name: str):
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_name)
        # optional warm-up
        self.model.generate(**self.tokenizer("warmup", return_tensors="pt"))

    def translate(self, text: str) -> str:
        tokens = self.tokenizer(text, return_tensors="pt", padding=True)
        output = self.model.generate(**tokens)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
    


translator_service = TranslatorService(model_name="Helsinki-NLP/opus-mt-uk-pl")
