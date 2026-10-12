import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Dad's Stock & IPO Assistant", page_icon="📈", layout="centered")

st.title("📈 Dad's Stock & IPO Assistant")

tab1, tab2 = st.tabs(["🔍 Stock Analysis", "🚀 IPO Tracker"])

# --- TAB 1: STOCKS ---
with tab1:
    st.subheader("Select or Search Stock")
    
    stock_dict = {
        "Reliance Industries": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "State Bank of India": "SBIN.NS",
        "Tata Motors": "TATAMOTORS.NS"
    }
    
    selected_name = st.selectbox("Choose Stock:", list(stock_dict.keys()))
    symbol = stock_dict[selected_name]
    
    if st.button("Check Stock Signal"):
        with st.spinner("Loading data..."):
            try:
                stock = yf.Ticker(symbol)
                df = stock.history(period="1mo")
                
                if not df.empty:
                    df['EMA_9'] = df['Close'].ewm(span=9, adjust=False).mean()
                    df['EMA_21'] = df['Close'].ewm(span=21, adjust=False).mean()
                    
                    latest_price = df['Close'].iloc[-1]
                    latest_ema9 = df['EMA_9'].iloc[-1]
                    latest_ema21 = df['EMA_21'].iloc[-1]
                    
                    st.metric(label=f"Current Price ({selected_name})", value=f"₹{latest_price:.2f}")
                    
                    if latest_ema9 > latest_ema21:
                        st.success("🟢 **BUY SIGNAL** (Uptrend detected)")
                    else:
                        st.error("🔴 **BEARISH / SELL** (Downtrend detected)")
                        
                    st.line_chart(df['Close'])
                else:
                    st.warning("Data currently unavailable.")
            except Exception as e:
                st.error("Error fetching stock price. Please try again.")

# --- TAB 2: IPOs ---
with tab2:
    st.subheader("Current & Upcoming Mainboard IPOs")
    
    ipo_data = [
        {"Company": "Reliance Jio Platforms", "Status": "Upcoming", "Issue Size": "~₹31,000 Cr", "Expected": "Oct 2026"},
        {"Company": "Avaada Electro", "Status": "Upcoming", "Issue Size": "~₹7,600 Cr", "Expected": "Oct 2026"},
        {"Company": "Carlsberg India", "Status": "Upcoming", "Issue Size": "~₹6,500 Cr", "Expected": "Oct 2026"}
    ]
    
    st.dataframe(pd.DataFrame(ipo_data), use_container_width=True)
