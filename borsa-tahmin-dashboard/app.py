import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from src.data_loader import get_live_data, get_historical_data
from src.indicators import prepare_features
from src.model import train_model
from src.charts import create_candlestick_chart, create_close_chart, create_prediction_chart
st.set_page_config(
    page_title="Anlık Borsa & Tahmin Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Anlık Borsa Grafiği ve Kısa Vadeli Tahmin Sistemi")
st_autorefresh(interval=60000, key="stock_refresh")

def generate_signal(current_price, predicted_price):
    change_percent = ((predicted_price - current_price) / current_price) * 100
    if change_percent > 2:
        return change_percent, " Güçlü Yükseliş Beklentisi", "success"
    elif change_percent > 0:
        return change_percent, " Hafif Yükseliş Beklentisi", "info"
    elif change_percent > -2:
        return change_percent, " Kararsız / Yatay Bölge", "warning"
    else:
        return change_percent, " Düşüş Riski Yüksek", "error"
with st.sidebar:
    st.header(" Kontrol Paneli")
    symbol = st.selectbox(
        "Hisse / Varlık Seçin",
        ["AAPL", "TSLA", "MSFT", "NVDA", "AMZN", "THYAO.IS", "GARAN.IS", "ASELS.IS", "KCHOL.IS"]
    )
    st.write("---")
    st.caption(" Ekran her 60 saniyede bir otomatik olarak güncel verilerle yenilenir.")
live_df = get_live_data(symbol)
historical_df = get_historical_data(symbol)
if live_df.empty or historical_df.empty:
    st.error("Veri çekme hatası! Lütfen internet bağlantısını veya sembolü kontrol edin.")
else:
    current_price = float(live_df["Close"].iloc[-1])
    first_price = float(live_df["Open"].iloc[0])
    daily_change = ((current_price - first_price) / first_price) * 100
    last_volume = int(live_df["Volume"].iloc[-1])
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.metric("Anlık Fiyat", f"${current_price:.2f}" if not symbol.endswith(".IS") else f"{current_price:.2f} TL")
    m_col2.metric("Gün İçi Değişim", f"{daily_change:.2f}%", delta=f"{daily_change:.2f}%")
    m_col3.metric("Son Hacim", f"{last_volume:,}")
    st.write("---")
    tab1, tab2 = st.tabs([" Canlı Takip (1 Dk)", " Genel Trend (90 Gün)"])
    with tab1:
        st.plotly_chart(create_candlestick_chart(live_df, symbol), use_container_width=True)
    with tab2:
        st.plotly_chart(create_close_chart(historical_df, symbol), use_container_width=True)
        
    st.write("---")
    model_df = prepare_features(historical_df)
    if len(model_df) < 40:
        st.warning("Modeli eğitmek için geçmiş veri seti yetersiz.")
    else:
        model, mae, rmse, y_test, predictions = train_model(model_df)
        features_list = ["Close", "Daily_Return", "MA_7", "MA_14", "MA_30", "Volatility_7", "Volume_Change", "Price_Range"]
        last_live_row = model_df[features_list].iloc[[-1]]
        predicted_price = model.predict(last_live_row)[0]
        predicted_change, signal_text, alert_type = generate_signal(current_price, predicted_price)
        st.subheader(" Yapay Zeka Kısa Vadeli Tahmin Raporu")    
        p_col1, p_col2, p_col3 = st.columns(3)
        p_col1.metric("Yarınki Tahmini Kapanış", f"${predicted_price:.2f}" if not symbol.endswith(".IS") else f"{predicted_price:.2f} TL")
        p_col2.metric("Beklenen Yönsel Değişim", f"{predicted_change:.2f}%", delta=f"{predicted_change:.2f}%")
        p_col3.metric("Model Hata Payı (MAE)", f"{mae:.2f}")
        if alert_type == "success": st.success(signal_text)
        elif alert_type == "info": st.info(signal_text)
        elif alert_type == "warning": st.warning(signal_text)
        else: st.error(signal_text)
        st.plotly_chart(create_prediction_chart(y_test, predictions), use_container_width=True)

st.caption(" **Yasal Uyarı:** Bu proje sadece eğitim ve portfolyo amacıyla geliştirilmiştir. Kesinlikle yatırım tavsiyesi içermez.")