# 📈 Stock Tracker

A web-based stock analysis dashboard built with **Python and Streamlit**. The application retrieves market and financial data using **Yahoo Finance through `yfinance`** and presents it through an interactive, black-and-blue themed interface.

## 🚀 Features

### 📊 Stock Search

* Search for stocks using their ticker symbols.
* Supports multiple international exchanges.
* Displays:

  * Company Name
  * Market Status
  * Sector
  * Industry
  * Current Price
  * Today's Change
  * Change %
  * Current Performance
  * Market Capitalization

### 🌍 Supported Exchanges

| Exchange        | Code      | Example       |
| --------------- | --------- | ------------- |
| NSE (India)     | `.NS`     | `RELIANCE.NS` |
| BSE (India)     | `.BO`     | `RELIANCE.BO` |
| NASDAQ (USA)    | No suffix | `AAPL`        |
| NYSE (USA)      | No suffix | `KO`          |
| LSE (UK)        | `.L`      | `SHEL.L`      |
| TSX (Canada)    | `.TO`     | `SHOP.TO`     |
| ASX (Australia) | `.AX`     | `BHP.AX`      |
| Tokyo (Japan)   | `.T`      | `7203.T`      |

### 📈 Performance Summary

The application calculates stock performance over:

* 1 Week
* 1 Month
* 3 Months
* 6 Months
* 1 Year
* 5 Years

### 📉 Interactive Charts

Interactive stock charts include:

* Closing price
* Starting-price reference line
* Daily change
* Daily change %
* Period change %
* Interactive hover information
* Zoom and pan functionality
* Multiple historical periods

### 🔄 Stock Comparison

Compare two stocks over:

* 1 Week
* 1 Month
* 3 Months
* 6 Months
* 1 Year
* 5 Years

The comparison is normalized to percentage change from each stock's starting price, making the relative performance easier to compare.

### 💰 Valuation Analysis

Displays available valuation metrics:

* P/E Ratio
* Forward P/E
* PEG Ratio
* Price-to-Book
* Price-to-Sales
* EV / EBITDA

### 📑 Financial Statement Analysis

Includes:

**Profit & Loss Statement**

* Revenue
* Gross Profit
* Operating Income
* EBITDA
* Net Income
* Gross Margin
* Operating Margin
* Net Profit Margin

**Balance Sheet**

* Total Assets
* Total Liabilities
* Total Debt
* Total Cash
* Current Assets
* Current Liabilities
* Current Ratio
* Debt-to-Equity
* Working Capital

**Cash Flow Statement**

* Operating Cash Flow
* Free Cash Flow
* Capital Expenditure
* Investing Cash Flow
* Financing Cash Flow

### 💵 Dividend Analysis

Displays:

* Dividend Rate
* Dividend Yield
* Payout Ratio
* Ex-Dividend Date
* Recent Dividend History

### 👥 Shareholder & Ownership Analysis

Displays:

* Institutional Ownership
* Insider Ownership

### ⚠️ Risk & Market Analysis

Displays:

* Beta
* Day's High
* Day's Low
* 52-Week High
* 52-Week Low
* 50-Day Moving Average
* 200-Day Moving Average

## 🎨 Interface

The application uses a **black and blue dashboard design** with:

* Dark background
* Navy-blue cards
* Blue highlights
* Interactive charts
* Responsive Streamlit layout
* Sidebar navigation
* Metric cards for important values

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **yfinance**
* **Plotly**
* **Pandas**

## 📁 Project Structure

```text
Stock-Tracker/
│
├── app.py
├── requirements.txt
└── README.md
```

## 💻 Running Locally

Clone the repository:

```bash
git clone https://github.com/your-username/Stock-Tracker.git
cd Stock-Tracker
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

The application will open in your web browser.

## ☁️ Deployment

The application can be deployed using **Streamlit Community Cloud** directly from the GitHub repository.

Select:

```text
Repository → app.py → Deploy
```

No database or separate backend server is required.

## 📌 Data Source

Market and financial information is retrieved through **Yahoo Finance using the `yfinance` Python library**.

Data availability may vary depending on the stock, exchange, market, and information provided by Yahoo Finance.

## ⚠️ Disclaimer

This application is intended for **educational and informational purposes only**.

The information displayed by the application should not be considered financial, investment, or trading advice. Always verify financial information using reliable sources before making investment decisions.

## 👨‍💻 Project

**Stock Tracker**

A Python-based interactive stock analysis dashboard designed to provide market information, historical performance, financial analysis, valuation metrics, dividend information, ownership data, risk metrics, and stock comparison in a single interface.
