from tensorflow.keras.models import load_model
from tensorflow.keras.initializers import Orthogonal



def load_model_for_symbol(symbol: str):
    """
    Memuat model berdasarkan simbol saham.
    """
    try:
        model_path = f"models/{symbol}_model.h5"
        model = load_model(model_path, custom_objects={"Orthogonal": Orthogonal})
        return model
    except Exception as e:
        print(f"Error loading model for {symbol}: {e}")
        return None
