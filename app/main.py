from fastapi import FastAPI, HTTPException
from app.prediction import predict_stock

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Stock Prediction API for LQ45"}

@app.get("/predict/")
async def predict():
    predictions = []
    """
    Endpoint untuk melakukan prediksi pada semua model yang tersedia.
    """

    symbols = ["ACES.JK", "ADRO.JK", "AMMN.JK", "AMRT.JK", "ANTM.JK", "ARTO.JK", "ASII.JK", "BBCA.jk"]
    
    for symbol in symbols:
        try:
            result = predict_stock(symbol)
            if result is None:
                continue  # Jika tidak ada data, skip saham tersebut
            predictions.append(result)
        
        except Exception as e:
            print(f"Kesalahan pada simbol {symbol}: {e}")
    
    return {
        "error": False,
        "message": "success",
        "stocks": predictions
    }
