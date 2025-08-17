import sqlite3
import os
from datetime import datetime

def setup_database():
    db_path = 'product_monitoring.db'
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            currency TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    return conn

def add_products_to_db(data):
    conn = setup_database()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (url, name, price, currency)
        VALUES (?, ?, ?, ?)
    ''', (data["url"], data["name"], data["price"], data["currency"]))

    product_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return product_id

def query_products(limit=None, url=None, order_by='timestamp DESC'):
    conn = setup_database()
    cursor = conn.cursor()
    
    query = "SELECT id, url, name, price, currency, timestamp FROM products"
    params = []
    
    if url:
        query += " WHERE url = ?"
        params.append(url)
    
    query += f" ORDER BY {order_by}"
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    
    products_json = []
    for row in results:
        product_dict = {
            "id": row[0],
            "url": row[1],
            "name": row[2],
            "price": row[3],
            "currency": row[4],
            "timestamp": row[5]
        }
        products_json.append(product_dict)
    
    conn.close()
    return products_json
    conn = setup_database()
    cursor = conn.cursor()
    
    # Check if product exists before deleting
    cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        conn.close()
        return False
    
    # Delete the product
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    
    return True

def update_product_timestamp(product_id, timestamp):
    conn = setup_database()
    cursor = conn.cursor()
    
    # Check if product exists before updating
    cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        conn.close()
        return False
    
    # Update the product price and currency
    cursor.execute("UPDATE products SET timestamp = ? WHERE id = ?", 
                   (timestamp, product_id))
    conn.commit()
    conn.close()
    
    return True
