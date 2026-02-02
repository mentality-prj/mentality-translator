import os
from transformers import pipeline, MarianMTModel, MarianTokenizer

class TranslatorService:
    def __init__(self, model_name: str):

        model_path = ".models/" + model_name.split("/")[-1] # ".models/opus-mt-uk-pl"
        self.tokenizer = MarianTokenizer.from_pretrained(model_path, local_files_only=True)
        self.model = MarianMTModel.from_pretrained(model_path, local_files_only=True)

        # optional warm-up
        self.model.generate(**self.tokenizer("warmup", return_tensors="pt"))
        #responce = self.translate("warmup")

    def translate(self, text: str) -> str:
        tokens = self.tokenizer(text, return_tensors="pt", padding=True)
        output = self.model.generate(**tokens)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
    

