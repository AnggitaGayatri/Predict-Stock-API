from datetime import datetime, timedelta
from app.model_loader import load_model_for_symbol
from app.firestore_handler import fetch_last_35_close_prices
from app.preprocessing import preprocess_data

def predict_stock(symbol: str):
    """
    Prediksi harga saham berdasarkan simbol saham dan mengembalikan hasil lengkap dengan status perubahan harga.
    """
    data = fetch_last_35_close_prices(symbol)
    if not data:
        return None

    company_name = data["company_name"]
    company_logo = data["company_logo"]
    close_prices = data["close_prices"]
    timestamps = data["timestamps"]

  
    input_data, scaler = preprocess_data(close_prices)

    model = load_model_for_symbol(symbol)
    if model is None:
        return None


    predicted_scaled_price = model.predict(input_data)
    predicted_price = scaler.inverse_transform(predicted_scaled_price)

    def adjust_price_to_fraction(price): 
        if price < 200:
            fraction = 1
        elif price < 500:
            fraction = 2
        elif price < 2000:
            fraction = 5
        else:
            fraction = 10
        return round(price / fraction) * fraction

    predicted_price = [adjust_price_to_fraction(p[0]) for p in predicted_price]

    
    last_data_timestamp = timestamps[-1]
    if isinstance(last_data_timestamp, str):
        last_data_timestamp = datetime.strptime(last_data_timestamp, "%Y-%m-%d %H:%M:%S")

    predicted_timestamp = last_data_timestamp + timedelta(hours=2)


    if predicted_timestamp.hour >= 17:
        predicted_timestamp = predicted_timestamp.replace(hour=10) + timedelta(days=1)


    if predicted_timestamp.weekday() == 5:  
        predicted_timestamp = predicted_timestamp.replace(hour=10) + timedelta(days=2)
    elif predicted_timestamp.weekday() == 6: 
        predicted_timestamp = predicted_timestamp.replace(hour=10) + timedelta(days=1)

    timestamp_str = predicted_timestamp.strftime("%Y-%m-%d %H:%M:%S")


    last_close_price = close_prices[-1]
    price_change = float(predicted_price[0]) - last_close_price

    price_change_str = f"{'+' if price_change > 0 else ''}{round(price_change, 2)}"


    if price_change > 0:
        status = "naik"
    elif price_change < 0:
        status = "turun"
    else:
        status = "stagnan"

    return {
        "symbol": symbol,
        "company_name": company_name,
        "company_logo": company_logo,
        "predicted_price": float(predicted_price[0]),
        "timestamp": timestamp_str,
        "price_change": price_change_str,
        "status": status
    }
