import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Real-Time Stock Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")

# --- Sidebar ---
st.sidebar.header("User Settings")
ticker_symbol = st.sidebar.text_input("Enter Stock Symbol:", "TCS.NS")
period = st.sidebar.selectbox("Select Time Period:", ["1d", "5d", "1mo", "1y", "5y"])

# --- Data Fetching ---
with st.spinner('Fetching market data...'):
    # group_by='column' वापरल्यामुळे डेटा सोप्या फॉरमॅटमध्ये येतो
    raw_data = yf.download(ticker_symbol, period=period, interval="1m" if period == "1d" else "1d")

# डेटा उपलब्ध असेल तरच पुढची प्रोसेस करा
if not raw_data.empty:
    # महत्वाचे: Multi-index कॉलम्स फिक्स करण्यासाठी ही स्टेप
    data = raw_data.copy()
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Latest Market Data")
        st.dataframe(data.tail(10))
    
    with col2:
        st.subheader("Interactive Price Chart")
        # Candlestick chart साठी आता डेटा व्यवस्थित मॅप होईल
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Price"
        )])
        
        fig.update_layout(
            xaxis_rangeslider_visible=False, 
            height=450,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- Summary Metrics ---
    st.divider()
    st.subheader("Market Summary")
    m1, m2, m3 = st.columns(3)
    
    current_price = float(data['Close'].iloc[-1])
    first_price = float(data['Open'].iloc[0])
    price_change = current_price - first_price
    max_high = float(data['High'].max())
    
    m1.metric("Current Price", f"₹{current_price:,.2f}")
    m2.metric("Total Change", f"₹{price_change:,.2f}", delta=f"{price_change:,.2f}")
    m3.metric("Highest in Period", f"₹{max_high:,.2f}")

else:
    st.error("Error: Stock symbol not found or data unavailable.")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Kartik Gaikwad")