from fastapi import FastAPI, HTTPException, Query
from app.prediction import predict_stock

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Stock Prediction API for LQ45"}

@app.get("/predict/")
async def predict(page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    predictions = []

    symbols = [
        "ACES.JK","AMRT.JK","AMMN.JK","ANTM.JK",
        "ARTO.JK","ASII.JK","BBCA.JK","BBNI.JK","BBRI.JK",
        "BBTN.JK","BMRI.JK","BRIS.JK","BRPT.JK","BUKA.JK",
        "CPIN.JK","EXCL.JK","GGRM.JK","GOTO.JK","HRUM.JK",
        "ICBP.JK","INCO.JK","INDF.JK","INKP.JK","INTP.JK"
    ]

    # Hitung start & end index sesuai page dan limit
    start_index = (page - 1) * limit
    end_index = start_index + limit

    # Ambil slice symbol yang sesuai halaman
    paginated_symbols = symbols[start_index:end_index]

    # Jika halaman melebihi jumlah data, kembalikan kosong
    if not paginated_symbols:
        return {
            "error": False,
            "message": "no more data",
            "stocks": []
        }

    # Lakukan prediksi untuk simbol-simbol tersebut
    for symbol in paginated_symbols:
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
        "page": page,
        "limit": limit,
        "total_stocks": len(symbols),
        "stocks": predictions
    }
