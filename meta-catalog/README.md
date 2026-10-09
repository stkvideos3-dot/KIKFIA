# KIKFIA Meta (Facebook & Instagram) product catalog

Files to upload in Meta Commerce Manager → Catalog → Data sources → Add items → Data feed → Upload once:

- `kikfia-meta-catalog.xlsx` (easiest to edit), or `kikfia-meta-catalog.csv` / `.tsv`

Before uploading, fill in the **price** column (yellow in the Excel file) with your starting price, for example `24900.00 USD`. Meta rejects rows without a price.

Each row is one product. Images are 1080×1080 and hosted publicly from this repository (`images/`), so Meta can download them. To rebuild after changing products: `python3 build_feed.py <commit-sha>`.
