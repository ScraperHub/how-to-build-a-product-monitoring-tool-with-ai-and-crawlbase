from database import add_products_to_db;
from database import update_product_timestamp;

product_json = {
    "url": "https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL",
	"name": "Apple iPhone 16, US Version, 128GB, Black - Unlocked (Renewed)",
	"price": 600.82,
	"currency": "$"
}
product_id = add_products_to_db(product_json)
update_product_timestamp(product_id, "2025-07-17 17:49:44")

product_json = {
    "url": "https://www.amazon.com/Apple-iPhone-16-Version-128GB/dp/B0DHJH2GZL",
	"name": "Apple iPhone 16, US Version, 128GB, Black - Unlocked (Renewed)",
	"price": 700.82,
	"currency": "$"
}
product_id = add_products_to_db(product_json)
update_product_timestamp(product_id, "2025-08-17 17:49:44")

