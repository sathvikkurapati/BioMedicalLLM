try:
    print("Verifying imports...")
    import torch
    print(f"Torch version: {torch.__version__}")
    import transformers
    print(f"Transformers version: {transformers.__version__}")
    import streamlit
    print(f"Streamlit version: {streamlit.__version__}")
    
    print("Checking local modules...")
    from src.model_engine import BioGPTModel
    from src.security_guard import SecurityGuard
    from src.privacy_lab import PrivacyLab
    print("All modules imported successfully.")
    
except Exception as e:
    print(f"VERIFICATION FAILED: {e}")
    exit(1)
