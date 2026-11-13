# Beauty Product Growth & Recommendation Analytics

## About the Project

This project focuses on analyzing a beauty and cosmetics e-commerce platform (similar to Nykaa) to understand customer behaviour, product performance and sales trends.

I used SQL, Python and Power BI to explore the dataset, identify patterns and understand areas where the shopping experience could be improved.

Along with data analysis, I also worked on identifying a product-related problem and suggesting a possible feature to address it.

The project covers the complete process from understanding the problem and analyzing data to suggesting improvements and defining how their impact can be measured.

**Start here:** [Case Study](docs/case_study.md)

## Key Finding

One of the main findings was that subcategories with 20 or more similar products, such as Moisturizer, Face Serum, Foundation, Lipstick, Shampoo and Sunscreen, had around 11% view-to-purchase conversion.

In comparison, subcategories with fewer and more differentiated products had around 20% conversion.

This showed that customers were browsing and adding products to their wishlist but were not converting into purchases at the same rate.

Based on this finding, I proposed a **Compare Products** feature to help customers compare similar products before making a purchase.

## Project Structure

```text
beauty-product-analytics/
│
├── README.md
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── user_events.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── derived/
│
├── scripts/
│   ├── 01_generate_data.py
│   └── 02_analysis.py
│
├── charts/
│
├── sql/
│   ├── 01_schema.sql
│   └── 02_analysis_queries.sql
│
├── powerbi/
│   └── dashboard_design.md
│
└── docs/
    ├── case_study.md
    ├── PRD.md
    ├── analysis_output.txt
    ├── interview_qna.md
    └── resume_description.md
```

## Analysis Performed

The analysis covers the following areas:

1. **Customer Behaviour:** Customer segments, repeat purchases, high-value customers and browsing patterns.
2. **Product Performance:** Product and subcategory performance, views, purchases and conversion rates.
3. **Pricing and Discounts:** Relationship between discounts, product prices and purchase behaviour.
4. **Reviews and Ratings:** How product ratings and review counts relate to customer engagement and purchases.
5. **Product Discovery:** Analysis of the shopping funnel to identify where customers drop off before purchasing.

## Product Recommendation

Based on the analysis, I proposed a **Compare Products** feature.

The idea is to allow customers to compare similar products based on price, ratings, ingredients and other product details.

The proposed feature also includes an A/B testing plan to measure whether it improves product discovery and purchase conversion before a wider rollout.

## Dataset Information

The project uses a synthetic beauty e-commerce dataset containing:

| Dataset | Records |
|---|---:|
| Customers | 6,000 |
| Products | 330 |
| User Events | Around 200,000 |
| Orders | Around 16,250 |
| Order Items | Around 16,250 |

The dataset includes customer details, product information, browsing activity, orders and purchase records.

## Tools & Technologies

- **Python:** Pandas, NumPy and Matplotlib
- **SQL:** MySQL, joins, CTEs and window functions
- **Power BI:** Data visualization and dashboard development
- **Excel/CSV:** Dataset handling

## How to Run

**Python Analysis**

```bash
cd scripts
python 01_generate_data.py
python 02_analysis.py
```

**SQL Analysis**

1. Run `sql/01_schema.sql` to create the database tables.
2. Load the CSV files into the respective tables.
3. Run `sql/02_analysis_queries.sql`.

**Power BI**

Import the dataset into Power BI and follow the dashboard design and measures documented in the `powerbi/` folder.

## Project Documentation

- [Case Study](docs/case_study.md)
- [Product Requirements Document](docs/PRD.md)
- [Analysis Output](docs/analysis_output.txt)
- [Interview Questions & Answers](docs/interview_qna.md)
- [Resume Description](docs/resume_description.md)

## Limitations

The project uses synthetic data with predefined patterns for analysis. The findings are useful for understanding customer behaviour and exploring product-related improvements, but they should not be treated as actual results from Nykaa or any other real e-commerce platform.
