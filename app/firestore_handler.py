import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Ambil JSON dari environment variable
firebase_creds = os.getenv("FIREBASE_CREDENTIALS")

if firebase_creds:
    creds_dict = json.loads(firebase_creds)
    creds = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(creds)
else:
    raise ValueError("FIREBASE_CREDENTIALS tidak ditemukan!")

# Menghubungkan ke Firestore
db = firestore.client()



def fetch_last_35_close_prices(symbol: str):
    """
    Mengambil data harga penutupan terakhir beserta timestamp dan data perusahaan untuk simbol saham dari Firestore.
    """
    try:
        # Mengambil data harga saham dan informasi perusahaan dari Firestore
        stock_ref = db.collection("stocks").document(symbol)
        stock_data = stock_ref.get().to_dict()
        
        # Ambil nama perusahaan dan logo
        company_name = stock_data.get('company_name', '')
        company_logo = stock_data.get('company_logo', '')
        
        # Ambil data harga saham dari koleksi daily_data
        docs = stock_ref.collection("daily_data").stream()
        close_prices = []
        for doc in docs:
            data = doc.to_dict()
            if 'Close' in data:
                close_prices.append((doc.id, data['Close']))
        
        # Mengurutkan data berdasarkan waktu (timestamp)
        close_prices.sort(key=lambda x: x[0])
        
        # Ambil 35 data terakhir
        last_35_prices = close_prices[-35:]
        
        # Jika data tidak cukup
        if len(last_35_prices) < 35:
            print(f"Data untuk {symbol} tidak cukup.")
            return None
        
        # Mengambil timestamp dan harga penutupan (close prices)
        timestamps = [item[0] for item in last_35_prices]
        close_values = [item[1] for item in last_35_prices]
        
        return {
            "company_name": company_name,
            "company_logo": company_logo,
            "timestamps": timestamps,
            "close_prices": close_values
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None
