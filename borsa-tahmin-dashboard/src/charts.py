import plotly.graph_objects as go

def create_candlestick_chart(df, symbol):
    fig = go.Figure()
    time_col = "Datetime" if "Datetime" in df.columns else "Date"
    
    fig.add_trace(go.Candlestick(
        x=df[time_col], open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"], name=symbol
    ))
    fig.update_layout(
        title=f"{symbol} Anlık Mum Grafiği (1 dk'lık)",
        xaxis_title="Zaman", yaxis_title="Fiyat",
        xaxis_rangeslider_visible=False, height=450,
        template="plotly_dark" 
    )
    return fig

def create_close_chart(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Kapanış"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"].rolling(7).mean(), mode="lines", name="MA 7"))
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"].rolling(30).mean(), mode="lines", name="MA 30"))
    
    fig.update_layout(
        title=f"{symbol} Son 90 Günlük Trend ve Ortalamalar",
        xaxis_title="Tarih", yaxis_title="Fiyat", height=450, template="plotly_dark"
    )
    return fig

def create_prediction_chart(y_test, predictions):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y_test.values, mode="lines", name="Gerçek Fiyat"))
    fig.add_trace(go.Scatter(y=predictions, mode="lines", name="Model Tahmini", line=dict(dash='dash')))
    
    fig.update_layout(
        title="Model Performansı: Gerçek vs Tahmin",
        xaxis_title="Son Test Günleri", yaxis_title="Fiyat", height=400, template="plotly_dark"
    )
    return fig