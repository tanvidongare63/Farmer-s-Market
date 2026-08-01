from app import create_app, db
from app.models import User, Product, Bid
from tabulate import tabulate

app = create_app()

def view_database():
    with app.app_context():
        # View Users
        users = User.query.all()
        print("\n=== USERS ===")
        user_data = []
        for user in users:
            user_data.append([
                user.id,
                user.name,
                user.email,
                user.user_type
            ])
        print(tabulate(user_data, headers=['ID', 'Name', 'Email', 'Type'], tablefmt='grid'))
        
        # View Products
        products = Product.query.all()
        print("\n=== PRODUCTS ===")
        product_data = []
        for product in products:
            product_data.append([
                product.id,
                product.name,
                product.category,
                f"{product.quantity} {product.unit}",
                f"₹{product.base_price}",
                product.owner.name
            ])
        print(tabulate(product_data, headers=['ID', 'Name', 'Category', 'Quantity', 'Price', 'Owner'], tablefmt='grid'))
        
        # View Bids
        bids = Bid.query.all()
        print("\n=== BIDS ===")
        bid_data = []
        for bid in bids:
            bid_data.append([
                bid.id,
                bid.product.name,
                bid.bidder.name,
                f"₹{bid.amount}",
                bid.status,
                bid.date.strftime('%Y-%m-%d %H:%M')
            ])
        print(tabulate(bid_data, headers=['ID', 'Product', 'Bidder', 'Amount', 'Status', 'Date'], tablefmt='grid'))

if __name__ == '__main__':
    view_database() 