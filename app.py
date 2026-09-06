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
    "USD": "$",import streamlit as st
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


def make_chart(data, title, currency, symbol, height=450):
    if data is None or data.empty:
        return None

    data = data.copy()
    data = data.dropna(subset=["Close"])

    if data.empty:
        return None

    data["Daily Change"] = data["Close"].diff()
    data["Daily Change %"] = data["Close"].pct_change() * 100

    start = data["Close"].iloc[0]

    data["Period Change %"] = (
        (data["Close"] - start) / start
    ) * 100

    final = data["Close"].iloc[-1]

    line_color = (
        "#00d084"
        if final >= start
        else "#ff4d6d"
    )

    customdata = []

    for i in range(len(data)):
        daily = data["Daily Change"].iloc[i]
        daily_pct = data["Daily Change %"].iloc[i]
        period_pct = data["Period Change %"].iloc[i]

        customdata.append([
            "N/A"
            if i == 0
            else f"{currency}{daily:+,.2f}",

            "N/A"
            if i == 0
            else f"{daily_pct:+.2f}%",

            f"{period_pct:+.2f}%"
        ])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name=symbol,
            line=dict(
                color=line_color,
                width=2.5
            ),
            customdata=customdata,
            hovertemplate=(
                "<b>" + symbol + "</b><br>"
                "Date: %{x|%d-%b-%Y}<br>"
                "Closing Price: " + currency +
                "%{y:,.2f}<br>"
                "Daily Change: %{customdata[0]}<br>"
                "Daily Change %: %{customdata[1]}<br>"
                "Period Change %: %{customdata[2]}"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=start,
        line_dash="dash",
        line_color="#78909c",
        line_width=1,
        annotation_text=(
            f"Starting Price: "
            f"{currency}{start:,.2f}"
        ),
        annotation_position="top left"
    )

    fig.update_layout(
        title=title,
        height=height,
        template="plotly_dark",
        paper_bgcolor="#05080f",
        plot_bgcolor="#08111f",
        font=dict(color="#dbeeff"),
        margin=dict(
            l=45,
            r=25,
            t=65,
            b=45
        ),
        hovermode="x",
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="#132a42"
        ),
        yaxis=dict(
            title=f"Price ({currency})",
            showgrid=True,
            gridcolor="#132a42"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbeeff")
        )
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

    if not annual.empty:
        p = annual.columns[0]

        def annual_value(key):
            if key in annual.index:
                return annual.loc[key, p]
            return None

        revenue = annual_value("Total Revenue")
        gross = annual_value("Gross Profit")
        operating = annual_value("Operating Income")
        ebitda = annual_value("EBITDA")
        net = annual_value("Net Income")

        st.markdown("### Profit & Loss Statement")

        st.caption(
            "Financial Year: "
            + (
                p.strftime("%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )

        cols = st.columns(5)

        values = [
            ("Revenue", revenue),
            ("Gross Profit", gross),
            ("Operating Income", operating),
            ("EBITDA", ebitda),
            ("Net Income", net)
        ]

        for col, (name, value) in zip(
            cols,
            values
        ):
            with col:
                st.metric(
                    name,
                    "N/A"
                    if value is None
                    else f"{currency}{value:,.0f}"
                )

        margins = [
            (
                "Gross Margin",
                gross / revenue * 100
                if revenue and gross is not None
                else None
            ),
            (
                "Operating Margin",
                operating / revenue * 100
                if revenue and operating is not None
                else None
            ),
            (
                "Net Profit Margin",
                net / revenue * 100
                if revenue and net is not None
                else None
            )
        ]

        cols = st.columns(3)

        for col, (name, value) in zip(
            cols,
            margins
        ):
            with col:
                st.metric(
                    name,
                    "N/A"
                    if value is None
                    else f"{value:+.2f}%"
                )

    if not quarterly.empty:
        p = quarterly.columns[0]

        revenue = (
            quarterly.loc["Total Revenue", p]
            if "Total Revenue" in quarterly.index
            else None
        )

        net = (
            quarterly.loc["Net Income", p]
            if "Net Income" in quarterly.index
            else None
        )

        st.markdown("### Latest Quarter")

        st.caption(
            "Quarter Ended: "
            + (
                p.strftime("%d-%b-%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )

        cols = st.columns(2)

        with cols[0]:
            st.metric(
                "Revenue",
                "N/A"
                if revenue is None
                else f"{currency}{revenue:,.0f}"
            )

        with cols[1]:
            st.metric(
                "Net Income",
                "N/A"
                if net is None
                else f"{currency}{net:,.0f}"
            )

    if not balance.empty:
        p = balance.columns[0]

        def balance_value(key):
            if key in balance.index:
                return balance.loc[key, p]
            return None

        assets = balance_value("Total Assets")

        liabilities = balance_value(
            "Total Liabilities Net Minority Interest"
        )

        debt = balance_value("Total Debt")

        cash = balance_value(
            "Cash Cash Equivalents And Short Term Investments"
        )

        current_assets = balance_value(
            "Current Assets"
        )

        current_liabilities = balance_value(
            "Current Liabilities"
        )

        equity = balance_value(
            "Stockholders Equity"
        )

        st.markdown("### Balance Sheet")

        st.caption(
            "Financial Year: "
            + (
                p.strftime("%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )

        rows = [
            ("Total Assets", assets),
            ("Total Liabilities", liabilities),
            ("Total Debt", debt),
            ("Total Cash", cash),
            ("Current Assets", current_assets),
            ("Current Liabilities", current_liabilities)
        ]

        cols = st.columns(3)

        for i, (name, value) in enumerate(rows):
            with cols[i % 3]:
                st.metric(
                    name,
                    "N/A"
                    if value is None
                    else f"{currency}{value:,.0f}"
                )

        current_ratio = (
            current_assets / current_liabilities
            if current_assets is not None
            and current_liabilities
            else None
        )

        debt_equity = (
            debt / equity
            if debt is not None and equity
            else None
        )

        working_capital = (
            current_assets - current_liabilities
            if current_assets is not None
            and current_liabilities is not None
            else None
        )

        cols = st.columns(3)

        with cols[0]:
            st.metric(
                "Current Ratio",
                "N/A"
                if current_ratio is None
                else f"{current_ratio:.2f}"
            )

        with cols[1]:
            st.metric(
                "Debt-to-Equity",
                "N/A"
                if debt_equity is None
                else f"{debt_equity:.2f}"
            )

        with cols[2]:
            st.metric(
                "Working Capital",
                "N/A"
                if working_capital is None
                else f"{currency}{working_capital:,.0f}"
            )

    if not cashflow.empty:
        p = cashflow.columns[0]

        def cashflow_value(key):
            if key in cashflow.index:
                return cashflow.loc[key, p]
            return None

        st.markdown("### Cash Flow Statement")

        st.caption(
            "Financial Year: "
            + (
                p.strftime("%Y")
                if hasattr(p, "strftime")
                else str(p)
            )
        )

        rows = [
            (
                "Operating Cash Flow",
                "Operating Cash Flow"
            ),
            (
                "Free Cash Flow",
                "Free Cash Flow"
            ),
            (
                "Capital Expenditure",
                "Capital Expenditure"
            ),
            (
                "Investing Cash Flow",
                "Investing Cash Flow"
            ),
            (
                "Financing Cash Flow",
                "Financing Cash Flow"
            )
        ]

        cols = st.columns(3)

        for i, (name, key) in enumerate(rows):
            value = cashflow_value(key)

            with cols[i % 3]:
                st.metric(
                    name,
                    "N/A"
                    if value is None
                    else f"{currency}{value:,.0f}"
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


def shareholders(info):
    section(
        "Shareholder & Ownership Analysis"
    )

    cols = st.columns(2)

    institutional = info.get(
        "heldPercentInstitutions"
    )

    insiders = info.get(
        "heldPercentInsiders"
    )

    with cols[0]:
        st.metric(
            "Institutional Ownership",
            "N/A"
            if institutional is None
            else f"{institutional * 100:.2f}%"
        )

    with cols[1]:
        st.metric(
            "Insider Ownership",
            "N/A"
            if insiders is None
            else f"{insiders * 100:.2f}%"
        )


def risk(info, currency):
    section(
        "Risk & Market Analysis"
    )

    beta = info.get("beta")

    st.metric(
        "Beta",
        "N/A"
        if beta is None
        else f"{beta:.2f}"
    )

    rows = [
        ("Day's High", "dayHigh"),
        ("Day's Low", "dayLow"),
        (
            "52-Week High",
            "fiftyTwoWeekHigh"
        ),
        (
            "52-Week Low",
            "fiftyTwoWeekLow"
        ),
        (
            "50-Day Moving Average",
            "fiftyDayAverage"
        ),
        (
            "200-Day Moving Average",
            "twoHundredDayAverage"
        )
    ]

    cols = st.columns(3)

    for i, (name, key) in enumerate(rows):
        value = info.get(key)

        with cols[i % 3]:
            st.metric(
                name,
                "N/A"
                if value is None
                else f"{currency}{value:,.2f}"
            )


def charts(symbol, currency):
    section("Charts / Graphs")

    choice = st.selectbox(
        "Select chart period",
        list(PERIODS.keys()),
        key="chart_period"
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
                symbol
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
                            height=390
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

    if analysis_category == "📊 Graph Analysis":
        st.info(
            "Graph Analysis structure is ready. "
            "Existing charts will be placed here."
        )

    elif analysis_category == "📈 Technical Analysis":
        st.info(
            "Technical Analysis structure is ready. "
            "Technical indicators will be added next."
        )

    elif analysis_category == "📑 Fundamental Analysis":
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
            shareholders(info)

        elif fundamental_option == "Risk & Market Analysis":
            risk(
                info,
                currency
            )

        elif fundamental_option == "Analyst Analysis":
            st.info(
                "Analyst Analysis structure is ready. "
                "Yfinance-provided analyst data will be added next."
            )

    elif analysis_category == "🔄 Stock Comparison":
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
                financials, dividends, ownership
                and risk analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("## 📊 Stock Tracker")
        st.caption("Black & Blue Edition")

        st.divider()

        st.markdown("### Stock Selection")

        if "selected_symbol" in st.session_state:
            st.success(
                f"Selected: {st.session_state['selected_symbol']}"
            )
        else:
            st.info("No stock selected.")

        st.divider()

        st.markdown("### Supported Exchanges")

        for name, code in EXCHANGES.items():
            st.write(
                f"**{name}:** {code}"
            )

    section("Main Menu")

    main_menu = st.selectbox(
        "Choose a section",
        [
            "🔍 Search / Select Stock",
            "📊 Analysis"
        ],
        key="main_menu"
    )

    if main_menu == "🔍 Search / Select Stock":
        section("Search for a Stock")

        exchange_instructions()

        symbol = st.text_input(
            "Stock Symbol",
            placeholder=(
                "Example: AAPL or RELIANCE.NS"
            )
        ).upper().strip()

        if st.button(
            "Search Stock",
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
            st.success(
                f"Currently selected: "
                f"{st.session_state['selected_symbol']}"
            )
            st.caption(
                "Go to Main Menu → Analysis to view "
                "different analyses without entering "
                "the stock symbol again."
            )

    else:
        if "selected_symbol" not in st.session_state:
            st.info(
                "Please select a stock first from "
                "Search / Select Stock."
            )
            return

        analysis_category = st.selectbox(
            "Select Analysis Category",
            [
                "📊 Graph Analysis",
                "📈 Technical Analysis",
                "📑 Fundamental Analysis",
                "🔄 Stock Comparison"
            ],
            key="analysis_category"
        )

        stock_dashboard(
            st.session_state["selected_symbol"],
            st.session_state["selected_info"],
            analysis_category
        )


if __name__ == "__main__":
    main()
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


def make_chart(data, title, currency, symbol, height=450):
    if data is None or data.empty:
        return None

    data = data.copy()
    data = data.dropna(subset=["Close"])

    if data.empty:
        return None

    data["Daily Change"] = data["Close"].diff()
    data["Daily Change %"] = data["Close"].pct_change() * 100

    start = data["Close"].iloc[0]

    data["Period Change %"] = (
        (data["Close"] - start) / start
    ) * 100

    final = data["Close"].iloc[-1]

    line_color = (
        "#00d084"
        if final >= start
        else "#ff4d6d"
    )

    customdata = []

    for i in range(len(data)):
        daily = data["Daily Change"].iloc[i]
        daily_pct = data["Daily Change %"].iloc[i]
        period_pct = data["Period Change %"].iloc[i]

        customdata.append([
            "N/A"
            if i == 0
            else f"{currency}{daily:+,.2f}",

            "N/A"
            if i == 0
            else f"{daily_pct:+.2f}%",

            f"{period_pct:+.2f}%"
        ])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name=symbol,
            line=dict(
                color=line_color,
                width=2.5
            ),
            customdata=customdata,
            hovertemplate=(
                "<b>" + symbol + "</b><br>"
                "Date: %{x|%d-%b-%Y}<br>"
                "Closing Price: " + currency +
                "%{y:,.2f}<br>"
                "Daily Change: %{customdata[0]}<br>"
                "Daily Change %: %{customdata[1]}<br>"
                "Period Change %: %{customdata[2]}"
                "<extra></extra>"
            )
        )
    )

    fig.add_hline(
        y=start,
        line_dash="dash",
        line_color="#78909c",
        line_width=1,
        annotation_text=(
            f"Starting Price: "
            f"{currency}{start:,.2f}"
        ),
        annotation_position="top left"
    )

    fig.update_layout(
        title=title,
        height=height,
        template="plotly_dark",
        paper_bgcolor="#05080f",
        plot_bgcolor="#08111f",
        font=dict(color="#dbeeff"),
        margin=dict(
            l=45,
            r=25,
            t=65,
            b=45
        ),
        hovermode="x",
        xaxis=dict(
            title="Date",
            showgrid=True,
            gridcolor="#132a42"
        ),
        yaxis=dict(
            title=f"Price ({currency})",
            showgrid=True,
            gridcolor="#132a42"
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbeeff")
        )
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

    def format_money(value):
        return "N/A" if value is None else f"{currency}{value:,.0f}"

    if not annual.empty:
        p = annual.columns[0]

        def annual_value(key):
            if key in annual.index:
                return annual.loc[key, p]
            return None

        revenue = annual_value("Total Revenue")
        gross = annual_value("Gross Profit")
        operating = annual_value("Operating Income")
        ebitda = annual_value("EBITDA")
        net = annual_value("Net Income")

        st.markdown("### Profit & Loss Statement")
        st.caption(
            "Financial Year: "
            + (p.strftime("%Y") if hasattr(p, "strftime") else str(p))
        )

        margin_gross = (
            gross / revenue * 100
            if revenue and gross is not None
            else None
        )
        margin_operating = (
            operating / revenue * 100
            if revenue and operating is not None
            else None
        )
        margin_net = (
            net / revenue * 100
            if revenue and net is not None
            else None
        )

        pnl_table = {
            "Financial Item": [
                "Revenue",
                "Gross Profit",
                "Operating Income",
                "EBITDA",
                "Net Income",
                "Gross Margin",
                "Operating Margin",
                "Net Profit Margin"
            ],
            "Value": [
                format_money(revenue),
                format_money(gross),
                format_money(operating),
                format_money(ebitda),
                format_money(net),
                "N/A" if margin_gross is None else f"{margin_gross:.2f}%",
                "N/A" if margin_operating is None else f"{margin_operating:.2f}%",
                "N/A" if margin_net is None else f"{margin_net:.2f}%"
            ]
        }

        st.dataframe(
            pnl_table,
            use_container_width=True,
            hide_index=True
        )

    if not quarterly.empty:
        p = quarterly.columns[0]

        revenue = (
            quarterly.loc["Total Revenue", p]
            if "Total Revenue" in quarterly.index
            else None
        )

        net = (
            quarterly.loc["Net Income", p]
            if "Net Income" in quarterly.index
            else None
        )

        st.markdown("### Latest Quarter")
        st.caption(
            "Quarter Ended: "
            + (p.strftime("%d-%b-%Y") if hasattr(p, "strftime") else str(p))
        )

        quarterly_table = {
            "Financial Item": ["Revenue", "Net Income"],
            "Value": [format_money(revenue), format_money(net)]
        }

        st.dataframe(
            quarterly_table,
            use_container_width=True,
            hide_index=True
        )

    if not balance.empty:
        p = balance.columns[0]

        def balance_value(key):
            if key in balance.index:
                return balance.loc[key, p]
            return None

        assets = balance_value("Total Assets")
        liabilities = balance_value(
            "Total Liabilities Net Minority Interest"
        )
        debt = balance_value("Total Debt")
        cash = balance_value(
            "Cash Cash Equivalents And Short Term Investments"
        )
        current_assets = balance_value("Current Assets")
        current_liabilities = balance_value("Current Liabilities")
        equity = balance_value("Stockholders Equity")

        current_ratio = (
            current_assets / current_liabilities
            if current_assets is not None and current_liabilities
            else None
        )

        debt_equity = (
            debt / equity
            if debt is not None and equity
            else None
        )

        working_capital = (
            current_assets - current_liabilities
            if current_assets is not None and current_liabilities is not None
            else None
        )

        st.markdown("### Balance Sheet")
        st.caption(
            "Financial Year: "
            + (p.strftime("%Y") if hasattr(p, "strftime") else str(p))
        )

        balance_table = {
            "Financial Item": [
                "Total Assets",
                "Total Liabilities",
                "Total Debt",
                "Total Cash",
                "Current Assets",
                "Current Liabilities",
                "Current Ratio",
                "Debt-to-Equity",
                "Working Capital"
            ],
            "Value": [
                format_money(assets),
                format_money(liabilities),
                format_money(debt),
                format_money(cash),
                format_money(current_assets),
                format_money(current_liabilities),
                "N/A" if current_ratio is None else f"{current_ratio:.2f}",
                "N/A" if debt_equity is None else f"{debt_equity:.2f}",
                format_money(working_capital)
            ]
        }

        st.dataframe(
            balance_table,
            use_container_width=True,
            hide_index=True
        )

    if not cashflow.empty:
        p = cashflow.columns[0]

        def cashflow_value(key):
            if key in cashflow.index:
                return cashflow.loc[key, p]
            return None

        st.markdown("### Cash Flow Statement")
        st.caption(
            "Financial Year: "
            + (p.strftime("%Y") if hasattr(p, "strftime") else str(p))
        )

        cashflow_table = {
            "Financial Item": [
                "Operating Cash Flow",
                "Free Cash Flow",
                "Capital Expenditure",
                "Investing Cash Flow",
                "Financing Cash Flow"
            ],
            "Value": [
                format_money(cashflow_value("Operating Cash Flow")),
                format_money(cashflow_value("Free Cash Flow")),
                format_money(cashflow_value("Capital Expenditure")),
                format_money(cashflow_value("Investing Cash Flow")),
                format_money(cashflow_value("Financing Cash Flow"))
            ]
        }

        st.dataframe(
            cashflow_table,
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


def shareholders(info):
    section(
        "Shareholder & Ownership Analysis"
    )

    cols = st.columns(2)

    institutional = info.get(
        "heldPercentInstitutions"
    )

    insiders = info.get(
        "heldPercentInsiders"
    )

    with cols[0]:
        st.metric(
            "Institutional Ownership",
            "N/A"
            if institutional is None
            else f"{institutional * 100:.2f}%"
        )

    with cols[1]:
        st.metric(
            "Insider Ownership",
            "N/A"
            if insiders is None
            else f"{insiders * 100:.2f}%"
        )


def risk(info, currency):
    section(
        "Risk & Market Analysis"
    )

    beta = info.get("beta")

    st.metric(
        "Beta",
        "N/A"
        if beta is None
        else f"{beta:.2f}"
    )

    rows = [
        ("Day's High", "dayHigh"),
        ("Day's Low", "dayLow"),
        (
            "52-Week High",
            "fiftyTwoWeekHigh"
        ),
        (
            "52-Week Low",
            "fiftyTwoWeekLow"
        ),
        (
            "50-Day Moving Average",
            "fiftyDayAverage"
        ),
        (
            "200-Day Moving Average",
            "twoHundredDayAverage"
        )
    ]

    cols = st.columns(3)

    for i, (name, key) in enumerate(rows):
        value = info.get(key)

        with cols[i % 3]:
            st.metric(
                name,
                "N/A"
                if value is None
                else f"{currency}{value:,.2f}"
            )


def charts(symbol, currency):
    section("Charts / Graphs")

    choice = st.selectbox(
        "Select chart period",
        list(PERIODS.keys()),
        key="chart_period"
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
                symbol
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
                            height=390
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
    info
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

    option = st.selectbox(
        "Select what you would like to view",
        [
            "Charts / Graphs",
            "Valuation Analysis",
            "Financial Statement Analysis",
            "Dividend Analysis",
            "Shareholder & Ownership Analysis",
            "Risk & Market Analysis",
            "Compare with Another Stock"
        ],
        key="analysis_option"
    )

    if option == "Charts / Graphs":
        charts(
            symbol,
            currency
        )

    elif option == "Valuation Analysis":
        valuation(info)

    elif option == "Financial Statement Analysis":
        financials(
            stock,
            currency
        )

    elif option == "Dividend Analysis":
        dividends(
            info,
            stock,
            currency
        )

    elif option == "Shareholder & Ownership Analysis":
        shareholders(info)

    elif option == "Risk & Market Analysis":
        risk(
            info,
            currency
        )

    elif option == "Compare with Another Stock":
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
                financials, dividends, ownership
                and risk analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown("## 📊 Stock Tracker")
        st.caption("Black & Blue Edition")

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "Search Stock",
                "Compare Stocks"
            ],
            label_visibility="collapsed"
        )

        st.divider()

        st.markdown(
            "### Supported Exchanges"
        )

        for name, code in EXCHANGES.items():
            st.write(
                f"**{name}:** {code}"
            )

    if page == "Search Stock":
        section("Search for a Stock")

        exchange_instructions()

        symbol = st.text_input(
            "Stock Symbol",
            placeholder=(
                "Example: AAPL or RELIANCE.NS"
            )
        ).upper().strip()

        if st.button(
            "Search Stock",
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
            stock_dashboard(
                st.session_state[
                    "selected_symbol"
                ],
                st.session_state[
                    "selected_info"
                ]
            )

    else:
        compare_stocks()


if __name__ == "__main__":
    main()
