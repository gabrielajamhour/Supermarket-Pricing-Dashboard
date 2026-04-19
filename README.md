# 🛒 Supermarket Pricing Dashboard

## 📌 Phase 1 — Scope Definition

The first phase of the project focused on defining a **clear, realistic, and analytically robust scope** before collecting any data. This step was essential to ensure that all subsequent analysis would be consistent, comparable, and meaningful.

### 🎯 Objective

The main objective of the project is to analyze pricing strategies and competitive positioning across major supermarket chains, combining data analysis with business-oriented insights.

### 🏪 Competitive Set

The analysis focuses on five supermarket chains operating in Spain:

* Mercadona
* Consum
* Carrefour
* Dia
* Alcampo

Originally, Lidl was considered as part of the competitive set. However, Consum was included instead of Lidl due to data accessibility constraints (website availability) and its strong regional presence in the Valencian market. This decision allowed for a more reliable and consistent data collection process, while maintaining a relevant representation of the local market.

### 🧺 Product Categories

To ensure comparability across chains, the analysis was structured around five core product categories:

* Dairy
* Breakfast
* Cleaning
* Fresh Produce
* Snacks

Within each category, a **consistent basket of 6–8 SKUs** was defined.

### 🧠 Product Selection Logic

One of the key challenges was that **exact product matches are not always available across all supermarkets**.

To address this, the following approach was adopted due to differences in product assortment across chains, exact product matches were not always available. Therefore, products were selected based on functional equivalence within each category, ensuring comparability at the category level rather than exact SKU level.

For example:

* Chocolate cereals were compared as a category (mainstream segment), not as identical brands.
* Private label and branded products were included depending on availability.

### ⚖️ Handling Packaging Variability

Products often differed in:

* weight (e.g. 375g vs 625g cereals)
* format (e.g. yogurt packs 4x125g vs 8x125g)

To ensure comparability, products with different packaging sizes were normalized using price per unit (€/kg or €/L). Additionally, products were grouped into approximate weight categories (e.g. ~500g) and normalized using price per unit to ensure consistency.

### 🥚 Controlling for Product Characteristics

In cases where standard pack sizes (e.g. 12 units) were not available, the closest private label alternative was selected (e.g. 10-unit packs in Dia), prioritising product segment consistency over packaging size. All comparisons were normalized using price per unit.

For laundry detergent, private label products were prioritised across all chains. Where multiple sizes were available, products closest to a ~3L standard were selected to reduce variability in packaging size while maintaining segment consistency.

When faced with trade-offs between packaging consistency and product segment consistency, I prioritised segment alignment to preserve the validity of price comparisons.

### 📌 Handling Missing Products

During data collection, not all products were available across every supermarket chain. For example, certain SKUs such as not-from-concentrate orange juice were not offered in Alcampo, and some size-specific products (e.g. medium eggs) were not consistently available across all chains.

To ensure data integrity and avoid distortions in the analysis, rows corresponding to unavailable products were excluded from the dataset, rather than being represented as empty (NaN) entries. This prevents incorrect aggregations (e.g. averages, counts) during data analysis.

This approach ensures that all calculations are based only on valid, observed data points, while maintaining transparency about product availability limitations across chains.

### 📌 Consumer-Relevant Metrics

While price per unit (€/kg, €/L, €/unit) was used as the primary normalization metric, additional consumer-relevant metrics were selectively introduced where applicable.

For certain cleaning products:

* Laundry liquid and dishwasher gel were evaluated using cost per use, based on the number of washes indicated on the packaging
* For products already measured per unit (e.g. capsules or tablets), price per unit was considered equivalent to cost per use

For all other products (e.g. food categories), cost per use was not applicable and therefore left empty.

This approach ensures that each category is evaluated using the most relevant metric from a consumer perspective, rather than applying a single metric uniformly.

### 📌 Data Collection Methodology
| Chain     |	Source Collection | Date  |	Method            |
| --------- | ----------------- | ----- | ----------------- |
| Mercadona |	Official website  | 19/04 |	Manual extraction |
| Consum	  | Official website  | 19/04 |	Manual extraction |
| Carrefour |	Official website  | 19/04 |	Manual extraction |
| Dia	      | Official website  | 19/04 |	Manual extraction |
| Alcampo   |	Official website  | 19/04 | Manual extraction |

All prices were collected from official supermarket websites on the same day to ensure temporal consistency. This approach minimizes bias due to price fluctuations and ensures comparability across chains.

### 📊 Key Performance Indicators (KPIs)

The analysis was designed around three groups of KPIs:

#### Price KPIs

* Average price by chain and category
* Price index (relative to market average = 100)
* Price per unit (€/kg, €/L, €/unit)

#### Competitive Positioning KPIs

* Cheapest chain per category
* Most expensive chain per category
* Price gap (%)

#### Brand Structure KPIs

* Private label share
* Private label price premium/discount vs branded products

### ⚙️ Constraints

The project was developed under the following constraints:

* Manual data collection (no scraping in MVP)
* One price snapshot per product per chain (with a second planned later)
* No store-level variation (one representative price per chain)
* Focus on the Spanish market (Valencia region)

### ✅ Definition of “Done”

The MVP is considered complete when:

* The dashboard allows filtering by chain, category, and brand type
* It clearly identifies the cheapest chain per category
* It includes at least 3 actionable insights
* The tool is deployed and publicly accessible

## 📊 Phase 2 — Dataset Creation

Once the scope was clearly defined, the next step was to build a **structured and reliable dataset**.

### 🧾 Data Collection Approach

Data was collected manually from:

* official supermarket websites
* publicly available product listings

Each product was recorded following a **standardized structure**, including:

* product_id
* product_name
* package_size
* brand
* private_label (yes/no)
* category
* chain
* price (€)
* unit (kg, L, unit)
* price_per_unit
* date

### 🧠 Data Consistency & Methodology

To ensure data quality and analytical rigor, I standardized product definitions, normalized all prices per unit, handled packaging variability through approximate categories, and validated consistency across chains before analysis.

Key methodological decisions included:

* Using **functional equivalence** when exact matches were unavailable
* Treating missing products as **missing values**, not forcing substitutions
* Normalizing all prices using **€/kg, €/L, or €/unit**
* Maintaining consistent product definitions across all chains

### 📦 Dataset Structure

The dataset was designed to balance:

* **comparability** (same product logic across chains)
* **realism** (reflecting actual market availability)

The final dataset includes 27 SKUs across 5 supermarket chains, resulting in a structured dataset ready for analysis.

This phase demonstrates the ability to translate a business problem into a structured analytical framework, ensuring that data collection supports meaningful and defensible insights.

### 🧭 Next Step

With the dataset completed, the project moves into: **Phase 3 — Data Analysis**, where pricing patterns, competitive positioning, and strategic insights will be extracted.

