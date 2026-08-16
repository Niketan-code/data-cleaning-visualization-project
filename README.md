# Data Cleaning & Visualization Project

## Project Title
**Retail Sales Data Cleaning, Analysis & Visualization**

## Objective
Clean a raw retail-sales dataset, handle missing values, duplicates and outliers, and create visualizations that communicate useful business insights.

## Dataset
The included `data/raw_retail_sales.csv` is a **practice dataset created for this assignment**. It intentionally contains common data-quality problems so the cleaning workflow can be demonstrated honestly.

## Data Problems Included
- Missing customer, region, quantity and price values.
- Duplicate order records.
- Inconsistent capitalization in text fields.
- Negative/invalid quantity and price values.
- Extreme sales values treated as outliers.

## Cleaning Process
1. Load the raw CSV with Pandas.
2. Inspect shape, data types, missing values and duplicates.
3. Standardize text columns.
4. Convert date and numeric columns to appropriate types.
5. Remove duplicate orders.
6. Replace invalid numeric values with missing values.
7. Fill missing categorical values with `Unknown`.
8. Fill numeric missing values using median values.
9. Recalculate `Total_Sales` from quantity × unit price.
10. Detect and cap extreme sales values using the IQR rule.
11. Save the cleaned dataset.

## Visualizations
The `visuals` folder contains:
- Monthly sales trend
- Sales by category
- Sales by product
- Sales by region
- Sales distribution
- Dashboard-style summary

## Key Findings
- Sales performance varies across months, showing periods of stronger and weaker demand.
- The product/category charts identify the largest contributors to revenue.
- Regional comparison shows where sales are concentrated.
- The distribution chart highlights unusually large orders before/after outlier treatment.

## How to Run
```bash
pip install pandas matplotlib seaborn
python analysis.py
```

## Submission Files
- `analysis.py` – complete Python workflow
- `data/raw_retail_sales.csv` – raw dataset
- `data/cleaned_retail_sales.csv` – cleaned dataset
- `visuals/` – charts and dashboard
- `report.pdf` – project report

## Tools Used
Python, Pandas, Matplotlib, Seaborn.
