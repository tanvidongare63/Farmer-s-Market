from app import create_app, db
from app.models import User

def migrate():
    app = create_app()
    with app.app_context():
        # Add phone column if it doesn't exist
        with db.engine.connect() as conn:
            conn.execute('ALTER TABLE user ADD COLUMN IF NOT EXISTS phone VARCHAR(20)')
            
        # Update existing users with a placeholder phone number if they don't have one
        users = User.query.filter_by(phone=None).all()
        for user in users:
            user.phone = "0000000000"  # Placeholder phone number
        db.session.commit()

if __name__ == "__main__":
    migrate() 