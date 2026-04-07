from engine import AgroViveEngine
import os

try:
    print("Loading engine test...")
    engine = AgroViveEngine(models_path="models")
    print("Engine loaded successfully!")
    # Test with a dummy image or check classes
    print(f"Classes loaded: {len(engine.classes)}")
except Exception as e:
    print(f"Error: {e}")
