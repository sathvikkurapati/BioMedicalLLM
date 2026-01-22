import torch
import math

class PrivacyLab:
    def __init__(self):
        pass

    def _compute_loss(self, model_obj, text):
        tokenizer = model_obj.tokenizer
        model = model_obj.model
        device = model_obj.device

        enc = tokenizer(text, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = model(**enc, labels=enc["input_ids"])
            loss = outputs.loss.item()

        return loss

    def simulate_mia(self, text, model_obj):
        """
        Loss-based Membership Inference Attack.
        Lower loss → higher chance of being in training data.
        """
        if model_obj.model is None:
            # Demo fallback (deterministic heuristic)
            length_factor = min(len(text) / 200, 1.0)
            structure_bonus = 0.3 if ("Patient" in text or "Diagnosis" in text) else 0.0
            score = 0.2 + length_factor * 0.4 + structure_bonus
            return min(score, 1.0)

        loss = self._compute_loss(model_obj, text)

        # Map loss to probability (empirical scaling)
        # BioGPT typical loss ~2–6
        score = 1 / (1 + math.exp(loss - 3.5))

        return float(max(0.0, min(score, 1.0)))

    def apply_mitigation(self, model_obj, prompt, noise=0.15):
        """
        Privacy defense: entropy injection during generation.
        This reduces confidence and raises loss.
        """
        return model_obj.generate_answer(
            prompt,
            temperature=1.1,
            top_k=30,
            top_p=0.85,
            noise=noise
        )
