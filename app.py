import streamlit as st
import requests
from bs4 import BeautifulSoup
import wikipedia
import yfinance as yf
import plotly.graph_objects as go

# -------------------------- Page Setup --------------------------
st.set_page_config(page_title="Finsight Pro - Stock Screener", layout="centered")
st.markdown("<h1 style='text-align: center;'>📊 Finsight Pro</h1>", unsafe_allow_html=True)
st.caption("Your personalized stock screener powered by Screener.in & Wikipedia")

# -------------------------- Descriptions --------------------------
ratio_descriptions = {
    "Market Cap": "Total value of a company’s outstanding shares; shows its size.",
    "Current Price": "Latest traded price of one share.",
    "High / Low": "The highest and lowest share prices in the past 52 weeks.",
    "Stock P/E": "Price-to-Earnings ratio; how much investors are willing to pay per ₹1 of earnings.",
    "Book Value": "Value of the company per share based on its balance sheet.",
    "Dividend Yield": "Annual dividend as a percentage of current price; shows income potential.",
    "ROCE": "Return on Capital Employed; how efficiently capital is used.",
    "ROE": "Return on Equity; profitability relative to shareholders' equity.",
    "Face Value": "The nominal or original value of the stock as assigned by the company."
}

# -------------------------- Screener API --------------------------
@st.cache_data(ttl=3600)
def get_company_suggestions(query):
    url = f"https://www.screener.in/api/company/search/?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def get_screener_data(relative_url):
    full_url = f"https://www.screener.in{relative_url}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(full_url, headers=headers)
    if response.status_code != 200:
        return None, f"❌ Failed to load company page. Status: {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')

    fields_needed = [
        "Market Cap", "Current Price", "High / Low", "Stock P/E", "Book Value",
        "Dividend Yield", "ROCE", "ROE", "Face Value"
    ]

    data = {}
    ratio_list = soup.select("ul#top-ratios > li")
    for li in ratio_list:
        label = li.select_one("span.name")
        value = li.select_one("span.value")
        if label and value:
            key = label.text.strip()
            val = value.get_text(strip=True).replace("\xa0", " ")
            if key in fields_needed:
                data[key] = val

    for key in fields_needed:
        data.setdefault(key, "N/A")

    return data, None

def get_wikipedia_summary(company_name):
    try:
        return wikipedia.summary(company_name, sentences=3)
    except:
        return "📄 Description not found."
    
def plot_price_chart(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="6mo")
        fig = go.Figure(data=[go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close']
        )])
        fig.update_layout(title="6-Month Price Trend", xaxis_title="Date", yaxis_title="Price")
        st.plotly_chart(fig)
    except Exception as e:
        st.warning("Unable to fetch chart data.")

# -------------------------- UI Logic --------------------------
query = st.text_input("🔍 Search company name")

if query:
    matches = get_company_suggestions(query)
    if matches:
        options = [f"{match['name']} ({match['url'].split('/')[2]})" for match in matches]
        selected_option = st.selectbox("🏢 Select company", options)

        if selected_option:
            selected_index = options.index(selected_option)
            selected_url = matches[selected_index]['url']
            selected_name = matches[selected_index]['name']

            

            with st.spinner("📡 Fetching financial data..."):
                data, error = get_screener_data(selected_url)
                if error:
                    st.error(error)
                else:
                    st.markdown(f"### 📈 Financial Summary for **{selected_name}**")
                    col1, col2 = st.columns(2)

                    for i, (key, value) in enumerate(data.items()):
                        description = ratio_descriptions.get(key, "")
                        if i % 2 == 0:
                            with col1:
                                st.markdown(f"**{key}**")
                                st.success(value, icon="📌")
                                st.caption(description)
                        else:
                            with col2:
                                st.markdown(f"**{key}**")
                                st.success(value, icon="📌")
                                st.caption(description)
                    ticker_symbol = selected_url.split("/")[2] + ".NS"  # Assuming NSE
                    plot_price_chart(ticker_symbol)
                    st.divider()
                    st.markdown("### 📚 Company Description" \
                    "")
                    st.info(get_wikipedia_summary(selected_name))
    else:
        st.warning("🔍 No matching companies found. Try another name.")
