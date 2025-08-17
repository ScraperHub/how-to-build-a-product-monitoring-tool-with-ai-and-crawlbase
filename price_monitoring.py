from database import query_products;
from perplexity_ai import analyze_data;
import json

def monitor_price():
    try:
        products = query_products()
        analysis_result = analyze_data(products)

        print("=" * 80)
        print("PRODUCT MONITORING ANALYSIS RESULTS")
        print("=" * 80)
        print()

        print(json.dumps(analysis_result, indent=2, ensure_ascii=False))
        
        print()
        print("=" * 80)
        print("END OF ANALYSIS RESULTS")
        print("=" * 80)

    except Exception as e:
        print(f"Error monitoring price: {str(e)}")

if __name__ == "__main__":
    # from crawling import crawl_amazon_product_details
    # from database import add_products_to_db

    # product_data = crawl_amazon_product_details("https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL/ref=sr_1_1")
    # add_products_to_db(product_data)
    monitor_price()
