from transformers import pipeline

class Engine:
    def __init__(self):
        self.generator = pipeline('text-generation', model='distilgpt2')

    def generate_text(self, prompt, max_length=100):
        generated_text = self.generator(prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']
        return generated_text