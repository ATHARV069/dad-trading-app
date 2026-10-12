import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Dad's Stock & IPO Assistant", page_icon="📈", layout="centered")

st.title("📈 Dad's Stock & IPO Assistant")

tab1, tab2 = st.tabs(["🔍 Stock Analysis", "🚀 IPO Tracker"])

with tab1:
    st.subheader("Select or Search Stock")
    
    stock_dict = {
        "Reliance Industries": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "State Bank of India (SBI)": "SBIN.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Infosys": "INFY.NS"
    }
    
    selected_name = st.selectbox("Choose a popular stock:", list(stock_dict.keys()))
    symbol_input = stock_dict[selected_name]
    
    # Cache data to prevent infinite loading / rate limits
    @st.cache_data(ttl=300)
    def load_data(symbol):
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="5d", interval="1d")
        return df

    if st.button("Check Market Signal"):
        with st.spinner("Fetching live market data..."):
            try:
                df = load_data(symbol_input)
                
                if not df.empty and len(df) >= 5:
                    df['EMA_9'] = df['Close'].ewm(span=3, adjust=False).mean()
                    df['EMA_21'] = df['Close'].ewm(span=5, adjust=False).mean()
                    
                    latest = df.iloc[-1]
                    price = latest['Close']
                    
                    st.metric(label=f"Current Price ({symbol_input})", value=f"₹{price:.2f}")
                    
                    if latest['EMA_9'] > latest['EMA_21']:
                        st.success("🟢 **Signal: BULLISH / BUY**")
                    else:
                        st.error("🔴 **Signal: BEARISH / EXIT**")
                        
                    st.line_chart(df['Close'])
                else:
                    st.warning("Market data temporarily unavailable. Please try again.")
            except Exception as e:
                st.error("Connection timeout with data provider. Please refresh.")

with tab2:
    st.subheader("Current & Upcoming Mainboard IPOs")
    st.info("💡 Always check Grey Market Premium (GMP) before applying.")
    
    ipo_data = [
        {"Company": "Reliance Jio Platforms", "Status": "Upcoming", "Issue Size": "~₹31,000 Cr", "Expected Date": "Oct 2026"},
        {"Company": "Avaada Electro", "Status": "Upcoming", "Issue Size": "~₹7,600 Cr", "Expected Date": "Oct 2026"},
        {"Company": "Carlsberg India", "Status": "Upcoming", "Issue Size": "~₹6,500 Cr", "Expected Date": "Oct 2026"}
    ]
    
    df_ipo = pd.DataFrame(ipo_data)
    st.dataframe(df_ipo, use_container_width=True)
