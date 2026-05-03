import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Supermarket Pricing Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

h1, h2, h3 {
    color: #2F2F2F;
}

[data-testid="stMetric"] {
    background-color: #F7F4EF;
    padding: 1rem;
    border-radius: 14px;
    border: 1px solid #E8E2D8;
}

[data-testid="stExpander"] {
    border: 1px solid #E8E2D8;
    border-radius: 12px;
}
            
.stMultiSelect [data-baseweb="tag"] {
    background-color: #6B8F71 !important;
    color: white !important;
    border-radius: 999px !important;
    font-weight: 600 !important;
}

.stMultiSelect [data-baseweb="tag"] span {
    color: white !important;
}

.stMultiSelect [data-baseweb="tag"] svg {
    fill: white !important;
}
            
            div[data-baseweb="select"] > div {
    border-color: #E8E2D8 !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: #6B8F71 !important;
    box-shadow: 0 0 0 1px #6B8F71 !important;
}
</style>
""", unsafe_allow_html=True)

PALETTE = {
    "primary": "#6B8F71",
    "secondary": "#D9A441",
    "accent": "#A67C52", 
    "light": "#F7F4EF",
    "dark": "#2F2F2F",
    "muted": "#8A8A8A"
}

CHAIN_COLORS = {
    "Mercadona": "#6B8F71",
    "Consum": "#D9A441",
    "Carrefour": "#8FB3A3",
    "Dia": "#C97C5D",
    "Alcampo": "#A67C52"
}

st.title("Supermarket Pricing Dashboard")
st.markdown(
    """
    Competitive pricing analysis across five Spanish supermarket chains:
    **Mercadona, Consum, Carrefour, Dia, and Alcampo**.
    """
)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_excel("data/Dataset.xlsx")

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    df["date"] = pd.to_datetime(df["date"])

    return df

df = load_data()

CATEGORY_LABELS = {
    "breakfast": "Breakfast",
    "cleaning": "Cleaning",
    "dairy": "Dairy",
    "fresh produce": "Fresh Produce",
    "snacks": "Snacks"
}

DATE_LABELS = {
    d.date(): d.strftime("%d-%m-%Y")
    for d in sorted(df["date"].dropna().unique())
}

# Filters
all_dates = sorted(df["date"].dt.date.unique())
all_categories = sorted(df["category"].dropna().unique())
all_chains = sorted(df["chain"].dropna().unique())

with st.form("filters_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_date = st.selectbox(
            "Collection date",
            all_dates,
            format_func=lambda x: DATE_LABELS[x]
        )

    with col2:
        selected_category = st.multiselect(
            "Category",
            all_categories,
            default=all_categories,
            format_func=lambda x: CATEGORY_LABELS.get(x, x.title())
        )

    with col3:
        selected_chain = st.multiselect(
            "Chain",
            all_chains,
            default=all_chains
        )

    apply_filters = st.form_submit_button("Apply filters")

filtered_df = df[
    (df["date"].dt.date == selected_date)
    & (df["category"].isin(selected_category))
    & (df["chain"].isin(selected_chain))
].copy()

# Create a clean analysis dataframe
analysis_df = filtered_df.copy()

if "comparability_flag" in analysis_df.columns:
    analysis_df = analysis_df[
        analysis_df["comparability_flag"].isna()
        | (analysis_df["comparability_flag"] == "comparable")
    ].copy()

# Add KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Rows", len(filtered_df))
col2.metric("Products", filtered_df["product_id"].nunique())
col3.metric("Chains", filtered_df["chain"].nunique())
col4.metric("Categories", filtered_df["category"].nunique())

# Price index function
def calculate_price_index(data):
    product_avg = (
        data.groupby("product_id")["price_per_unit"]
        .mean()
        .reset_index(name="product_market_avg")
    )

    indexed = data.merge(product_avg, on="product_id", how="left")

    indexed["price_index"] = (
        indexed["price_per_unit"] / indexed["product_market_avg"] * 100
    )

    return indexed

# Calculate price index
indexed_df = calculate_price_index(analysis_df)

# Chart 1: Price Index by chain
st.header("1. Overall price positioning")
st.subheader("Price Index by Chain")

chain_index = (
    indexed_df.groupby("chain")["price_index"]
    .mean()
    .sort_values()
    .reset_index()
)

fig_chain = px.bar(
    chain_index.sort_values("price_index"),
    x="price_index",
    y="chain",
    orientation="h",
    text=chain_index["price_index"].round(1),
    color="chain",
    color_discrete_map=CHAIN_COLORS,
    labels={"price_index": "Price Index", "chain": ""}
)

fig_chain.add_vline(x=100, line_dash="dash", line_color="#8A8A8A")

fig_chain.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color=PALETTE["dark"]),
)

st.plotly_chart(fig_chain, use_container_width=True)

def insight_box(text):
    st.markdown(
        f"""
        <div style="
            background-color: #F7F4EF;
            border-left: 5px solid #6B8F71;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            margin: 1rem 0 2rem 0;
            color: #2F2F2F;
        ">
            <strong>Insight:</strong><br>
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )

if chain_index["chain"].nunique() >= 2:
    best_chain = chain_index.iloc[0]["chain"]
    best_index = chain_index.iloc[0]["price_index"]

    worst_chain = chain_index.iloc[-1]["chain"]
    worst_index = chain_index.iloc[-1]["price_index"]

    insight_box(
    f"{best_chain} has the lowest price index ({best_index:.1f}), "
    f"while {worst_chain} has the highest ({worst_index:.1f}) for the current selection."
)
else:
    st.info(
        "Select at least two chains to compare price positioning."
    )

# Chart 2: Heatmap
st.header("2. Category-level positioning")
st.subheader("Price Index by Category and Chain")

category_chain = (
    indexed_df.groupby(["category", "chain"])["price_index"]
    .mean()
    .reset_index()
)

pivot_table = category_chain.pivot(
    index="category",
    columns="chain",
    values="price_index"
)

fig_heatmap = px.imshow(
    pivot_table,
    text_auto=".1f",
    color_continuous_scale="RdYlGn_r",
    zmin=90,
    zmax=110,
    labels=dict(color="Price Index")
)

fig_heatmap.update_layout(
    xaxis_title="Chain",
    yaxis_title="Category"
)

st.plotly_chart(fig_heatmap, use_container_width=True)

insight_box(
    "Pricing leadership varies by category, suggesting that chains do not follow a single low-price strategy across the full basket."
)

# Chart 3: Cheapest chain per category
st.header("3. Cheapest chain by category")

cheapest = category_chain.loc[
    category_chain.groupby("category")["price_index"].idxmin()
].sort_values("price_index")

fig_cheapest = px.bar(
    cheapest,
    x="price_index",
    y="category",
    orientation="h",
    text="chain",
    color="chain",
    color_discrete_map=CHAIN_COLORS,
    labels={
        "price_index": "Price Index",
        "category": "",
        "chain": "Cheapest Chain"
    }
)

fig_cheapest.add_vline(x=100, line_dash="dash", line_color=PALETTE["muted"])

fig_cheapest.update_traces(
    textposition="outside",
    textfont=dict(
        size=13,
        color=PALETTE["dark"],
        family="Arial Black"
    )
)

fig_cheapest.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color=PALETTE["dark"]),
    xaxis_title="Price Index",
    yaxis_title=""
)

st.plotly_chart(fig_cheapest, use_container_width=True)

best_category = cheapest.iloc[0]["category"]
best_chain_category = cheapest.iloc[0]["chain"]
best_category_index = cheapest.iloc[0]["price_index"]

insight_box(
    f"{best_chain_category} is the strongest category-level price leader, "
    f"with the lowest observed category index in {best_category} "
    f"({best_category_index:.1f})."
)

# Chart 4: Basket simulation
st.header("4. Fixed basket cost")

basket_df = analysis_df[
    analysis_df["private_label"].astype(str).str.lower() == "yes"
].copy()

complete_products = (
    basket_df.groupby("product_id")["chain"]
    .nunique()
)

complete_products = complete_products[
    complete_products == basket_df["chain"].nunique()
].index

basket_df = basket_df[basket_df["product_id"].isin(complete_products)]

basket_total = (
    basket_df.groupby("chain")["price_eur"]
    .sum()
    .sort_values()
    .reset_index(name="basket_total_eur")
)

basket_total = basket_total.sort_values("basket_total_eur")

fig_basket = px.bar(
    basket_total.sort_values("basket_total_eur"),
    x="basket_total_eur",
    y="chain",
    orientation="h",
    text=basket_total["basket_total_eur"].round(2),
    color="chain",
    color_discrete_map=CHAIN_COLORS,
    labels={"basket_total_eur": "Basket Cost (€)", "chain": ""}
)

fig_basket.update_layout(
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(color=PALETTE["dark"])
)

st.plotly_chart(fig_basket, use_container_width=True)

basket_cheapest = basket_total.iloc[0]["chain"]
basket_cost = basket_total.iloc[0]["basket_total_eur"]

insight_box(
    f"{basket_cheapest} offers the lowest fixed basket cost at €{basket_cost:.2f}, "
    "based only on comparable private-label products available across all chains."
)

# Chart 5: Temporal comparison
st.header("5. Price stability over time")

temporal_df = df.copy()

if "comparability_flag" in temporal_df.columns:
    temporal_df = temporal_df[
        temporal_df["comparability_flag"].isna()
        | (temporal_df["comparability_flag"] == "comparable")
    ].copy()

pivot_time = temporal_df.pivot_table(
    index=["product_id", "chain", "category"],
    columns="date",
    values="price_per_unit"
)

if pivot_time.shape[1] >= 2:
    first_date = pivot_time.columns.min()
    second_date = pivot_time.columns.max()

    pivot_time["percent_change"] = (
        (pivot_time[second_date] - pivot_time[first_date])
        / pivot_time[first_date]
        * 100
    )

    changes = pivot_time.reset_index()
    changes = changes.dropna(subset=["percent_change"])

    stable_share = (changes["percent_change"].abs() <= 1).mean() * 100
    changed_products = (changes["percent_change"].abs() > 1).sum()

    col1, col2 = st.columns(2)
    col1.metric("Stable prices", f"{stable_share:.0f}%")
    col2.metric("Meaningful changes", changed_products)

    insight_box(
        f"{stable_share:.0f}% of comparable product-chain pairs changed by 1% or less, "
        "suggesting high short-term price stability across the two-week period."
    )

    category_changes = (
        changes
        .assign(abs_change=changes["percent_change"].abs())
        .groupby("category")["abs_change"]
        .mean()
        .sort_values()
        .reset_index()
    )

    category_changes["category_label"] = category_changes["category"].map(
        lambda x: CATEGORY_LABELS.get(x, x.title())
    )

    fig_stability = px.bar(
        category_changes,
        x="abs_change",
        y="category_label",
        orientation="h",
        text=category_changes["abs_change"].round(1),
        labels={
            "abs_change": "Average absolute price change (%)",
            "category_label": ""
        }
    )

    fig_stability.update_traces(
        marker_color=PALETTE["primary"],
        textposition="outside",
        textfont=dict(color=PALETTE["dark"], size=12)
    )

    fig_stability.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=PALETTE["dark"]),
        showlegend=False,
        xaxis_title="Average absolute price change (%)",
        yaxis_title=""
    )

    st.plotly_chart(fig_stability, use_container_width=True)

else:
    insight_box("Temporal comparison requires at least two collection dates.")

with st.expander("View detailed price changes"):
    st.dataframe(changes.sort_values("percent_change", ascending=False))

# Raw data viewer
st.header("Dataset expander")
with st.expander("View dataset"):
    st.dataframe(df)