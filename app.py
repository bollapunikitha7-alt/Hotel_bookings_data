import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# HOTEL BUSINESS ANALYTICS - PROFESSIONAL STREAMLIT DASHBOARD
# =========================================================

st.set_page_config(
    page_title="Hotel Business Analytics",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 1. THEME
# =========================================================

st.sidebar.markdown("## 🏨 Hotel Analytics")

dark_mode = st.sidebar.toggle("Dark Mode", value=False)

if dark_mode:
    BG = "#0B1020"
    SURFACE = "#121A2A"
    SURFACE_2 = "#172235"
    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"
    BORDER = "#26354A"
    GRID = "#26354A"
    PRIMARY = "#7C83FF"
    CYAN = "#22D3EE"
    GREEN = "#34D399"
    RED = "#FB7185"
    ORANGE = "#FBBF24"
else:
    BG = "#F5F7FB"
    SURFACE = "#FFFFFF"
    SURFACE_2 = "#F8FAFC"
    TEXT = "#172033"
    MUTED = "#64748B"
    BORDER = "#E2E8F0"
    GRID = "#E8EDF4"
    PRIMARY = "#4F46E5"
    CYAN = "#0891B2"
    GREEN = "#059669"
    RED = "#E11D48"
    ORANGE = "#D97706"

# =========================================================
# 2. PROFESSIONAL CSS
# =========================================================

st.markdown(
    f"""
    <style>
        html, body, [class*="css"] {{
            font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}

        .stApp {{
            background: {BG};
            color: {TEXT};
        }}

        .block-container {{
            max-width: 1500px;
            padding-top: 2.8rem !important;
            padding-bottom: 1.5rem !important;
            padding-left: 1.6rem !important;
            padding-right: 1.6rem !important;
        }}

        /* ---------- HEADER ---------- */
        .hero {{
            background: linear-gradient(135deg, {PRIMARY}, #06B6D4);
            border-radius: 16px;
            padding: 22px 26px;
            margin: 0 0 16px 0;
            color: white;
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.16);
        }}

        .hero-title {{
            font-size: 27px;
            font-weight: 800;
            margin: 0;
            letter-spacing: -0.4px;
        }}

        .hero-subtitle {{
            font-size: 12px;
            opacity: 0.90;
            margin-top: 5px;
        }}

        .hero-badge {{
            display: inline-block;
            margin-top: 12px;
            padding: 5px 10px;
            border-radius: 20px;
            background: rgba(255,255,255,0.17);
            font-size: 10px;
            font-weight: 600;
        }}

        /* ---------- KPI CARDS ---------- */
        .kpi {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 13px;
            padding: 14px 16px;
            min-height: 102px;
            box-shadow: 0 4px 14px rgba(15,23,42,0.045);
        }}

        .kpi-label {{
            color: {MUTED};
            font-size: 11px;
            font-weight: 600;
        }}

        .kpi-value {{
            color: {TEXT};
            font-size: 24px;
            font-weight: 800;
            margin-top: 7px;
            letter-spacing: -0.5px;
        }}

        .kpi-note {{
            color: {MUTED};
            font-size: 9px;
            margin-top: 5px;
        }}

        /* ---------- SECTION ---------- */
        .section {{
            color: {TEXT};
            font-size: 15px;
            font-weight: 750;
            margin: 18px 0 7px 0;
        }}

        .section-note {{
            color: {MUTED};
            font-size: 10px;
            margin-bottom: 7px;
        }}

        /* ---------- CHART WRAPPER ---------- */
        .chart-head {{
            color: {TEXT};
            font-size: 12px;
            font-weight: 700;
            margin: 4px 0 2px 2px;
        }}

        /* ---------- INSIGHT CARDS ---------- */
        .insight {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 14px;
            min-height: 118px;
            box-shadow: 0 3px 12px rgba(15,23,42,0.04);
        }}

        .insight-title {{
            color: {TEXT};
            font-size: 12px;
            font-weight: 750;
            margin-bottom: 6px;
        }}

        .insight-body {{
            color: {MUTED};
            font-size: 10px;
            line-height: 1.55;
        }}

        /* ---------- SIDEBAR ---------- */
        section[data-testid="stSidebar"] {{
            background: {SURFACE};
            border-right: 1px solid {BORDER};
        }}

        section[data-testid="stSidebar"] label {{
            font-size: 11px !important;
            color: {TEXT} !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown p {{
            font-size: 11px;
        }}

        /* ---------- STREAMLIT METRIC - fallback ---------- */
        div[data-testid="stMetric"] {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 12px;
        }}

        /* ---------- HIDE DEFAULT CHROME ---------- */
        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        header {{
            background: transparent !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 3. LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    df = pd.read_csv("hotel_bookings_data.csv")

    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    if "arrival_date_month" in df.columns:
        df["arrival_date_month"] = pd.Categorical(
            df["arrival_date_month"],
            categories=months,
            ordered=True
        )

    required_date_cols = {
        "arrival_date_year",
        "arrival_date_month",
        "arrival_date_day_of_month"
    }

    if required_date_cols.issubset(df.columns):
        df["arrival_date"] = pd.to_datetime(
            df["arrival_date_year"].astype(str) + "-" +
            df["arrival_date_month"].astype(str) + "-" +
            df["arrival_date_day_of_month"].astype(str),
            format="%Y-%B-%d",
            errors="coerce"
        )
    else:
        df["arrival_date"] = pd.NaT

    return df, months


try:
    df, month_order = load_data()
except Exception:
    st.error(
        "❌ Dataset not found. Put `hotel_bookings_data.csv` inside "
        "`data/` and restart the app."
    )
    st.stop()

# =========================================================
# 4. SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Dashboard Filters")

hotel_options = ["All"] + sorted(
    df["hotel"].dropna().unique().tolist()
) if "hotel" in df.columns else ["All"]

market_options = ["All"] + sorted(
    df["market_segment"].dropna().unique().tolist()
) if "market_segment" in df.columns else ["All"]

deposit_options = ["All"] + sorted(
    df["deposit_type"].dropna().unique().tolist()
) if "deposit_type" in df.columns else ["All"]

selected_hotel = st.sidebar.selectbox("🏨 Hotel Type", hotel_options)
selected_market = st.sidebar.selectbox("📊 Market Segment", market_options)
selected_deposit = st.sidebar.selectbox("💳 Deposit Type", deposit_options)

valid_dates = df["arrival_date"].dropna()

if len(valid_dates) > 0:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_dates = st.sidebar.date_input(
        "📅 Arrival Date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    selected_dates = None

# =========================================================
# 5. APPLY FILTERS
# =========================================================

filtered = df.copy()

if selected_hotel != "All" and "hotel" in filtered.columns:
    filtered = filtered[filtered["hotel"] == selected_hotel]

if selected_market != "All" and "market_segment" in filtered.columns:
    filtered = filtered[filtered["market_segment"] == selected_market]

if selected_deposit != "All" and "deposit_type" in filtered.columns:
    filtered = filtered[filtered["deposit_type"] == selected_deposit]

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start = pd.Timestamp(selected_dates[0])
    end = pd.Timestamp(selected_dates[1]) + pd.Timedelta(days=1)

    filtered = filtered[
        (filtered["arrival_date"] >= start) &
        (filtered["arrival_date"] < end)
    ]

# =========================================================
# 6. CALCULATIONS
# =========================================================

total = len(filtered)

cancelled = (
    int(filtered["is_canceled"].sum())
    if total > 0 and "is_canceled" in filtered.columns
    else 0
)

cancel_rate = cancelled / total * 100 if total else 0

avg_adr = (
    filtered["adr"].mean()
    if total > 0 and "adr" in filtered.columns
    else 0
)

avg_lead = (
    filtered["lead_time"].mean()
    if total > 0 and "lead_time" in filtered.columns
    else 0
)

avg_stay = 0

if total > 0:
    stay_cols = [
        c for c in
        ["stays_in_weekend_nights", "stays_in_week_nights"]
        if c in filtered.columns
    ]

    if stay_cols:
        avg_stay = filtered[stay_cols].sum(axis=1).mean()

# =========================================================
# 7. HEADER
# =========================================================

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-title">🏨 Hotel Business Analytics</div>
        <div class="hero-subtitle">
            Interactive performance dashboard for bookings, cancellations,
            demand patterns and pricing behaviour.
        </div>
        <div class="hero-badge">
            ● {total:,} bookings currently selected
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 8. STATUS BAR
# =========================================================

st.markdown(
    f"""
    <div style="
        background:{'#063B2E' if dark_mode else '#ECFDF5'};
        border:1px solid {GREEN};
        border-radius:9px;
        padding:8px 12px;
        color:{TEXT};
        font-size:10px;
        margin-bottom:14px;
    ">
        ✓ Dataset loaded successfully &nbsp;•&nbsp;
        {total:,} bookings selected &nbsp;•&nbsp;
        {len(df.columns)} columns available
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# 9. KPI ROW
# =========================================================

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">👥 TOTAL BOOKINGS</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-note">Selected records</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">❌ CANCELLED</div>
            <div class="kpi-value">{cancelled:,}</div>
            <div class="kpi-note">Booking cancellations</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">📊 CANCELLATION RATE</div>
            <div class="kpi-value">{cancel_rate:.1f}%</div>
            <div class="kpi-note">Cancellation exposure</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">💰 AVERAGE ADR</div>
            <div class="kpi-value">${avg_adr:.2f}</div>
            <div class="kpi-note">Average daily rate</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k5:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">⏱ AVG LEAD TIME</div>
            <div class="kpi-value">{avg_lead:.0f}</div>
            <div class="kpi-note">Days before arrival</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 10. PLOT HELPERS
# =========================================================

def polish(fig, height=300):
    fig.update_layout(
        template="plotly_dark" if dark_mode else "plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Arial",
            size=10,
            color=TEXT
        ),
        margin=dict(l=38, r=20, t=38, b=38),
        hoverlabel=dict(
            font_size=11
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10)
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        tickfont=dict(size=9),
        title_font=dict(size=10)
    )

    return fig


def chart_title(icon, title, note=""):
    st.markdown(
        f"""
        <div class="chart-head">
            {icon} {title}
        </div>
        <div class="section-note">{note}</div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 11. OVERVIEW CHARTS
# =========================================================

st.markdown(
    '<div class="section">📈 Booking Overview</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

# Hotel type
with c1:
    chart_title(
        "🏨",
        "Bookings by Hotel Type",
        "Compare booking volume between hotel categories."
    )

    if "hotel" in filtered.columns:
        h = filtered["hotel"].value_counts().reset_index()
        h.columns = ["Hotel", "Bookings"]

        fig = px.bar(
            h,
            x="Hotel",
            y="Bookings",
            text_auto=",",
            color="Hotel",
            color_discrete_sequence=[PRIMARY, CYAN]
        )

        fig.update_traces(
            textposition="outside",
            textfont_size=9
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Bookings"
        )

        st.plotly_chart(
            polish(fig, 275),
            use_container_width=True
        )

# Market segment
with c2:
    chart_title(
        "📊",
        "Bookings by Market Segment",
        "Identify the channels generating the highest booking volume."
    )

    if "market_segment" in filtered.columns:
        m = filtered["market_segment"].value_counts().reset_index()
        m.columns = ["Segment", "Bookings"]

        fig = px.bar(
            m,
            x="Bookings",
            y="Segment",
            orientation="h",
            text_auto=",",
            color="Bookings",
            color_continuous_scale=[
                PRIMARY, CYAN, GREEN
            ]
        )

        fig.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Bookings",
            yaxis_title=None,
            yaxis=dict(autorange="reversed")
        )

        fig.update_traces(
            textposition="outside",
            textfont_size=8
        )

        st.plotly_chart(
            polish(fig, 275),
            use_container_width=True
        )

# =========================================================
# 12. CANCELLATION + MONTHLY TREND
# =========================================================

c3, c4 = st.columns(2)

with c3:
    chart_title(
        "❌",
        "Booking Status",
        "Confirmed versus cancelled bookings."
    )

    if "is_canceled" in filtered.columns:
        status = (
            filtered["is_canceled"]
            .map({0: "Confirmed", 1: "Cancelled"})
            .value_counts()
            .reset_index()
        )

        status.columns = ["Status", "Bookings"]

        fig = px.pie(
            status,
            names="Status",
            values="Bookings",
            hole=0.62,
            color="Status",
            color_discrete_map={
                "Confirmed": GREEN,
                "Cancelled": RED
            }
        )

        fig.update_traces(
            textinfo="percent",
            textfont_size=11
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                y=-0.05
            )
        )

        st.plotly_chart(
            polish(fig, 275),
            use_container_width=True
        )

with c4:
    chart_title(
        "📅",
        "Monthly Booking Trend",
        "Seasonal pattern of arrivals across the selected period."
    )

    if "arrival_date_month" in filtered.columns:
        trend = (
            filtered.groupby(
                "arrival_date_month",
                observed=True
            )
            .size()
            .reindex(month_order, fill_value=0)
            .reset_index()
        )

        trend.columns = ["Month", "Bookings"]

        fig = px.area(
            trend,
            x="Month",
            y="Bookings"
        )

        fig.update_traces(
            line=dict(color=PRIMARY, width=3),
            fillcolor="rgba(79,70,229,0.12)"
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Bookings"
        )

        st.plotly_chart(
            polish(fig, 275),
            use_container_width=True
        )

# =========================================================
# 13. PRICING + LEAD TIME
# =========================================================

st.markdown(
    '<div class="section">💰 Pricing & Booking Behaviour</div>',
    unsafe_allow_html=True
)

c5, c6 = st.columns(2)

with c5:
    chart_title(
        "💵",
        "Average ADR by Hotel Type",
        "Compare average daily rate between hotel types."
    )

    if {"hotel", "adr"}.issubset(filtered.columns):
        adr_df = (
            filtered.groupby("hotel", as_index=False)["adr"]
            .mean()
        )

        fig = px.bar(
            adr_df,
            x="hotel",
            y="adr",
            text_auto=".2f",
            color="hotel",
            color_discrete_sequence=[PRIMARY, ORANGE]
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Average ADR"
        )

        fig.update_traces(
            textposition="outside",
            textfont_size=9
        )

        st.plotly_chart(
            polish(fig, 275),
            use_container_width=True
        )

with c6:
    chart_title(
        "⏱",
        "Lead Time Distribution",
        "Understand how early guests typically make reservations."
    )

    if "lead_time" in filtered.columns:
        lead = filtered["lead_time"].dropna()

        # Keep the chart readable by limiting the visible range
        lead_plot = lead[lead <= lead.quantile(0.98)]

        fig = px.histogram(
            lead_plot,
            x="lead_time",
            nbins=30
        )

        fig.update_traces(
            marker_color=CYAN,
            opacity=0.85
        )

        fig.update_layout(
            xaxis_title="Lead Time (days)",
            yaxis_title="Bookings"
        )

        st.plotly_chart(
            polish(fig, 275),
            use_container_width=True
        )

# =========================================================
# 14. TOP CITIES / ORIGIN
# =========================================================

c7, c8 = st.columns(2)

with c7:
    city_col = None

    if "city" in filtered.columns:
        city_col = "city"
    elif "country" in filtered.columns:
        city_col = "country"

    chart_title(
        "🌍",
        "Top Guest Origin",
        "Highest-volume guest origin locations."
    )

    if city_col:
        origin = (
            filtered[city_col]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .reset_index()
        )

        origin.columns = ["Origin", "Bookings"]

        fig = px.bar(
            origin,
            x="Bookings",
            y="Origin",
            orientation="h",
            text_auto=",",
            color="Bookings",
            color_continuous_scale="Viridis"
        )

        fig.update_layout(
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed"),
            xaxis_title="Bookings",
            yaxis_title=None
        )

        st.plotly_chart(
            polish(fig, 300),
            use_container_width=True
        )
    else:
        st.info("No city/country column is available in the dataset.")

with c8:
    chart_title(
        "⭐",
        "Special Requests",
        "Booking volume by number of special requests."
    )

    if "total_of_special_requests" in filtered.columns:
        req = (
            filtered["total_of_special_requests"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        req.columns = ["Requests", "Bookings"]

        fig = px.bar(
            req,
            x="Requests",
            y="Bookings",
            text_auto=",",
            color="Bookings",
            color_continuous_scale="Plasma"
        )

        fig.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Special Requests",
            yaxis_title="Bookings"
        )

        st.plotly_chart(
            polish(fig, 300),
            use_container_width=True
        )

# =========================================================
# 15. KEY BUSINESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="section">💡 Key Business Insights</div>',
    unsafe_allow_html=True
)

top_market = "N/A"
top_market_count = 0
top_hotel = "N/A"
top_hotel_count = 0
top_origin = "N/A"
top_origin_count = 0

if total > 0:

    if "market_segment" in filtered.columns:
        s = filtered["market_segment"].value_counts()
        if len(s):
            top_market = s.index[0]
            top_market_count = int(s.iloc[0])

    if "hotel" in filtered.columns:
        s = filtered["hotel"].value_counts()
        if len(s):
            top_hotel = s.index[0]
            top_hotel_count = int(s.iloc[0])

    if city_col:
        s = filtered[city_col].fillna("Unknown").value_counts()
        if len(s):
            top_origin = s.index[0]
            top_origin_count = int(s.iloc[0])

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.markdown(
        f"""
        <div class="insight" style="border-top:3px solid {RED};">
            <div class="insight-title">⚠️ Cancellation Risk</div>
            <div class="insight-body">
                Cancellation rate is
                <b style="color:{RED};">{cancel_rate:.1f}%</b>.
                This indicates the level of booking volume exposed
                to cancellation-related revenue uncertainty.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with i2:
    st.markdown(
        f"""
        <div class="insight" style="border-top:3px solid {PRIMARY};">
            <div class="insight-title">📊 Leading Channel</div>
            <div class="insight-body">
                <b style="color:{PRIMARY};">{top_market}</b>
                is the largest market segment with
                <b>{top_market_count:,}</b> bookings.
                Marketing effort can be aligned with this demand source.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with i3:
    st.markdown(
        f"""
        <div class="insight" style="border-top:3px solid {CYAN};">
            <div class="insight-title">🏨 Strongest Hotel Type</div>
            <div class="insight-body">
                <b style="color:{CYAN};">{top_hotel}</b>
                contributes the highest booking volume with
                <b>{top_hotel_count:,}</b> bookings in the current selection.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with i4:
    st.markdown(
        f"""
        <div class="insight" style="border-top:3px solid {GREEN};">
            <div class="insight-title">🌍 Top Origin</div>
            <div class="insight-body">
                <b style="color:{GREEN};">{top_origin}</b>
                is the leading guest origin with
                <b>{top_origin_count:,}</b> bookings.
                This can support targeted acquisition campaigns.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 16. MANAGEMENT RECOMMENDATIONS
# =========================================================

st.markdown(
    '<div class="section">🎯 Management Recommendations</div>',
    unsafe_allow_html=True
)

r1, r2, r3 = st.columns(3)

with r1:
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">1. Reduce Cancellation Exposure</div>
            <div class="insight-body">
                Use deposit policies, reminder messages and
                differentiated cancellation rules for segments
                with higher cancellation exposure.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r2:
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">2. Optimize Pricing</div>
            <div class="insight-body">
                Current average ADR is
                <b>${avg_adr:.2f}</b>.
                Compare ADR with monthly demand and hotel type
                before changing room rates.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r3:
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">3. Improve Demand Planning</div>
            <div class="insight-body">
                Average lead time is
                <b>{avg_lead:.0f} days</b>.
                Use booking lead-time patterns to plan staffing,
                promotions and inventory availability.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================================
# 17. FOOTER
# =========================================================

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:{MUTED};
        font-size:9px;
        padding:22px 0 5px 0;
    ">
        🏨 Hotel Business Analytics
        &nbsp;•&nbsp;
        Python + Pandas + Plotly + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
