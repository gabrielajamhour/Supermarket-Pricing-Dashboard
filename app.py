# --------------- IMPORTS --------------- #
import streamlit as st
import pandas as pd
import plotly.express as px


# --------------- PAGE CONFIGURATION --------------- #
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

[data-testid="stDataFrame"] {
    overflow-x: auto;
}
            
.stMultiSelect [data-baseweb="tag"] {
    background-color: #417c94 !important;
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
    border-color: #417c94 !important;
    box-shadow: 0 0 0 1px #417c94 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #8A8A8A;
    font-weight: 600;
    border-radius: 8px 8px 0 0;
    padding: 0.5rem 1rem;
}

/* Active tab */
button[data-baseweb="tab"][aria-selected="true"] {
    color: #417c94 !important;
    border-bottom: 3px solid #417c94 !important;
    background-color: #F7F4EF !important;
}

/* Hover */
button[data-baseweb="tab"]:hover {
    color: #417c94 !important;
}

/* Remove default red focus/active line */
button[data-baseweb="tab"]:focus,
button[data-baseweb="tab"]:active {
    box-shadow: none !important;
}

/* Underline indicator */
[data-baseweb="tab-highlight"] {
    background-color: #417c94 !important;
}
</style>
""", unsafe_allow_html=True)


# --------------- LOAD DATASET --------------- #
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


# --------------- GLOBAL VARIABLES --------------- #

PALETTE = {
    "primary": "#417c94",
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

CATEGORY_LABELS = {
    "breakfast": "Breakfast",
    "cleaning": "Cleaning",
    "dairy": "Dairy",
    "fresh produce": "Fresh Produce",
    "snacks": "Snacks"
}

REFERENCE_QUANTITIES = {
    "dairy_milk_whole_1l": 1,
    "dairy_milk_semi_1L": 1,
    "dairy_yogurt_greek_1kg": 1,
    "dairy_yogurt_natural_pack_125g": 0.125,
    "dairy_yogurt_natural_pack_120g_branded": 0.12,
    "dairy_cheese_sliced_approx_200g": 0.2,
    "dairy_cheese_grated_200g": 0.2,
    "breakfast_cereals_cornflakes_500g": 0.5,
    "breakfast_cereals_cornflakes_500g_branded": 0.5,
    "breakfast_cereals_chocolate_approx_500g": 0.5,
    "breakfast_juice_orange_not_from_concentrate_1L": 1,
    "breakfast_juice_orange_from_concentrate_1L": 1,
    "breakfast_coffee_ground_approx_250g": 0.25,
    "breakfast_coffee_capsules_with_milk_16": 16,
    "cleaning_dishwasher_tablets_approx_30u": 30,
    "cleaning_dishwasher_tablets_approx_30u_branded": 30,
    "cleaning_dishwasher_gel_approx_750ml": 0.75,
    "cleaning_laundry_liquid_approx_3L": 3,
    "cleaning_laundry_capsules_approx_25u": 25,
    "fresh_eggs_size_M_12u": 12,
    "fresh_eggs_size_L_12u": 12,
    "fresh_eggs_free_range_approx_12u": 12,
    "fresh_chicken_breast_approx_500g": 0.5,
    "fresh_bananas_kg": 1,
    "snacks_crisps_salted_300g": 0.3,
    "snacks_crisps_salted_248g_branded": 0.248,
    "snacks_crisps_ham_approx_150g": 0.15,
    "snacks_biscuits_digestive_approx_400_800g": 0.8,
    "snacks_biscuits_cookies_approx_200g": 0.2,
    "snacks_chocolate_milk_approx_100g": 0.1,
    "snacks_chocolate_dark_85_100g": 0.1,
}

DATE_LABELS = {
    d.date(): d.strftime("%d-%m-%Y")
    for d in sorted(df["date"].dropna().unique())
}


# --------------- TITLE --------------- #
style_align_text = 'text-align: center'
st.markdown(f"<h1 style='{style_align_text}'>Supermarket Pricing Dashboard</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='{style_align_text}'>Competitive pricing analysis across five Spanish supermarket chains: <strong>Mercadona, Consum, Carrefour, Dia and Alcampo</strong>.</p>", unsafe_allow_html=True)


# --------------- FILTERS --------------- #

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


# --------------- HELPER FUNCTIONS --------------- #

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

# Insight box function
def insight_box(finding, interpretation=None, implication=None):
    content = f"<strong>Finding:</strong><br>{finding}<br><br>"

    if interpretation:
        content += f"<strong>Interpretation:</strong><br>{interpretation}<br><br>"

    if implication:
        content += f"<strong>Implication:</strong><br>{implication}"

    st.markdown(
        f"""
        <div style="
            background-color: #F7F4EF;
            border-left: 5px solid #417c94;
            padding: 1rem 1.2rem;
            border-radius: 12px;
            margin: 1rem 0 2rem 0;
        ">
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

# Build implication function
def build_implication(best_chain, best_index, worst_chain, worst_index):
    spread = worst_index - best_index

    # tight market → little differentiation
    if spread < 3:
        return (
            "The pricing spread across chains is very narrow, indicating a highly competitive market "
            "where retailers are closely tracking each other rather than differentiating on price."
        )

    # moderate spread → segmented competition
    elif spread < 6:
        return (
            "There is a moderate pricing gap across chains, suggesting partial differentiation. "
            "Some retailers are competing on efficiency while others tolerate higher price positioning in exchange for margin."
        )

    # wide spread → structural divergence
    else:
        return (
            "The pricing gap across chains is substantial, pointing to structurally different pricing strategies. "
            "Some retailers appear to prioritise volume leadership, while others operate with a clear premium positioning."
        )

# Format changes table function
def format_changes_table(data):
        formatted = data.copy()

        formatted["category"] = formatted["category"].map(
            lambda x: CATEGORY_LABELS.get(x, x.title())
        )

        formatted = formatted.rename(columns={
            "product_id": "Product",
            "chain": "Chain",
            "category": "Category",
            "percent_change": "Change (%)"
        })

        return formatted[["Product", "Chain", "Category", "Change (%)"]]


# --------------- VARIABLES --------------- #

# Filtered dataset (base selection from UI)
filtered_df = df[
    (df["date"].dt.date == selected_date)
    & (df["category"].isin(selected_category))
    & (df["chain"].isin(selected_chain))
].copy()

# Comparable-only analysis dataset
analysis_df = filtered_df.copy()

if "comparability_flag" in analysis_df.columns:
    analysis_df = analysis_df[
        (analysis_df["comparability_flag"].isna()) |
        (analysis_df["comparability_flag"] == "comparable")
    ].copy()

# Temporal dataset (full history, not filtered by selected date)
temporal_df = df.copy()

if "comparability_flag" in temporal_df.columns:
    temporal_df = temporal_df[
        (temporal_df["comparability_flag"].isna()) |
        (temporal_df["comparability_flag"] == "comparable")
    ].copy()

# Pivot for temporal comparison
pivot_time = temporal_df.pivot_table(
    index=["product_id", "chain", "category"],
    columns="date",
    values="price_per_unit"
)

# Default empty structures (prevents KeyError downstream)
changes = pivot_time.reset_index()
category_changes = pd.DataFrame(
    columns=["category", "abs_change", "category_label"]
)

# --------------- TEMPORAL CALCULATIONS --------------- #

if pivot_time.shape[1] >= 2:

    first_date = pivot_time.columns.min()
    last_date = pivot_time.columns.max()

    # Percent change across the period
    pivot_time["percent_change"] = (
        (pivot_time[last_date] - pivot_time[first_date])
        / pivot_time[first_date]
        * 100
    )

    changes = pivot_time.reset_index()

    # Stability metrics (safe now)
    stable_share = (changes["percent_change"].abs() <= 1).mean() * 100
    changed_products = (changes["percent_change"].abs() > 1).sum()

    # Category-level volatility
    category_changes = (
        changes
        .assign(abs_change=changes["percent_change"].abs())
        .groupby("category")["abs_change"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    category_changes["category_label"] = category_changes["category"].map(
        lambda x: CATEGORY_LABELS.get(x, x.title())
    )

# Safe cleanup (only if column exists)
if "percent_change" in changes.columns:
    changes = changes.dropna(subset=["percent_change"])


# --------------- EXECUTIVE SUMMARY METRICS --------------- #

# Calculate price index
indexed_df = calculate_price_index(analysis_df)

chain_index = (
    indexed_df.groupby("chain")["price_index"]
    .mean()
    .sort_values()
    .reset_index()
)

best_chain = chain_index.iloc[0]["chain"]
best_index = chain_index.iloc[0]["price_index"]

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

basket_df = basket_df[
    basket_df["product_id"].isin(complete_products)
].copy()

basket_df["reference_quantity"] = (
    basket_df["product_id"]
    .map(REFERENCE_QUANTITIES)
)

basket_df = basket_df.dropna(subset=["reference_quantity"])

basket_df["equivalent_cost"] = (
    basket_df["price_per_unit"]
    * basket_df["reference_quantity"]
)

basket_total = (
    basket_df.groupby("chain")["equivalent_cost"]
    .sum()
    .sort_values()
    .reset_index(name="basket_total_eur")
)

basket_cheapest = basket_total.iloc[0]["chain"]
basket_cost = basket_total.iloc[0]["basket_total_eur"]

basket_expensive = basket_total.iloc[-1]["chain"]
basket_expensive_cost = basket_total.iloc[-1]["basket_total_eur"]

basket_gap = basket_expensive_cost - basket_cost

basket_gap_pct = (
    (basket_expensive_cost - basket_cost)
    / basket_cost
    * 100
)

pl_brand_df = analysis_df.copy()

pl_brand_df = pl_brand_df[
    pl_brand_df["private_label"].notna()
]

pl_brand_df["label_type"] = pl_brand_df["private_label"].apply(
    lambda x: "Private Label"
    if str(x).lower() == "yes"
    else "Branded"
)

comparison = (
    pl_brand_df.groupby(
        ["category", "label_type"]
    )["price_per_unit"]
    .mean()
    .reset_index()
)

comparison["category_label"] = comparison["category"].map(
    lambda x: CATEGORY_LABELS.get(x, x.title())
)

pl_summary = (
    comparison
    .pivot(
        index="category_label",
        columns="label_type",
        values="price_per_unit"
    )
)

pl_summary["premium_pct"] = (
    (pl_summary["Branded"] - pl_summary["Private Label"])
    / pl_summary["Private Label"]
    * 100
)

largest_premium_category = (
    pl_summary["premium_pct"]
    .idxmax()
)

largest_premium = (
    pl_summary["premium_pct"]
    .max()
)


# --------------- KPI CARDS --------------- #
col1, col2, col3, col4 = st.columns(4)

col1.metric("Cheapest equivalent basket", basket_cheapest)
col2.metric("Basket gap", f"{basket_gap_pct:.0f}%")
col3.metric("Most volatile category", category_changes.loc[
    category_changes["abs_change"].idxmax(), "category_label"
])
col4.metric("Avg market-relative index", f"{indexed_df['price_index'].mean():.1f}")

st.caption(
    "Price index metrics are relative to market averages, while basket metrics reflect absolute consumer spend."
)


# --------------- EXECUTIVE SUMMARY AND METHODOLOGY --------------- #

executive_summary = f"""
<div style="
    background-color: #F7F4EF;
    padding: 1.2rem;
    border-radius: 14px;
    border: 1px solid #E8E2D8;
    margin-top: 1rem;
    margin-bottom: 2rem;
">
<b>Executive summary</b><br><br>

• {best_chain} shows the most competitive overall pricing ({best_index:.1f}).<br>

• The equivalent basket in {basket_expensive} costs
approximately {basket_gap_pct:.0f}% more than in {basket_cheapest}.<br>

• The largest branded premium appears in {largest_premium_category},
where branded products cost roughly {largest_premium:.0f}% more than private-label alternatives.<br>

• Most prices remained stable across the two-week comparison period.
</div>
"""

st.markdown(executive_summary, unsafe_allow_html=True)

with st.expander("Methodology"):
    st.markdown("""
    - Products were manually collected from five Spanish supermarket chains across two collection periods.
    - Functional equivalence was prioritised over exact brand matching to improve cross-chain comparability.
    - Products flagged as not comparable were excluded from indexed analysis.
    - Price indices were normalised relative to the market average for each product.
    - Basket comparisons use standardised reference quantities to reduce package-size distortions.
    - Temporal analysis compares identical product-chain pairs between snapshots.
    """)


# --------------- SIDEBAR --------------- #

st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Go to:",
    [
        "Overview",
        "1. Overall price positioning",
        "2. Category-level positioning",
        "3. Category price leadership",
        "4. Equivalent basket cost",
        "5. Brand premium analysis",
        "6. Cost per use — cleaning",
        "7. Short-term pricing dynamics",
        "8. Product deep dive",
        "View filtered dataset",
    ]
)

show_all = (section == "Overview")


# --------------- SECTION 1: OVERALL PRICE POSITIONING --------------- #

if section == "Overall price positioning" or show_all:
    st.markdown("---")
    st.header("1. Overall price positioning")

    worst_chain = chain_index.iloc[-1]["chain"]
    worst_index = chain_index.iloc[-1]["price_index"]

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

    fig_chain.update_xaxes(range=[90, 110])

    st.plotly_chart(fig_chain, width='stretch')

    if chain_index["chain"].nunique() >= 2:
        insight_box(
            f"{best_chain} leads the pricing index at {best_index:.1f}, while {worst_chain} sits at {worst_index:.1f}.",

            interpretation=build_implication(best_chain, best_index, worst_chain, worst_index),

            implication=(
                "In this type of structure, competitive advantage is likely driven more by category-level positioning "
                "than by overall price leadership, meaning that basket composition matters more than global pricing strategy."
            )
        )
    else:
        st.info(
            "Select at least two chains to compare price positioning."
        )


# --------------- SECTION 2: CATEGORY-LEVEL POSITIONING --------------- #

if section == "Category-level positioning" or show_all:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("2. Category-level positioning")

    category_chain = (
        indexed_df.groupby(["category", "chain"])["price_index"]
        .mean()
        .reset_index()
    )

    dispersion = (
        indexed_df.groupby("category")["price_per_unit"]
        .std()
        .reset_index(name="std_dev")
        .sort_values("std_dev", ascending=False)
    )

    dispersion["category_label"] = dispersion["category"].map(
        lambda x: CATEGORY_LABELS.get(x, x.title())
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

    st.plotly_chart(fig_heatmap, width='stretch')

    fig_dispersion = px.bar(
        dispersion,
        x="std_dev",
        y="category_label",
        orientation="h",
        text=dispersion["std_dev"].round(2),
        color="std_dev",
        color_continuous_scale=["#E8E2D8", "#417c94"]
    )

    fig_dispersion.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=PALETTE["dark"]),
        showlegend=False
    )

    st.plotly_chart(fig_dispersion, width='stretch')

    insight_box(
        "Category-level indices show clear variation in leadership across chains, rather than a single dominant retailer.",
        
        interpretation=(
            "This indicates that pricing strategy is not unified across the assortment — "
            "chains likely optimise categories independently based on demand elasticity and competitive pressure."
        ),

        implication=(
            "Retail competition is therefore fragmented: winning in one category does not translate into overall dominance, "
            "which increases the importance of mix management."
        )
    )


# --------------- SECTION 3: CATEGORY PRICE LEADERSHIP --------------- #

if section == "Category price leadership" or show_all:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("3. Category price leadership")

    cheapest = category_chain.loc[
        category_chain.groupby("category")["price_index"].idxmin()
    ].sort_values("category")

    cheapest_display = cheapest.copy()

    cheapest_display["Category"] = cheapest_display["category"].map(
        lambda x: CATEGORY_LABELS.get(x, x.title())
    )

    cheapest_display["Cheapest Chain"] = cheapest_display["chain"]

    cheapest_display["Price Index"] = cheapest_display["price_index"].round(1)

    cheapest_display = cheapest_display[
        ["Category", "Cheapest Chain", "Price Index"]
    ]

    category_wins = (
        cheapest["chain"]
        .value_counts()
        .reset_index()
    )

    top_chain = category_wins.iloc[0]["chain"]
    top_wins = category_wins.iloc[0]["count"]

    fig_cheapest = px.bar(
        cheapest,
        x="price_index",
        y="category",
        color="chain",
        orientation="h",
        text=cheapest["price_index"].round(1),
        color_discrete_map=CHAIN_COLORS,
        labels={
            "price_index": "Lowest category index",
            "category": "",
            "chain": "Winning chain"
        }
    )

    fig_cheapest.update_traces(
        textposition="outside"
    )

    fig_cheapest.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=PALETTE["dark"]),
        xaxis_title="Lowest observed category index",
        yaxis_title=""
    )

    st.plotly_chart(fig_cheapest, width='stretch')

    st.caption(
        "Price leadership is distributed across chains rather than dominated by a single retailer."
        f"{top_chain} leads in {top_wins} categories, while other chains remain competitive in specific segments."
    )


# --------------- SECTION 4: EQUIVALENT BASKET COST --------------- #

if section == "Equivalent basket cost" or show_all:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("4. Equivalent basket cost")

    fig_basket = px.bar(
        basket_total,
        x="basket_total_eur",
        y="chain",
        orientation="h",
        text=basket_total["basket_total_eur"].round(2),
        color="chain",
        color_discrete_map=CHAIN_COLORS,
        labels={
            "basket_total_eur": "Equivalent Basket Cost (€)",
            "chain": ""
        }
    )

    fig_basket.update_traces(
        textposition="outside",
        textfont=dict(size=12, color=PALETTE["dark"])
    )

    fig_basket.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=PALETTE["dark"]),
        xaxis_title="Equivalent basket cost (€)",
        yaxis_title=""
    )

    st.plotly_chart(fig_basket, width='stretch')

    st.caption(
        "Basket comparisons use standardized reference quantities "
        "(e.g. 500g chicken breast, 1L milk, 30 washes detergent) to reduce "
        "distortions caused by package-size differences."
    )

    insight_box(
        f"{basket_cheapest} delivers the lowest standardized basket at €{basket_cost:.2f}, "
        f"while {basket_expensive} is €{basket_gap:.2f} higher.",

        interpretation=(
            "Because the basket is normalized using equivalent quantities and restricted to comparable items, "
            "the difference reflects structural efficiency rather than packaging or brand mix effects."
        ),

        implication=(
            "This suggests that cost leadership is consistent across essential goods, which is the segment "
            "most relevant for perceived affordability and price image."
        )
    )


# --------------- SECTION 5: BRAND PREMIUM ANALYSIS --------------- #

if section == "Brand premium analysis" or show_all:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("5. Brand premium analysis")

    fig_pl = px.bar(
        comparison,
        x="category_label",
        y="price_per_unit",
        color="label_type",
        barmode="group",
        labels={
            "category_label": "",
            "price_per_unit": "Average price per unit",
            "label_type": ""
        },
        color_discrete_map={
            "Private Label": PALETTE["primary"],
            "Branded": PALETTE["secondary"]
        }
    )

    fig_pl.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=PALETTE["dark"]),
        legend_title_text=""
    )

    st.plotly_chart(fig_pl, width='stretch')

    insight_box(
        f"The strongest brand premium appears in {largest_premium_category}, where branded products are significantly more expensive than private label.",

        interpretation=(
            "Premium dispersion across categories suggests that brand power is not uniform — "
            "it is concentrated in categories where perceived quality differences are more salient."
        ),

        implication=(
            "This creates strategic opportunity for retailers to expand private label penetration in high-premium categories, "
            "where consumers are more sensitive to price-quality trade-offs."
        )
    )


# --------------- SECTION 6: COST PER USE (CLEANING) --------------- #

if section == "Cost per use — cleaning" or show_all:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("6. Cost per use (cleaning products)")

    cost_df = analysis_df.copy()

    cost_df = cost_df[
        cost_df["category"] == "cleaning"
    ].copy()

    cost_df = cost_df.dropna(
        subset=["cost_per_use"]
    )

    cost_df["product_label"] = (
        cost_df["product_id"]
        .str.replace("_", " ")
        .str.title()
    )

    fig_cost = px.bar(
        cost_df,
        x="chain",
        y="cost_per_use",
        color="chain",
        facet_col="product_label",
        facet_col_wrap=2,
        text=cost_df["cost_per_use"].round(2),
        color_discrete_map=CHAIN_COLORS,
        labels={
            "cost_per_use": "Cost per use (€)",
            "chain": ""
        }
    )

    fig_cost.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    fig_cost.update_traces(
        textposition="outside"
    )

    fig_cost.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color=PALETTE["dark"]),
        showlegend=False,
        height=900
    )

    st.plotly_chart(fig_cost, width='stretch')

    st.caption(
        "Cleaning products show substantial cost-per-use differences between" 
        " brands and private-label alternatives. In several cases, branded dishwasher"
        " and laundry products cost 60–80% more per use than supermarket equivalents.",
    )


# --------------- SECTION 7: SHORT-TERM PRICING DYNAMICS --------------- #

if section == "Short-term pricing dynamics" or show_all:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.header("7. Short-term pricing dynamics")

    insight_box(
        "Most products remain stable across the two-week period, with only a small subset showing meaningful movement.",

        interpretation=(
            "Price adjustments are concentrated in specific branded items rather than broad category repricing, "
            "suggesting tactical rather than structural changes."
        ),

        implication=(
            "This indicates a pricing system driven by promotional cycles and targeted adjustments, "
            "rather than continuous market-wide inflation or deflation."
        )
    )

    with st.expander("View detailed price changes"):
        changes_display = changes.copy()
        changes_display = changes_display[changes_display["percent_change"].abs() > 1].copy()

        changes_display["direction"] = changes_display["percent_change"].apply(
            lambda x: "Increase" if x > 0 else "Decrease"
        )

        changes_display["percent_change"] = changes_display["percent_change"].round(1)

        increases = (
            changes_display[changes_display["direction"] == "Increase"]
            .sort_values("percent_change", ascending=False)
        )

        decreases = (
            changes_display[changes_display["direction"] == "Decrease"]
            .sort_values("percent_change")
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Price increases")
            st.dataframe(
                format_changes_table(increases),
                width='stretch',
                hide_index=True
            )

        with col2:
            st.markdown("#### Price decreases")
            st.dataframe(
                format_changes_table(decreases),
                width='stretch',
                hide_index=True
            )


# --------------- SECTION 8: PRODUCT DEEP DIVE --------------- #

if section == "Product deep dive" or show_all:
    st.markdown("---")
    st.header("8. Product deep dive")
    st.caption("Drill-down analysis at product level (selected independently from global view)")

    selected_product = st.selectbox(
        "Select a product",
        sorted(analysis_df["product_id"].unique())
    )

    # Current filtered snapshot (for market comparison)
    product_snapshot = analysis_df[
        analysis_df["product_id"] == selected_product
    ].copy()

    # Full historical data (for time evolution)
    product_history = df[
        df["product_id"] == selected_product
    ].copy()

    st.caption(
        f"Showing {product_history['chain'].nunique()} chains • "
        f"{product_history['date'].nunique()} dates • "
        f"{product_history['category'].iloc[0] if len(product_history) else ''}"
    )

    tabs = st.tabs([
        "Market position",
        "Price over time"
    ])

    # 1. MARKET POSITION
    with tabs[0]:

        product_avg = product_snapshot["price_per_unit"].mean()

        product_snapshot["relative_index"] = (
            product_snapshot["price_per_unit"]
            / product_avg
            * 100
        )

        fig_position = px.bar(
            product_snapshot,
            x="chain",
            y="relative_index",
            color="chain",
            text=product_snapshot["relative_index"].round(1),
            color_discrete_map=CHAIN_COLORS,
            labels={
                "relative_index": "Relative price index",
                "chain": ""
            }
        )

        fig_position.add_hline(
            y=100,
            line_dash="dash",
            line_color="#8A8A8A"
        )

        fig_position.update_traces(
            textposition="outside"
        )

        fig_position.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color=PALETTE["dark"]),
            showlegend=False
        )

        st.plotly_chart(
            fig_position,
            width='stretch'
        )

        st.caption(
            "Values above 100 indicate above-market pricing "
            "for the selected product."
        )

    # 2. PRICE OVER TIME
    with tabs[1]:

        fig_prod_time = px.line(
            product_history,
            x="date",
            y="price_per_unit",
            color="chain",
            markers=True,
            color_discrete_map=CHAIN_COLORS,
            labels={
                "price_per_unit": "Price per unit (€)",
                "date": "Date",
                "chain": ""
            }
        )

        fig_prod_time.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color=PALETTE["dark"]),
            legend_title_text=""
        )

        st.plotly_chart(
            fig_prod_time,
            width='stretch'
        )


# --------------- RAW DATA VIEWER --------------- #

if section == "View filtered dataset" or show_all:
    st.markdown("---")
    with st.expander("View filtered dataset"):
        st.dataframe(filtered_df)


# --------------- FOOTER --------------- #

st.caption(
    f"<p style='{style_align_text}'>Dashboard developed by Gabriela Rego Jamhour • Data collected manually across Spanish supermarket chains<br>Last updated: May 2026 • GitHub: https://github.com/gabrielajamhour/Supermarket-Pricing-Dashboard</p>",
    unsafe_allow_html=True
)
