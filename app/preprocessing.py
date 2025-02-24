import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(data: list[float]):
    """
    Melakukan preprocessing data saham untuk input model.
    """
    # Pastikan data yang diteruskan hanya harga penutupan
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(np.array(data).reshape(-1, 1))
    input_data = data_scaled.reshape(1, len(data), 1)  # Sesuaikan dengan input LSTM
    return input_data, scaler
