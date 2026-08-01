from app import create_app, db
from app.models import User, Product, Bid

def init_db():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Create all tables with new schema
        db.create_all()
        print("Database initialized successfully!")

if __name__ == "__main__":
    init_db() 