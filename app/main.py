from fastapi import FastAPI, HTTPException
from app.prediction import predict_stock
from fastapi import FastAPI, HTTPException, Query

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

    symbols = ["ACES.JK", "ADRO.JK", "AMMN.JK", "AMRT.JK", "ANTM.JK", 
               "ARTO.JK", "ASII.JK", "BBCA.JK", "BBNI.JK", "BBRI.JK"
                ]
    
    for symbol in symbols:
        try:
            result = predict_stock(symbol)
            if result is None:
                continue  
            predictions.append(result)
        
        except Exception as e:
            print(f"Kesalahan pada simbol {symbol}: {e}")
    
    return {
        "error": False,
        "message": "success",
        "stocks": predictions
    }



@app.get("/predict-by-symbol")
async def predict_by_symbol(symbol: str = Query(..., description="Kode simbol saham, misalnya ACES.JK")):
    """
    Endpoint untuk melakukan prediksi berdasarkan simbol saham tertentu.
    """
    try:
        result = predict_stock(symbol)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Data untuk simbol {symbol} tidak ditemukan atau tidak cukup.")
        
        return {
            "error": False,
            "message": "success",
            "stocks": [result]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat memproses prediksi: {e}")
