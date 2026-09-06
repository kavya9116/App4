import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Stock Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

CURRENCY_SYMBOLS = {
    "INR": "₹",
    "USD": "$",
    "GBP": "£",
    "EUR": "€",
    "JPY": "¥",
    "CNY": "¥",
    "AUD": "A$",
    "CAD": "C$"
}

PERIODS = {
    "1 Week": "1wk",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y"
}

EXCHANGES = {
    "NSE (India)": ".NS",
    "BSE (India)": ".BO",
    "NASDAQ (USA)": "No suffix",
    "NYSE (USA)": "No suffix",
    "LSE (UK)": ".L",
    "TSX (Canada)": ".TO",
    "ASX (Australia)": ".AX",
    "Tokyo (Japan)": ".T"
}

st.markdown("""
<style>
.stApp {
    background: #05080f;
    color: #eaf2ff;
}

[data-testid="stHeader"] {
    background: rgba(5,8,15,0.95);
}

[data-testid="stSidebar"] {
    background: #080d18;
    border-right: 1px solid #12345a;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg,#071326,#0a2140);
    border: 1px solid #1257a6;
    border-radius: 20px;
    padding: 30px 34px;
    margin-bottom: 24px;
    box-shadow: 0 10px 35px rgba(0,100,255,.12);
}

.hero h1 {
    margin: 0;
    color: #ffffff;
    font-size: 42px;
}

.hero p {
    color: #9fc7f7;
    font-size: 16px;
    margin-top: 8px;
}

.section {
    color: #55aaff;
    font-size: 22px;
    font-weight: 700;
    border-left: 4px solid #1683ff;
    padding-left: 12px;
    margin: 28px 0 16px;
}

.card {
    background: linear-gradient(145deg,#0a111e,#0b1626);
    border: 1px solid #173d67;
    border-radius: 16px;
    padding: 20px;
    min-height: 110px;
}

.card-title {
    color: #8cb9e8;
    font-size: 13px;
    margin-bottom: 7px;
}

.card-value {
    color: #ffffff;
    font-size: 23px;
    font-weight: 700;
}

.exchange-box {
    background: #08111f;
    border: 1px solid #164c82;
    border-radius: 14px;
    padding: 18px 22px;
    margin: 12px 0 22px;
}

.exchange-box table {
    border-collapse: collapse;
}

.exchange-box th,
.exchange-box td {
    padding: 5px 10px 5px 0;
    border-bottom: 1px solid #153654;
}

.small-note {
    color: #7897b7;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #1768b7;
    background: #0b2543;
    color: white;
    font-weight: 600;
}

div.stButton > button:hover {
    border-color: #3da0ff;
    background: #10385f;
}

[data-testid="stMetric"] {
    background: #0a111e;
    border: 1px solid #173d67;
    border-radius: 14px;
    padding: 15px;
}

hr {
    border-color: #153654;
}
</style>
""", unsafe_allow_html=True)


def section(title):
    st.markdown(
        f'<div class="section">{title}</div>',
        unsafe_allow_html=True
    )


def card(title, value):
    st.markdown(
        f'<div class="card">'
        f'<div class="card-title">{title}</div>'
        f'<div class="card-value">{value}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


def exchange_instructions():
    st.markdown("**Enter the stock symbol along with the exchange code.**")

    st.table({
        "Exchange": [
            "NSE (India)",
            "BSE (India)",
            "NASDAQ (USA)",
            "NYSE (USA)",
            "LSE (UK)",
            "TSX (Canada)",
            "ASX (Australia)",
            "Tokyo (Japan)"
        ],
        "Code": [
            ".NS",
            ".BO",
            "No suffix",
            "No suffix",
            ".L",
            ".TO",
            ".AX",
            ".T"
        ]
    })

    st.markdown(
        "**Examples:**  \n"
        "`Reliance – NSE:` `RELIANCE.NS`  \n"
        "`Reliance – BSE:` `RELIANCE.BO`  \n"
        "`Apple – NASDAQ:` `AAPL`  \n"
        "`Microsoft – NASDAQ:` `MSFT`  \n"
        "`Coca-Cola – NYSE:` `KO`  \n"
        "`Toyota – Tokyo:` `7203.T`"
    )

@st.cache_data(ttl=300, show_spinner=False)
def get_stock_info(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        data = stock.history(
            period="5d",
            raise_errors=False
        )

        if data.empty:
            return None

        if "Close" not in data.columns:
            return None

        if data["Close"].dropna().empty:
            return None

        if not info.get("longName"):
            return None

        return info

    except Exception:
        return None


def get_stock(symbol):
    try:
        return yf.Ticker(symbol)
    except Exception:
        return None


@st.cache_data(ttl=300, show_spinner=False)
def get_history(symbol, period):
    try:
        return yf.Ticker(symbol).history(
            period=period,
            raise_errors=False
        )
    except Exception:
        return None


def currency_for(info):
    code = info.get("currency", "N/A")
    return CURRENCY_SYMBOLS.get(code, code + " ")


def money(value, currency):
    if value is None:
        return "N/A"

    return f"{currency}{value:,.2f}"


def make_chart(
    data,
    title,
    currency,
    symbol,
    height=500,
    show_ma20=False,
    show_ma50=False
):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name=symbol
        )
    )

    if show_ma20:
        ma20 = data["Close"].rolling(20).mean()
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=ma20,
                mode="lines",
                name="20D MA"
            )
        )

    if show_ma50:
        ma50 = data["Close"].rolling(50).mean()
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=ma50,
                mode="lines",
                name="50D MA"
            )
        )

    fig.update_layout(
        title=f"{symbol} — {title}",
        height=height,
        xaxis_title="Date",
        yaxis_title=f"Price ({currency})",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def make_comparison_chart(
    data1,
    symbol1,
    data2,
    symbol2,
    period
):
    if (
        data1 is None
        or data2 is None
        or data1.empty
        or data2.empty
    ):
        return None

    data1 = data1["Close"].dropna()
    data2 = data2["Close"].dropna()

    if data1.empty or data2.empty:
        return None

    data1 = (
        data1 / data1.iloc[0] - 1
    ) * 100

    data2 = (
        data2 / data2.iloc[0] - 1
    ) * 100

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data1.index,
            y=data1,
            mode="lines",
            name=symbol1,
            line=dict(width=2.5),
            hovertemplate=(
                f"<b>{symbol1}</b><br>"
                "Date: %{x|%d-%b-%Y}<br>"
                "Change: %{y:+.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data2.index,
            y=data2,
            mode="lines",
            name=symbol2,
            line=dict(width=2.5),
            hovertemplate=(
                f"<b>{symbol2}</b><br>"
                "Date: %{x|%d-%b-%Y}<br>"
                "Change: %{y:+.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="#78909c",
        line_width=1
    )

    fig.update_layout(
        title=(
            f"{symbol1} vs {symbol2} - "
            f"Performance Comparison ({period})"
        ),
        height=520,
        template="plotly_dark",
        paper_bgcolor="#05080f",
        plot_bgcolor="#08111f",
        font=dict(color="#dbeeff"),
        hovermode="x unified",
        margin=dict(
            l=45,
            r=25,
            t=65,
            b=45
        ),
        xaxis=dict(
            title="Date",
            gridcolor="#132a42"
        ),
        yaxis=dict(
            title="Change from Starting Price (%)",
            gridcolor="#132a42"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    return fig


def show_stock_header(info, symbol):
    currency = currency_for(info)

    check = get_history(symbol, "5d")

    price = info.get("currentPrice")

    if (
        price is None
        and check is not None
        and not check.empty
    ):
        price = check["Close"].iloc[-1]

    previous = info.get("previousClose")

    change = (
        price - previous
        if price is not None and previous is not None
        else None
    )

    change_pct = (
        change / previous * 100
        if change is not None and previous
        else None
    )

    state = info.get(
        "marketState",
        "N/A"
    )

    if state in ["REGULAR", "PRE"]:
        status = "OPEN"
    elif state == "POST":
        status = "CLOSED (After Market)"
    else:
        status = "CLOSED"

    if change is None:
        performance = "N/A"
    elif change > 0:
        performance = "GAINING"
    elif change < 0:
        performance = "FALLING"
    else:
        performance = "UNCHANGED"

    weekend = datetime.now().weekday() in [5, 6]

    change_label = (
        "Last Trading Day's Change"
        if weekend
        else "Today's Change"
    )

    change_pct_label = (
        "Last Trading Day's Change %"
        if weekend
        else "Change %"
    )

    section("Stock Overview")

    cols = st.columns(4)

    values = [
        (
            "Company Name",
            info.get(
                "longName",
                "N/A"
            )
        ),
        (
            "Market Status",
            status
        ),
        (
            "Sector",
            info.get(
                "sector",
                "N/A"
            )
        ),
        (
            "Industry",
            info.get(
                "industry",
                "N/A"
            )
        )
    ]

    for col, (title, value) in zip(
        cols,
        values
    ):
        with col:
            card(title, value)

    st.write("")

    cols = st.columns(4)

    values = [
        (
            "Current Price",
            money(price, currency)
        ),
        (
            change_label,
            money(change, currency)
        ),
        (
            change_pct_label,
            "N/A"
            if change_pct is None
            else f"{change_pct:+.2f}%"
        ),
        (
            "Current Performance",
            performance
        )
    ]

    for col, (title, value) in zip(
        cols,
        values
    ):
        with col:
            card(title, value)

    market_cap = info.get("marketCap")

    st.write("")

    cols = st.columns(3)

    with cols[0]:
        st.metric(
            "Market Cap",
            "N/A"
            if market_cap is None
            else f"{currency}{market_cap:,.0f}"
        )

    with cols[1]:
        st.metric(
            "Previous Close",
            money(previous, currency)
        )

    with cols[2]:
        st.metric(
            "Currency",
            info.get("currency", "N/A")
        )

    return currency


def performance_summary(symbol):
    section("Performance Summary")

    cols = st.columns(6)

    for col, (title, period) in zip(
        cols,
        PERIODS.items()
    ):
        data = get_history(
            symbol,
            period
        )

        if data is None or data.empty:
            result = "N/A"
        else:
            start = data["Close"].iloc[0]
            end = data["Close"].iloc[-1]

            result = (
                f"{(end - start) / start * 100:+.2f}%"
            )

        with col:
            st.metric(
                title,
                result
            )


def valuation(info):
    section("Valuation Analysis")

    rows = [
        ("P/E Ratio", "trailingPE"),
        ("Forward P/E", "forwardPE"),
        ("PEG Ratio", "pegRatio"),
        ("Price-to-Book", "priceToBook"),
        (
            "Price-to-Sales",
            "priceToSalesTrailing12Months"
        ),
        (
            "EV / EBITDA",
            "enterpriseToEbitda"
        )
    ]

    cols = st.columns(3)

    for i, (name, key) in enumerate(rows):
        value = info.get(key)

        display = (
            "N/A"
            if value is None
            else f"{value:.2f}"
        )

        with cols[i % 3]:
            st.metric(
                name,
                display
            )


def financials(stock, currency):
    section("Financial Statement Analysis")

    annual = stock.income_stmt
    quarterly = stock.quarterly_income_stmt
    balance = stock.balance_sheet
    cashflow = stock.cashflow

    def value(frame, key, column):
        if frame is not None and not frame.empty and key in frame.index:
            return frame.loc[key, column]
        return None

    def money_value(v):
        return "N/A" if v is None else f"{currency}{v:,.0f}"

    if not annual.empty:
        p = annual.columns[0]

        rows = [
            ("Revenue", value(annual, "Total Revenue", p)),
            ("Gross Profit", value(annual, "Gross Profit", p)),
            ("Operating Income", value(annual, "Operating Income", p)),
            ("EBITDA", value(annual, "EBITDA", p)),
            ("Net Income", value(annual, "Net Income", p))
        ]

        table = [
            {
                "Financial Item": name,
                "Value": money_value(v)
            }
            for name, v in rows
        ]

        st.markdown("### Profit & Loss Statement")
        st.caption(
            "Financial Year: "
            + (
                p.strftime("%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

    if not quarterly.empty:
        p = quarterly.columns[0]

        rows = [
            ("Revenue", value(quarterly, "Total Revenue", p)),
            ("Net Income", value(quarterly, "Net Income", p))
        ]

        table = [
            {
                "Financial Item": name,
                "Value": money_value(v)
            }
            for name, v in rows
        ]

        st.markdown("### Latest Quarter")
        st.caption(
            "Quarter Ended: "
            + (
                p.strftime("%d-%b-%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

    if not balance.empty:
        p = balance.columns[0]

        rows = [
            ("Total Assets", value(balance, "Total Assets", p)),
            (
                "Total Liabilities",
                value(
                    balance,
                    "Total Liabilities Net Minority Interest",
                    p
                )
            ),
            ("Total Debt", value(balance, "Total Debt", p)),
            (
                "Total Cash",
                value(
                    balance,
                    "Cash Cash Equivalents And Short Term Investments",
                    p
                )
            ),
            ("Current Assets", value(balance, "Current Assets", p)),
            (
                "Current Liabilities",
                value(balance, "Current Liabilities", p)
            ),
            (
                "Stockholders Equity",
                value(balance, "Stockholders Equity", p)
            )
        ]

        table = [
            {
                "Financial Item": name,
                "Value": money_value(v)
            }
            for name, v in rows
        ]

        st.markdown("### Balance Sheet")
        st.caption(
            "Financial Year: "
            + (
                p.strftime("%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

    if not cashflow.empty:
        p = cashflow.columns[0]

        rows = [
            (
                "Operating Cash Flow",
                value(cashflow, "Operating Cash Flow", p)
            ),
            (
                "Free Cash Flow",
                value(cashflow, "Free Cash Flow", p)
            ),
            (
                "Capital Expenditure",
                value(cashflow, "Capital Expenditure", p)
            ),
            (
                "Investing Cash Flow",
                value(cashflow, "Investing Cash Flow", p)
            ),
            (
                "Financing Cash Flow",
                value(cashflow, "Financing Cash Flow", p)
            )
        ]

        table = [
            {
                "Financial Item": name,
                "Value": money_value(v)
            }
            for name, v in rows
        ]

        st.markdown("### Cash Flow Statement")
        st.caption(
            "Financial Year: "
            + (
                p.strftime("%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

def dividends(info, stock, currency):
    section("Dividend Analysis")

    rate = info.get("dividendRate")
    yield_ = info.get("dividendYield")
    payout = info.get("payoutRatio")
    ex = info.get("exDividendDate")

    cols = st.columns(3)

    with cols[0]:
        st.metric(
            "Dividend Rate",
            "N/A"
            if rate is None
            else f"{currency}{rate:,.2f}"
        )

    with cols[1]:
        st.metric(
            "Dividend Yield",
            "N/A"
            if yield_ is None
            else f"{yield_ * 100:.2f}%"
        )

    with cols[2]:
        st.metric(
            "Payout Ratio",
            "N/A"
            if payout is None
            else f"{payout * 100:.2f}%"
        )

    if ex:
        try:
            ex = datetime.fromtimestamp(ex).strftime(
                "%d-%b-%Y"
            )
        except Exception:
            pass

    st.metric(
        "Ex-Dividend Date",
        ex or "N/A"
    )

    st.markdown("### Dividend History")

    data = stock.dividends

    if data.empty:
        st.info(
            "No dividend history available."
        )
    else:
        table = data.tail(10).reset_index()

        table.columns = [
            "Date",
            "Dividend"
        ]

        table["Date"] = table["Date"].dt.strftime(
            "%d-%b-%Y"
        )

        table["Dividend"] = table["Dividend"].map(
            lambda x: f"{currency}{x:,.2f}"
        )

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )


def shareholders(info, stock):
    section("Shareholder & Ownership Analysis")

    ownership = [
        (
            "Institutional Ownership",
            info.get("heldPercentInstitutions")
        ),
        (
            "Insider Ownership",
            info.get("heldPercentInsiders")
        ),
        (
            "Shares Outstanding",
            info.get("sharesOutstanding")
        ),
        (
            "Float Shares",
            info.get("floatShares")
        )
    ]

    table = []

    for name, value in ownership:
        if value is None:
            display = "N/A"
        elif "Ownership" in name:
            display = f"{value * 100:.2f}%"
        else:
            display = f"{value:,.0f}"

        table.append({
            "Ownership Item": name,
            "Value": display
        })

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    holders = None

    try:
        holders = stock.institutional_holders
    except Exception:
        pass

    if holders is not None and not holders.empty:
        st.markdown("### Major Institutional Holders")
        st.dataframe(
            holders,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Institutional holder data not available.")

def risk(info, currency):
    section("Risk & Market Analysis")

    rows = [
        ("Beta", info.get("beta"), "number"),
        ("Day's High", info.get("dayHigh"), "money"),
        ("Day's Low", info.get("dayLow"), "money"),
        ("52-Week High", info.get("fiftyTwoWeekHigh"), "money"),
        ("52-Week Low", info.get("fiftyTwoWeekLow"), "money"),
        (
            "50-Day Moving Average",
            info.get("fiftyDayAverage"),
            "money"
        ),
        (
            "200-Day Moving Average",
            info.get("twoHundredDayAverage"),
            "money"
        ),
        (
            "Average Volume",
            info.get("averageVolume"),
            "number"
        )
    ]

    table = []

    for name, value, kind in rows:
        if value is None:
            display = "N/A"
        elif kind == "money":
            display = f"{currency}{value:,.2f}"
        else:
            display = f"{value:,.2f}"

        table.append({
            "Market / Risk Item": name,
            "Value": display
        })

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

def analyst_analysis(stock):
    section("Analyst Analysis")

    sections = [
        ("Price Targets", "analyst_price_targets"),
        ("Recommendations", "recommendations"),
        ("Upgrades & Downgrades", "upgrades_downgrades"),
        ("Earnings Estimates", "earnings_estimate"),
        ("Revenue Estimates", "revenue_estimate"),
        ("EPS Trend", "eps_trend"),
        ("EPS Revisions", "eps_revisions"),
        ("Growth Estimates", "growth_estimates")
    ]

    displayed = False

    for title, attribute in sections:
        try:
            data = getattr(stock, attribute)
        except Exception:
            data = None

        if data is None:
            continue

        if hasattr(data, "empty") and data.empty:
            continue

        st.markdown(f"### {title}")

        if hasattr(data, "to_frame") and not hasattr(data, "columns"):
            data = data.to_frame()

        if hasattr(data, "reset_index"):
            data = data.reset_index()

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        displayed = True

    if not displayed:
        st.info("Analyst data is not available for this stock.")


def charts(symbol, currency):
    section("Charts / Graphs")

    choice = st.selectbox(
        "Select chart period",
        list(PERIODS.keys()),
        key="chart_period"
    )

    st.markdown("### Moving Average Overlays")

    ma20 = st.checkbox(
        "Show 20D Moving Average",
        key="show_ma20"
    )

    ma50 = st.checkbox(
        "Show 50D Moving Average",
        key="show_ma50"
    )

    if st.button(
        "Show Selected Chart",
        type="primary"
    ):
        data = get_history(
            symbol,
            PERIODS[choice]
        )

        if data is None or data.empty:
            st.warning(
                "No historical data available."
            )
        else:
            fig = make_chart(
                data,
                choice,
                currency,
                symbol,
                show_ma20=ma20,
                show_ma50=ma50
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.markdown("### All Graphs")

    if st.button(
        "Show All Graphs",
        key="all_graphs"
    ):
        items = list(PERIODS.items())

        for row_start in range(
            0,
            len(items),
            2
        ):
            cols = st.columns(2)

            for col, (title, period) in zip(
                cols,
                items[row_start:row_start + 2]
            ):
                with col:
                    data = get_history(
                        symbol,
                        period
                    )

                    if (
                        data is None
                        or data.empty
                    ):
                        st.warning(
                            f"{title}: "
                            "No data available."
                        )
                    else:
                        fig = make_chart(
                            data,
                            title,
                            currency,
                            symbol,
                            height=390,
                            show_ma20=ma20,
                            show_ma50=ma50
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

def compare_stocks(
    symbol1=None,
    symbol2=None
):
    section("Compare Two Stocks")

    exchange_instructions()

    first = st.text_input(
        "First stock symbol",
        value=symbol1 or "",
        key="compare_first"
    ).upper().strip()

    second = st.text_input(
        "Second stock symbol",
        value=symbol2 or "",
        key="compare_second"
    ).upper().strip()

    period = st.selectbox(
        "Comparison Period",
        list(PERIODS.keys()),
        key="comparison_period"
    )

    if st.button(
        "Compare Stocks",
        type="primary"
    ):
        if not first or not second:
            st.warning(
                "Enter both stock symbols."
            )
            return

        info1 = get_stock_info(first)
        info2 = get_stock_info(second)

        if info1 is None or info2 is None:
            st.error(
                "Invalid stock symbol. "
                "Please check both symbols "
                "and exchange codes."
            )
            return

        data1 = get_history(
            first,
            PERIODS[period]
        )

        data2 = get_history(
            second,
            PERIODS[period]
        )

        fig = make_comparison_chart(
            data1,
            first,
            data2,
            second,
            period
        )

        if fig is None:
            st.warning(
                "Comparison data unavailable."
            )
        else:
            st.plotly_chart(
                fig,
                use_container_width=True
            )


def stock_dashboard(
    symbol,
    info,
    analysis_category
):
    stock = get_stock(symbol)

    if stock is None:
        st.error(
            "Unable to load stock."
        )
        return

    currency = show_stock_header(
        info,
        symbol
    )

    performance_summary(symbol)

    section("Analysis")

    if analysis_category == "📑 Fundamental Analysis":
        fundamental_option = st.selectbox(
            "Select Fundamental Analysis",
            [
                "Valuation Analysis",
                "Financial Statement Analysis",
                "Dividend Analysis",
                "Shareholder & Ownership Analysis",
                "Risk & Market Analysis",
                "Analyst Analysis"
            ],
            key="fundamental_option"
        )

        if fundamental_option == "Valuation Analysis":
            valuation(info)

        elif fundamental_option == "Financial Statement Analysis":
            financials(
                stock,
                currency
            )

        elif fundamental_option == "Dividend Analysis":
            dividends(
                info,
                stock,
                currency
            )

        elif fundamental_option == "Shareholder & Ownership Analysis":
            shareholders(
                info,
                stock
            )

        elif fundamental_option == "Risk & Market Analysis":
            risk(
                info,
                currency
            )

        elif fundamental_option == "Analyst Analysis":
            analyst_analysis(stock)

    elif analysis_category == "📈 Technical Analysis":
        section("Technical Analysis")

        rows = [
            ("50-Day Moving Average", info.get("fiftyDayAverage")),
            ("200-Day Moving Average", info.get("twoHundredDayAverage")),
            ("52-Week High", info.get("fiftyTwoWeekHigh")),
            ("52-Week Low", info.get("fiftyTwoWeekLow")),
            ("Beta", info.get("beta")),
            ("Average Volume", info.get("averageVolume"))
        ]

        table = []

        for name, value in rows:
            if value is None:
                display = "N/A"
            elif "Average" in name and "Volume" not in name:
                display = f"{currency}{value:,.2f}"
            elif "High" in name or "Low" in name:
                display = f"{currency}{value:,.2f}"
            else:
                display = f"{value:,.2f}"

            table.append({
                "Market Indicator": name,
                "Value": display
            })

        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "These are values directly provided by yfinance. "
            "Calculated technical indicators will be added in the next phase."
        )

    elif analysis_category == "📊 Graph Analysis":
        charts(
            symbol,
            currency
        )

    elif analysis_category == "🔄 Comparison of Stocks":
        compare_stocks(
            symbol,
            None
        )


def main():
    st.markdown(
        """
        <div class="hero">
            <h1>📈 Stock Tracker</h1>
            <p>
                Market data, performance, valuation,
                financials, dividends, ownership,
                risk and analyst data.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("## 📊 Stock Tracker")
        st.caption("Black & Blue Edition")

        st.divider()

        if "selected_symbol" in st.session_state:
            st.markdown(
                f"**Selected Stock:** "
                f"`{st.session_state['selected_symbol']}`"
            )
        else:
            st.caption("No stock selected")

        st.divider()

        st.markdown(
            "### Supported Exchanges"
        )

        for name, code in EXCHANGES.items():
            st.write(
                f"**{name}:** {code}"
            )

    section("Select Stock")

    exchange_instructions()

    symbol = st.text_input(
        "Stock Symbol",
        value=st.session_state.get(
            "selected_symbol",
            ""
        ),
        placeholder="Example: AAPL or RELIANCE.NS"
    ).upper().strip()

    if st.button(
        "Search / Select Stock",
        type="primary"
    ):
        if not symbol:
            st.warning(
                "Please enter a stock symbol."
            )
            return

        info = get_stock_info(symbol)

        if info is None:
            st.error(
                "Invalid stock symbol. "
                "Please check the stock symbol "
                "and exchange code."
            )
            return

        st.session_state[
            "selected_symbol"
        ] = symbol

        st.session_state[
            "selected_info"
        ] = info

    if "selected_symbol" in st.session_state:
        st.divider()

        analysis_category = st.radio(
            "Analysis",
            [
                "📑 Fundamental Analysis",
                "📈 Technical Analysis",
                "📊 Graph Analysis",
                "🔄 Comparison of Stocks"
            ],
            horizontal=True,
            key="analysis_category"
        )

        st.divider()

        stock_dashboard(
            st.session_state[
                "selected_symbol"
            ],
            st.session_state[
                "selected_info"
            ],
            analysis_category
        )


if __name__ == "__main__":
    main()
