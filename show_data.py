import sqlite3
from datetime import datetime

def save_data_to_file():
    # Open a file to write the data
    with open('database_data.txt', 'w', encoding='utf-8') as file:
        # Connect to the database
        conn = sqlite3.connect('app/farmers_market.db')
        cursor = conn.cursor()
        
        # Write Users data
        file.write("\n=== USERS ===\n")
        try:
            cursor.execute("SELECT * FROM user")
            users = cursor.fetchall()
            for user in users:
                file.write(f"\nUser ID: {user[0]}\n")
                file.write(f"Name: {user[3]}\n")
                file.write(f"Email: {user[1]}\n")
                file.write(f"Type: {user[4]}\n")
                file.write("-" * 30 + "\n")
        except sqlite3.OperationalError as e:
            file.write(f"Could not fetch users: {e}\n")
        
        # Write Products data
        file.write("\n=== PRODUCTS ===\n")
        try:
            cursor.execute("SELECT * FROM product")
            products = cursor.fetchall()
            for product in products:
                file.write(f"\nProduct ID: {product[0]}\n")
                file.write(f"Name: {product[1]}\n")
                file.write(f"Category: {product[3]}\n")
                file.write(f"Quantity: {product[4]} {product[5]}\n")
                file.write(f"Base Price: ₹{product[6]}\n")
                file.write("-" * 30 + "\n")
        except sqlite3.OperationalError as e:
            file.write(f"Could not fetch products: {e}\n")
        
        # Write Bids data
        file.write("\n=== BIDS ===\n")
        try:
            cursor.execute("SELECT * FROM bid")
            bids = cursor.fetchall()
            for bid in bids:
                file.write(f"\nBid ID: {bid[0]}\n")
                file.write(f"Amount: ₹{bid[1]}\n")
                file.write(f"Status: {bid[3]}\n")
                file.write("-" * 30 + "\n")
        except sqlite3.OperationalError as e:
            file.write(f"Could not fetch bids: {e}\n")
        
        conn.close()
        
        print("Data has been saved to 'database_data.txt'")

if __name__ == '__main__':
    save_data_to_file() 