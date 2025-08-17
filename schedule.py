from crawling import crawl_amazon_product_details
from database import add_products_to_db
from price_monitoring import monitor_price
import schedule
import time

def job():
    product_data = crawl_amazon_product_details("https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL/ref=sr_1_1")
    add_products_to_db(product_data)
    monitor_price()

# Run every day at 10:30 AM
schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
