import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

def train_model(df):
    """Zaman serisi sırasını bozmadan Random Forest modelini eğitir."""
    features = [
        "Close", "Daily_Return", "MA_7", "MA_14", 
        "MA_30", "Volatility_7", "Volume_Change", "Price_Range"
    ]
    
    X = df[features]
    y = df["Target"]
    split_index = int(len(df) * 0.8)  
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    return model, mae, rmse, y_test, predictions