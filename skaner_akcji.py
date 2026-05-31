import streamlit as st
import yfinance as yf
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="Lukasz Investment Terminal", layout="wide")

st.title("📊")

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #1E293B 0%, #0F172A 35%, #020617 100%);
        color: #F8FAFC;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1600px;
    }

    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 900 !important;
        letter-spacing: -0.02em;
    }

    p, label, span {
        color: #E2E8F0 !important;
    }

    .terminal-card {
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 24px;
        padding: 30px;
        margin: 22px 0px;
        box-shadow: 0 18px 45px rgba(0,0,0,0.45);
    }

    .green-card {
        border-left: 8px solid #22C55E;
    }

    .yellow-card {
        border-left: 8px solid #EAB308;
    }

    .red-card {
        border-left: 8px solid #EF4444;
    }

    .big-score {
        font-size: 64px;
        font-weight: 900;
        color: #22C55E;
        line-height: 1;
    }

    .subtitle {
        color: #94A3B8 !important;
        font-size: 17px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.35);
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-radius: 14px 14px 0px 0px;
        padding: 12px 20px;
        color: #CBD5E1;
        font-weight: 800;
        border: 1px solid rgba(148, 163, 184, 0.15);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #16A34A, #22C55E) !important;
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #16A34A, #22C55E);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 12px 24px;
        font-weight: 900;
        box-shadow: 0 10px 25px rgba(34,197,94,0.25);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #15803D, #16A34A);
        color: white;
    }

    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
    }

    textarea, input {
        background-color: #111827 !important;
        color: #F8FAFC !important;
        border-radius: 16px !important;
        border: 1px solid #334155 !important;
    }

    [data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.25);
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="terminal-card green-card">
    <h2>🚀 Lukasz Investment Terminal</h2>
    <p class="subtitle">
    Macro Gate · Quality Growth · Fair Value · AI Advisor · Portfolio Allocation
    </p>
</div>
""", unsafe_allow_html=True)

def score_color(score):
    if score >= 75:
        return "green-card"
    elif score >= 55:
        return "yellow-card"
    else:
        return "red-card"


def stars(score):
    if score >= 85:
        return "⭐⭐⭐⭐⭐"
    elif score >= 70:
        return "⭐⭐⭐⭐☆"
    elif score >= 55:
        return "⭐⭐⭐☆☆"
    elif score >= 40:
        return "⭐⭐☆☆☆"
    else:
        return "⭐☆☆☆☆"
MY_PORTFOLIO = (
    "NVO,CRM,NVDA,MSFT,META,TSM,THEON,QCOM,IBKR,AVGO,ANET,ORCL,GOOGL,ASML,APH,"
    "SNDK,DELL,SOFI,CSCO,PANW,AVAV,DDOG,LRCX,AMAT,AMD,PLTR,MU,INTC,QBTS"
)

NASDAQ_100 = (
    "AAPL,MSFT,NVDA,AMZN,META,GOOGL,GOOG,AVGO,TSLA,COST,NFLX,AMD,PEP,ADBE,CSCO,"
    "TMUS,LIN,INTU,TXN,QCOM,AMGN,AMAT,ISRG,CMCSA,HON,VRTX,ADP,SBUX,GILD,MU,"
    "PANW,ADI,LRCX,MELI,KLAC,CDNS,SNPS,MDLZ,REGN,CRWD,ORLY,ABNB,CSX,MAR,MRVL,"
    "FTNT,ADSK,ROP,PAYX,PCAR,CHTR,NXPI,AEP,ROST,KDP,EXC,FAST,CTAS,AZN,TEAM,"
    "ODFL,CPRT,DDOG,EA,GEHC,BIIB,VRSK,XEL,CCEP,FANG,MNST,ZS,TTWO,DXCM,IDXX,"
    "BKR,ON,CDW,ANSS,WBD,ILMN,GFS,ARM"
)

PRICE_ALERTS = {
    "NVDA": 200,
    "AMZN": 240,
    "CRWD": 650,
    "SNOW": 220,
    "TTWO": 200,
    "MSFT": 420,
    "META": 580,
    "GOOGL": 340,
    "ANET": 140,
}

def get_data(ticker, period="2y"):
    return yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False
    )

def calc_rsi(close, window=14):
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze_stock(ticker):
    data = get_data(ticker)

    if data.empty or len(data) < 200:
        return None

    close = data["Close"].squeeze()
    volume = data["Volume"].squeeze()

    sma50 = close.rolling(50).mean()
    sma200 = close.rolling(200).mean()
    rsi = calc_rsi(close)

    price = float(close.iloc[-1])
    sma50_now = float(sma50.iloc[-1])
    sma200_now = float(sma200.iloc[-1])
    rsi_now = float(rsi.iloc[-1])
    ath = float(close.max())
    distance_ath = ((price / ath) - 1) * 100

    spy = get_data("SPY")
    spy_close = spy["Close"].squeeze()
    stock_return = (price / float(close.iloc[-126]) - 1) * 100
    spy_return = (float(spy_close.iloc[-1]) / float(spy_close.iloc[-126]) - 1) * 100
    relative_strength = stock_return - spy_return

    avg_volume = float(volume.rolling(20).mean().iloc[-1])
    last_volume = float(volume.iloc[-1])
    volume_score = 100 if last_volume > avg_volume else 40

    trend_score = 0
    if price > sma50_now:
        trend_score += 35
    if price > sma200_now:
        trend_score += 35
    if sma50_now > sma200_now:
        trend_score += 30

    if 35 <= rsi_now <= 55:
        rsi_score = 100
    elif 55 < rsi_now <= 70:
        rsi_score = 70
    elif rsi_now < 35:
        rsi_score = 75
    elif rsi_now > 75:
        rsi_score = 20
    else:
        rsi_score = 50

    if distance_ath <= -30:
        ath_score = 100
    elif distance_ath <= -20:
        ath_score = 80
    elif distance_ath <= -10:
        ath_score = 60
    elif distance_ath <= -5:
        ath_score = 45
    else:
        ath_score = 30

    rs_score = max(0, min(100, 50 + relative_strength * 3))

    composite = (
        trend_score * 0.30 +
        rsi_score * 0.20 +
        ath_score * 0.20 +
        volume_score * 0.10 +
        rs_score * 0.20
    )

    alert_price = PRICE_ALERTS.get(ticker)
    alert = ""
    if alert_price and price <= alert_price:
        alert = "🚨 ALERT CENOWY"

    if composite >= 75:
        decision = "🟢 DOKUP"
    elif composite >= 60:
        decision = "🟡 WARTO ROZWAŻYĆ"
    elif composite >= 45:
        decision = "🟠 OBSERWUJ"
    else:
        decision = "🔴 CZEKAJ"

    return {
        "Ticker": ticker,
        "Cena": round(price, 2),
        "Composite": round(composite, 1),
        "Trend": round(trend_score, 1),
        "RSI": round(rsi_now, 1),
        "RSI Score": round(rsi_score, 1),
        "ATH": round(ath, 2),
        "Od ATH %": round(distance_ath, 1),
        "RelStr 6M": round(relative_strength, 1),
        "Volume Score": round(volume_score, 1),
        "Alert": alert,
        "Decyzja": decision
    }

def scan_tickers(tickers_text):
    tickers = [x.strip().upper() for x in tickers_text.split(",") if x.strip()]
    results = []
    progress = st.progress(0)

    for i, ticker in enumerate(tickers):
        try:
            result = analyze_stock(ticker)
            if result:
                results.append(result)
            else:
                st.warning(f"{ticker}: za mało danych")
        except Exception as e:
            st.error(f"{ticker}: {e}")

        progress.progress((i + 1) / len(tickers))

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    return df.sort_values("Composite", ascending=False)
def macro_gate():

    score = 0

    spy = get_data("SPY")["Close"].squeeze()
    qqq = get_data("QQQ")["Close"].squeeze()
    vix = get_data("^VIX")["Close"].squeeze()

    spy_price = float(spy.iloc[-1])
    qqq_price = float(qqq.iloc[-1])
    vix_now = float(vix.iloc[-1])

    spy_sma200 = float(spy.rolling(200).mean().iloc[-1])
    qqq_sma200 = float(qqq.rolling(200).mean().iloc[-1])

    # TREND
    trend_score = 0

    if spy_price > spy_sma200:
        trend_score += 10

    if qqq_price > qqq_sma200:
        trend_score += 10

    score += trend_score

    # VIX
    if vix_now < 15:
        vix_score = 15
    elif vix_now < 18:
        vix_score = 12
    elif vix_now < 22:
        vix_score = 8
    elif vix_now < 28:
        vix_score = 4
    else:
        vix_score = 0

    score += vix_score

    # PRZEGRZANIE NASDAQ
    qqq_distance = ((qqq_price / qqq_sma200) - 1) * 100

    if qqq_distance <= 5:
        overheating_score = 15
        overheating_status = "Neutralnie"

    elif qqq_distance <= 10:
        overheating_score = 10
        overheating_status = "Lekko rozgrzany"

    elif qqq_distance <= 15:
        overheating_score = 5
        overheating_status = "Drogo"

    else:
        overheating_score = 0
        overheating_status = "Mocno przegrzany"

    score += overheating_score

    # BREADTH NASDAQ
    sample = [
        "AAPL","MSFT","NVDA","AMZN","META",
        "GOOGL","AVGO","AMD","NFLX","COST",
        "PANW","CRWD","ANET","ASML","TSM"
    ]

    above = 0

    for ticker in sample:

        try:
            d = get_data(ticker)

            if d.empty:
                continue

            c = d["Close"].squeeze()

            p = float(c.iloc[-1])
            sma = float(c.rolling(200).mean().iloc[-1])

            if p > sma:
                above += 1

        except:
            pass

    breadth = above / len(sample) * 100

    if breadth >= 70:
        breadth_score = 20

    elif breadth >= 55:
        breadth_score = 14

    elif breadth >= 40:
        breadth_score = 8

    else:
        breadth_score = 2

    score += breadth_score

    # FINAL SCORE

    if score >= 55:
        mode = "🟢 FULL DEPLOY"
        sizing = "Inwestuj normalnie"

    elif score >= 40:
        mode = "🟡 REDUCED"
        sizing = "Inwestuj 50-70% kapitału"

    elif score >= 25:
        mode = "🟠 CAUTIOUS"
        sizing = "Kupuj tylko najlepsze spółki"

    else:
        mode = "🔴 DEFENSIVE"
        sizing = "Więcej gotówki"

    return {
        "score": round(score,1),
        "mode": mode,
        "sizing": sizing,
        "SPY": round(spy_price,2),
        "SPY SMA200": round(spy_sma200,2),
        "QQQ": round(qqq_price,2),
        "QQQ SMA200": round(qqq_sma200,2),
        "QQQ od SMA200 %": round(qqq_distance,1),
        "VIX": round(vix_now,2),
        "Breadth %": round(breadth,1),
        "Overheating": overheating_status
    }
def safe_info_get(info, key, default=None):
    value = info.get(key, default)

    if value in [None, "", "None"]:
        return default

    return value


def score_quality_growth(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        price = safe_info_get(info, "currentPrice", None)
        market_cap = safe_info_get(info, "marketCap", None)

        revenue_growth = safe_info_get(info, "revenueGrowth", None)
        gross_margin = safe_info_get(info, "grossMargins", None)
        operating_margin = safe_info_get(info, "operatingMargins", None)
        profit_margin = safe_info_get(info, "profitMargins", None)
        roe = safe_info_get(info, "returnOnEquity", None)
        debt_equity = safe_info_get(info, "debtToEquity", None)
        forward_pe = safe_info_get(info, "forwardPE", None)
        trailing_pe = safe_info_get(info, "trailingPE", None)
        earnings_growth = safe_info_get(info, "earningsGrowth", None)
        free_cashflow = safe_info_get(info, "freeCashflow", None)
        total_revenue = safe_info_get(info, "totalRevenue", None)

        if price is None:
            hist = stock.history(period="5d")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])

        fcf_margin = None
        if free_cashflow and total_revenue and total_revenue != 0:
            fcf_margin = free_cashflow / total_revenue

        available_fields = [
            revenue_growth,
            gross_margin,
            operating_margin,
            profit_margin,
            roe,
            forward_pe
        ]

        data_points = sum(1 for x in available_fields if x is not None)

        if data_points < 3:
            return {
                "Ticker": ticker,
                "Cena": round(price, 2) if price else "Brak danych",
                "Market Cap": round(market_cap / 1_000_000_000, 1) if market_cap else "Brak danych",
                "Quality Score": None,
                "Revenue Growth %": "Brak danych",
                "Earnings Growth %": "Brak danych",
                "Gross Margin %": "Brak danych",
                "Operating Margin %": "Brak danych",
                "Profit Margin %": "Brak danych",
                "FCF Margin %": "Brak danych",
                "ROE %": "Brak danych",
                "Debt/Equity": "Brak danych",
                "Forward PE": "Brak danych",
                "PEG Approx": "Brak danych",
                "Fair Value": "Brak danych",
                "Upside/Downside %": "Brak danych",
                "Status danych": "⚠️ Brak danych yfinance",
                "Ocena": "Nie oceniaj"
            }

        score = 0

        # Revenue Growth - 25 pkt
        if revenue_growth is not None:
            if revenue_growth >= 0.30:
                score += 25
            elif revenue_growth >= 0.20:
                score += 20
            elif revenue_growth >= 0.10:
                score += 12
            elif revenue_growth > 0:
                score += 5

        # Gross Margin - 15 pkt
        if gross_margin is not None:
            if gross_margin >= 0.60:
                score += 15
            elif gross_margin >= 0.40:
                score += 10
            elif gross_margin >= 0.25:
                score += 5

        # Operating Margin - 15 pkt
        if operating_margin is not None:
            if operating_margin >= 0.25:
                score += 15
            elif operating_margin >= 0.15:
                score += 10
            elif operating_margin >= 0.05:
                score += 5

        # FCF Margin - 10 pkt
        if fcf_margin is not None:
            if fcf_margin >= 0.20:
                score += 10
            elif fcf_margin >= 0.10:
                score += 7
            elif fcf_margin > 0:
                score += 3

        # ROE - 10 pkt
        if roe is not None:
            if roe >= 0.25:
                score += 10
            elif roe >= 0.15:
                score += 7
            elif roe >= 0.08:
                score += 4

        # Debt - 10 pkt
        if debt_equity is not None:
            debt_equity_ratio = debt_equity / 100
            if debt_equity_ratio <= 0.5:
                score += 10
            elif debt_equity_ratio <= 1:
                score += 6
            elif debt_equity_ratio <= 2:
                score += 2
        else:
            debt_equity_ratio = None

        # Valuation - 15 pkt
        peg_approx = None

        if forward_pe and revenue_growth and revenue_growth > 0:
            peg_approx = forward_pe / (revenue_growth * 100)

            if peg_approx <= 1.5:
                score += 15
            elif peg_approx <= 2.5:
                score += 10
            elif peg_approx <= 4:
                score += 5

        # Prosty Fair Value model
        fair_value = None
        upside = None

        if price and forward_pe and revenue_growth:

            growth_pct = revenue_growth * 100

            if growth_pct >= 30:
                fair_pe = 25
            elif growth_pct >= 20:
                fair_pe = 22
            elif growth_pct >= 10:
                fair_pe = 18
            else:
                fair_pe = 15

            fair_value = price * (fair_pe / forward_pe)
            upside = ((fair_value / price) - 1) * 100

        if score >= 80:
            rating = "🟢 Świetna jakość"
        elif score >= 65:
            rating = "🟡 Dobra jakość"
        elif score >= 50:
            rating = "🟠 Średnia jakość"
        else:
            rating = "🔴 Słaba / ryzykowna"

        return {
            "Ticker": ticker,
            "Cena": round(price, 2) if price else "Brak danych",
            "Market Cap": round(market_cap / 1_000_000_000, 1) if market_cap else "Brak danych",
            "Quality Score": round(score, 1),
            "Revenue Growth %": round(revenue_growth * 100, 1) if revenue_growth is not None else "Brak danych",
            "Earnings Growth %": round(earnings_growth * 100, 1) if earnings_growth is not None else "Brak danych",
            "Gross Margin %": round(gross_margin * 100, 1) if gross_margin is not None else "Brak danych",
            "Operating Margin %": round(operating_margin * 100, 1) if operating_margin is not None else "Brak danych",
            "Profit Margin %": round(profit_margin * 100, 1) if profit_margin is not None else "Brak danych",
            "FCF Margin %": round(fcf_margin * 100, 1) if fcf_margin is not None else "Brak danych",
            "ROE %": round(roe * 100, 1) if roe is not None else "Brak danych",
            "Debt/Equity": round(debt_equity_ratio, 2) if debt_equity_ratio is not None else "Brak danych",
            "Forward PE": round(forward_pe, 2) if forward_pe else "Brak danych",
            "PEG Approx": round(peg_approx, 2) if peg_approx else "Brak danych",
            "Fair Value": round(fair_value, 2) if fair_value else "Brak danych",
            "Upside/Downside %": round(upside, 1) if upside is not None else "Brak danych",
            "Status danych": "✅ OK",
            "Ocena": rating
        }

    except Exception as e:
        return {
            "Ticker": ticker,
            "Cena": "Błąd",
            "Market Cap": "Błąd",
            "Quality Score": None,
            "Revenue Growth %": "Błąd",
            "Earnings Growth %": "Błąd",
            "Gross Margin %": "Błąd",
            "Operating Margin %": "Błąd",
            "Profit Margin %": "Błąd",
            "FCF Margin %": "Błąd",
            "ROE %": "Błąd",
            "Debt/Equity": "Błąd",
            "Forward PE": "Błąd",
            "PEG Approx": "Błąd",
            "Fair Value": "Błąd",
            "Upside/Downside %": "Błąd",
            "Status danych": f"❌ {e}",
            "Ocena": "Nie oceniaj"
        }


def scan_quality_growth(tickers_text):
    tickers = [x.strip().upper() for x in tickers_text.split(",") if x.strip()]
    rows = []
    progress = st.progress(0)

    for i, ticker in enumerate(tickers):
        rows.append(score_quality_growth(ticker))
        progress.progress((i + 1) / len(tickers))

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    if "Quality Score" in df.columns:
        df["Quality Score Sort"] = pd.to_numeric(df["Quality Score"], errors="coerce")
        df = df.sort_values("Quality Score Sort", ascending=False)
        df = df.drop(columns=["Quality Score Sort"])

    return df

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Macro Gate",
    "💼 Mój portfel",
    "📈 Nasdaq 100",
    "💰 Co kupić za 700 CHF",
    "⭐ Quality Growth",
    "💰 Fair Value",
    "🤖 AI Advisor"
])

with tab1:
    st.header("📊 Macro Deployment Gate")

    if st.button("🚀 Sprawdź rynek PRO"):
        result = macro_gate()

        if result:
            score = result["score"]

            if score >= 55:
                gate_color = "🟢"
            elif score >= 40:
                gate_color = "🟡"
            elif score >= 25:
                gate_color = "🟠"
            else:
                gate_color = "🔴"

            st.markdown(f"""
            <div class="terminal-card green-card">
                <h2>{gate_color} {result["mode"]}</h2>
                <p class="subtitle">Aktualny tryb inwestowania</p>
                <div style="font-size:54px;font-weight:900;color:#22C55E;">
                    {score}/70
                </div>
                <p style="font-size:20px;font-weight:800;">
                    {result["sizing"]}
                </p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("SPY", result["SPY"], f"SMA200: {result['SPY SMA200']}")
            with c2:
                st.metric("QQQ", result["QQQ"], f"SMA200: {result['QQQ SMA200']}")
            with c3:
                st.metric("VIX", result["VIX"])
            with c4:
                st.metric("Breadth", f"{result['Breadth %']}%")

            st.markdown("### 📈 Wykresy rynku")

            sp500 = yf.download("^GSPC", period="2y", auto_adjust=True, progress=False)
            nasdaq = yf.download("^NDX", period="2y", auto_adjust=True, progress=False)

            col_a, col_b = st.columns(2)

            with col_a:
                fig_sp = px.line(
                    sp500,
                    y="Close",
                    title="S&P 500 — 2 lata"
                )
                fig_sp.add_scatter(
                    x=sp500.index,
                    y=sp500["Close"].rolling(200).mean(),
                    mode="lines",
                    name="SMA200"
                )
                fig_sp.update_layout(
                    template="plotly_dark",
                    height=430,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(15,23,42,0.85)",
                    font=dict(color="#E2E8F0"),
                    title_font=dict(size=22),
                )
                fig_sp.update_traces(line=dict(width=3))
                st.plotly_chart(fig_sp, use_container_width=True)

            with col_b:
                fig_ndx = px.line(
                    nasdaq,
                    y="Close",
                    title="Nasdaq 100 — 2 lata"
                )
                fig_ndx.add_scatter(
                    x=nasdaq.index,
                    y=nasdaq["Close"].rolling(200).mean(),
                    mode="lines",
                    name="SMA200"
                )
                fig_ndx.update_layout(
                    template="plotly_dark",
                    height=430,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(15,23,42,0.85)",
                    font=dict(color="#E2E8F0"),
                    title_font=dict(size=22),
                )
                fig_ndx.update_traces(line=dict(width=3))
                st.plotly_chart(fig_ndx, use_container_width=True)

            st.markdown("### 📋 Szczegóły Macro Gate")
            st.dataframe(pd.DataFrame([result]), use_container_width=True)

        else:
            st.error("Nie udało się pobrać danych makro.")

with tab2:
    st.header("💼 Mój portfel")

    portfolio_text = st.text_area("Tickery portfela", MY_PORTFOLIO, key="portfolio")

    if st.button("Skanuj mój portfel"):
        df = scan_tickers(portfolio_text)

        if not df.empty:
            st.subheader("🏆 Ranking portfela")
            st.dataframe(df, use_container_width=True)

            st.download_button(
                "📥 Pobierz CSV",
                df.to_csv(index=False).encode("utf-8"),
                "moj_portfel_ranking.csv",
                "text/csv"
            )

with tab3:
    st.header("📈 Nasdaq 100")

    nasdaq_text = st.text_area("Tickery Nasdaq 100", NASDAQ_100, key="nasdaq")

    min_score = st.slider("Minimalny Composite Score", 0, 100, 60)

    if st.button("Skanuj Nasdaq 100"):
        df = scan_tickers(nasdaq_text)

        if not df.empty:
            filtered = df[df["Composite"] >= min_score]

            st.metric("Spółek po filtrze", len(filtered))
            st.dataframe(filtered, use_container_width=True)

            st.download_button(
                "📥 Pobierz CSV",
                filtered.to_csv(index=False).encode("utf-8"),
                "nasdaq100_ranking.csv",
                "text/csv"
            )

with tab4:
    st.header("💰 Co kupić za 700 CHF")

    budget = st.number_input("Budżet CHF", value=700, step=50)

    if st.button("Wylicz alokację"):
        macro = macro_gate()
        df = scan_tickers(MY_PORTFOLIO)

        if macro and not df.empty:
            st.subheader(macro["mode"])
            st.write(macro["sizing"])

            if macro["score"] >= 70:
                deploy_budget = budget
            elif macro["score"] >= 40:
                deploy_budget = budget * 0.5
            else:
                deploy_budget = budget * 0.25

            df["Value Score"] = (
                df["Composite"] * 0.7
                + (100 - abs(df["Od ATH %"])) * 0.2
                + (100 - abs(df["RSI"] - 50)) * 0.1
            )

            candidates = (
                df.sort_values("Value Score", ascending=False)
                .head(3)
            )

            if candidates.empty:
                st.warning("Brak mocnych kandydatów. Lepiej poczekać.")
            else:
                weights = [0.5, 0.3, 0.2]
                rows = []

                for idx, (_, row) in enumerate(candidates.iterrows()):
                    amount = deploy_budget * weights[idx]

                    rows.append({
                        "Ticker": row["Ticker"],
                        "Kwota CHF": round(amount, 2),
                        "Composite": row["Composite"],
                        "Value Score": round(row["Value Score"], 1),
                        "Decyzja": row["Decyzja"],
                        "Cena": row["Cena"],
                        "Od ATH %": row["Od ATH %"],
                        "RSI": row["RSI"]
                    })

                alloc_df = pd.DataFrame(rows)

                st.success(
                    f"Sugerowana kwota do inwestycji: {round(deploy_budget, 2)} CHF"
                )

                st.dataframe(alloc_df, use_container_width=True)
with tab5:
    st.header("⭐ Quality Growth Score")

    qg_text = st.text_area("Tickery do analizy jakości", MY_PORTFOLIO, key="quality_growth")

    if st.button("Analizuj Quality Growth"):
        qg_df = scan_quality_growth(qg_text)

        if not qg_df.empty:
            st.subheader("🏆 Ranking jakości spółek")
            st.dataframe(qg_df, use_container_width=True)


with tab6:
    st.header("💰 Fair Value")

    fv_text = st.text_area("Tickery do wyceny", MY_PORTFOLIO, key="fair_value")

    if st.button("Sprawdź Fair Value"):
        fv_df = scan_quality_growth(fv_text)

        if not fv_df.empty:
            fair_df = fv_df[[
                "Ticker",
                "Cena",
                "Fair Value",
                "Upside/Downside %",
                "Quality Score",
                "Ocena"
            ]]

            st.dataframe(fair_df.sort_values("Upside/Downside %", ascending=False), use_container_width=True)


with tab7:
    st.header("🤖 AI Investment Advisor")

    if st.button("Przeanalizuj portfel AI"):
        qg_df = scan_quality_growth(MY_PORTFOLIO)
        tech_df = scan_tickers(MY_PORTFOLIO)
        macro = macro_gate()

        if not qg_df.empty and not tech_df.empty and macro:
            merged = pd.merge(
                qg_df,
                tech_df[["Ticker", "Composite", "RSI", "Od ATH %", "Decyzja"]],
                on="Ticker",
                how="left"
            )

            merged["Final Score"] = (
                merged["Quality Score"] * 0.60 +
                merged["Composite"] * 0.25 +
                merged["Upside/Downside %"].clip(-50, 50) * 0.15
            )

            merged = merged.sort_values("Final Score", ascending=False)

            st.subheader("📊 Ocena rynku")
            st.write(f"Macro Gate: **{macro['mode']}** — wynik {macro['score']}")
            st.write(macro["sizing"])

            st.subheader("🏆 Najlepsze spółki według AI Advisor")
            st.dataframe(merged, use_container_width=True)

            best = merged.iloc[0]
            best_quality = merged.sort_values("Quality Score", ascending=False).iloc[0]
            best_value = merged.sort_values("Upside/Downside %", ascending=False).iloc[0]
            most_expensive = merged.sort_values("Upside/Downside %", ascending=True).iloc[0]

            st.subheader("🤖 Wnioski AI Advisor")

            st.markdown(f"""
            **Najlepsza spółka ogólnie:** {best['Ticker']}  
            **Najlepsza jakość fundamentalna:** {best_quality['Ticker']}  
            **Największy potencjał względem Fair Value:** {best_value['Ticker']}  
            **Najdroższa / najmniej atrakcyjna wycena:** {most_expensive['Ticker']}  

            **Rekomendacja:**  
            Przy obecnym Macro Gate (**{macro['mode']}**) nie kupowałbym agresywnie całego portfela.
            Najpierw wybierałbym spółki z wysokim Quality Score, dodatnim potencjałem do Fair Value
            i sensownym Composite Score.
            """)
