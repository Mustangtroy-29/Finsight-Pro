# 📊 Finsight Pro

**Finsight Pro** is a sleek and user-friendly Streamlit-based stock screener that scrapes key financial data from [Screener.in](https://www.screener.in/). It supports autocomplete search, detailed ratio insights, financial filters, and price trend visualizations using Plotly.

---

## 🚀 Features

- 🔍 **Autocomplete Company Search** using Screener's public API
- 📈 **Key Financial Metrics**: Market Cap, P/E, ROE, ROCE, Dividend Yield, etc.
- 📚 **Summary** of the company
- 🧠 **Ratio Explanations** with expandable tooltips for beginners
- 📊 **Price Trend Charts** using `yfinance` and `plotly`
- 🎛️ **Filters** for Market Cap, P/E Ratio, and more (Coming soon)
- 🧾 Clean and responsive UI with Streamlit

---

## 🛠️ Tech Stack

| Tool            | Purpose                     |
| --------------- | --------------------------- |
| `Streamlit`     | UI framework                |
| `requests`      | API and web scraping        |
| `BeautifulSoup` | HTML parsing from Screener  |
| `Wikipedia API` | Company description         |
| `yfinance`      | Historical stock price data |
| `Plotly`        | Candlestick charts          |
| `GNews`         | Provide news & updates      |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mustangtroy-29/Finsight-Pro.git
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate     # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

---

## 🌐 Live Demo

🔗 [Click here to try it live](https://your-streamlit-app-link)

---

## ⚠️ Disclaimer

This app is for educational and informational purposes only.  
Financial data is fetched from third-party sources and may not always be accurate or real-time.  
**Always verify data before making investment decisions.**
