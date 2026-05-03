import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Supermarket Pricing Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Supermarket Pricing Dashboard")
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

# Add sidebar filters
st.sidebar.header("Filters")

selected_date = st.sidebar.selectbox(
    "Collection date",
    sorted(df["date"].dt.date.unique())
)

selected_category = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

selected_chain = st.sidebar.multiselect(
    "Chain",
    sorted(df["chain"].dropna().unique()),
    default=sorted(df["chain"].dropna().unique())
)

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
st.subheader("Price Index by Chain")

chain_index = (
    indexed_df.groupby("chain")["price_index"]
    .mean()
    .sort_values()
    .reset_index()
)

fig_chain = px.bar(
    chain_index,
    x="chain",
    y="price_index",
    title="Average Price Index by Chain",
    labels={"price_index": "Price Index (Market Average = 100)", "chain": "Chain"}
)

fig_chain.add_hline(y=100, line_dash="dash")

st.plotly_chart(fig_chain, use_container_width=True)

# Chart 2: Price Index by category and chain
st.subheader("Price Index by Category and Chain")

category_chain = (
    indexed_df.groupby(["category", "chain"])["price_index"]
    .mean()
    .reset_index()
)

fig_heatmap = px.density_heatmap(
    category_chain,
    x="chain",
    y="category",
    z="price_index",
    title="Price Index Heatmap by Category and Chain",
    labels={"price_index": "Price Index"}
)

st.plotly_chart(fig_heatmap, use_container_width=True)

# Chart 3: Cheapest chain per category
st.subheader("Cheapest Chain per Category")

cheapest = category_chain.loc[
    category_chain.groupby("category")["price_index"].idxmin()
].sort_values("category")

st.dataframe(
    cheapest.rename(columns={"chain": "Cheapest Chain", "price_index": "Price Index"}),
    use_container_width=True
)

# Chart 4: Basket simulation
st.subheader("Fixed Basket Cost Comparison")

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

fig_basket = px.bar(
    basket_total,
    x="basket_total_eur",
    y="chain",
    orientation="h",
    title="Fixed Basket Cost by Chain",
    labels={"basket_total_eur": "Basket Cost (€)", "chain": "Chain"}
)

st.plotly_chart(fig_basket, use_container_width=True)

# Chart 5: Temporal comparison
st.subheader("Price Changes Between Snapshots")

temporal_df = df.copy()
temporal_df = df[
    df["comparability_flag"].isna()
    | (df["comparability_flag"] == "comparable")
]

if "comparability_flag" in temporal_df.columns:
    temporal_df = temporal_df[
        temporal_df["comparability_flag"].isna()
        | (temporal_df["comparability_flag"] == "comparable")
    ].copy()

pivot_time = temporal_df.pivot_table(
    index=["product_id", "chain"],
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

    fig_changes = px.histogram(
        changes,
        x="percent_change",
        nbins=30,
        title="Distribution of Price Changes Between Snapshots",
        labels={"percent_change": "% Change"}
    )

    st.plotly_chart(fig_changes, use_container_width=True)

    st.dataframe(
        changes.sort_values("percent_change", ascending=False).head(15),
        use_container_width=True
    )
else:
    st.info("Temporal comparison requires at least two collection dates.")

# Raw data viewer
st.subheader("Filtered Dataset")
st.dataframe(filtered_df, use_container_width=True)