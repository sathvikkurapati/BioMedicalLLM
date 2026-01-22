from transformers import BioGptTokenizer, BioGptForCausalLM
import torch

class BioGPTModel:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        print(f"Loading BioGPT model on {self.device}...")
        self.tokenizer = BioGptTokenizer.from_pretrained("microsoft/BioGPT")
        self.model = BioGptForCausalLM.from_pretrained("microsoft/BioGPT")
        self.model.to(self.device)
        print("Model loaded.")
        
    def generate_answer(self, prompt, max_length=200, mock=False):
        if mock:
            return f"[DEMO MODE] This is a simulated answer for: '{prompt}'. \n\nIn a real deployment, BioGPT would analyze the clinical context. For now, here is a placeholder medical fact: The patient appears to be exhibiting symptoms consistent with viral infection. usage of antibiotics is not recommended unless bacterial co-infection is present."

        if not self.model:
            self.load_model()
        
        # Optimization: Use Greedy Search (num_beams=1) for speed on CPU
        # If GPU is available, we could possibly increase this, but 1 is safest for speed.
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            output = self.model.generate(
                **inputs, 
                min_length=10, 
                max_length=max_length, 
                num_beams=1,  # Reduced from 5 to 1 for speed
                do_sample=True, # Add sampling for variety since we removed beams
                temperature=0.7,
                top_k=50,
                early_stopping=True
            )
        return self.tokenizer.decode(output[0], skip_special_tokens=True)
