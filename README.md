# 🛒 Supermarket Pricing Dashboard

**End-to-end competitive pricing analysis of 5 Spanish supermarket chains**, combining structured data collection, analytical rigor, and business-oriented insights.

## 🧠 Methodology (Key Decisions)

This project focuses on ensuring **comparability across heterogeneous supermarket assortments**, where identical products are not always available.

The following principles guided dataset design:

* **Functional equivalence over exact matching**
  When identical SKUs were not available, products were selected based on their functional role (e.g. mainstream chocolate cereals), ensuring category-level comparability.

* **Unit normalization for fair comparison**
  All prices were standardized using price per unit (€/kg, €/L, €/unit) to account for differences in packaging size.

* **Approximate size grouping**
  Products with varying formats (e.g. 375g vs 625g) were grouped into approximate size tiers (e.g. ~500g).

* **Segmentation when product characteristics affect price**
  For products such as eggs, where size impacts pricing, categories were split (e.g. M vs L).

* **Segment consistency over packaging consistency**
  When trade-offs arose, priority was given to comparing equivalent product segments (e.g. private label vs private label).

* **Explicit handling of missing products**
  Unavailable products were excluded from the dataset to avoid distortions in aggregation.

* **Consumer-relevant metrics where applicable**
  Cost per use (€/wash or €/cycle) was introduced for cleaning products where relevant.

---

## 📌 Project Overview

### 🎯 Objective

Analyze pricing strategies and competitive positioning across major supermarket chains, combining data analysis with business-oriented insights.

### 🏪 Competitive Set

* Mercadona
* Consum
* Carrefour
* Dia
* Alcampo

> Consum was included instead of Lidl due to data accessibility constraints and its strong regional presence in the Valencian market.

### 🧺 Product Categories

* Dairy
* Breakfast
* Cleaning
* Fresh Produce
* Snacks

A consistent basket of **~30 core SKUs** was defined across categories.

---

## 📊 Phase 1 — Scope Definition

The first phase focused on designing a **clear and analytically robust framework** before data collection.

### 🧠 Product Selection Logic

Exact product matches were not always available across chains. Therefore:

> Products were selected based on **functional equivalence**, ensuring comparability at the category level rather than exact SKU level.

### ⚖️ Handling Packaging Variability

Products differed in size and format (e.g. 375g vs 625g, 4x125g vs 8x125g).

To ensure comparability:

* Products were grouped into **approximate size categories**
* Prices were normalized using **€/kg, €/L, or €/unit**

### 🥚 Controlling for Product Characteristics

For products where size affects pricing:

* Eggs were segmented by size (M vs L)
* Closest equivalents were selected when standard formats were unavailable

### 📌 Handling Missing Products

Unavailable products were excluded from the dataset instead of being represented as empty (NaN) rows. This ensures accurate aggregation and avoids distortions.

### 📌 Consumer-Relevant Metrics

For cleaning products:

* Laundry liquid and dishwasher gel → **cost per use**
* Capsules and tablets → **price per unit = cost per use**

Other categories use standard unit pricing.

### 📌 Brand Benchmarks

Selected national brands were included to complement private label analysis:

* Kellogg's (cereals)
* Danone (yogurt)
* Fairy (dishwasher tablets)
* Lay's (salted crisps)

When unavailable in a chain, observations were treated as missing.

### 📌 Data Collection Methodology

| Chain     | Source           | Date  | Method            |
| --------- | ---------------- | ----- | ----------------- |
| Mercadona | Official website | 19/04 | Manual extraction |
| Consum    | Official website | 19/04 | Manual extraction |
| Carrefour | Official website | 19/04 | Manual extraction |
| Dia       | Official website | 19/04 | Manual extraction |
| Alcampo   | Official website | 19/04 | Manual extraction |

All prices were collected on the same day to ensure **temporal consistency**.

---

## 📊 Phase 2 — Dataset Creation

### 🧾 Data Structure

Each observation includes:

* product_id
* product_name
* package_size
* brand
* private_label
* category
* chain
* price (€)
* unit (kg, L, unit)
* price_per_unit
* date

### 🧠 Data Quality & Consistency

To ensure analytical rigor:

* Product definitions were standardized
* Packaging variability was controlled through approximation
* Prices were normalized across all observations
* Missing values were handled explicitly

### 📦 Dataset Summary

* **~30 core SKUs**
* **5 supermarket chains**
* Structured for consistent cross-chain comparison

---

## 📊 Key Performance Indicators (KPIs)

### Price KPIs

* Average price by chain and category
* Price index (market average = 100)
* Price per unit

### Competitive Positioning

* Cheapest chain per category
* Most expensive chain per category
* Price gap (%)

### Brand Structure

* Private label share
* Private label vs branded price gap

---

## ⚙️ Constraints

* Manual data collection (no scraping)
* Single price snapshot (second planned)
* No store-level variation
* Focus on Valencia region

---

## 🧭 Next Step

➡️ **Phase 3 — Data Analysis**

Focus:

* Pricing patterns
* Competitive positioning
* Strategic insights
