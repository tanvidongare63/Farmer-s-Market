from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Product, Bid, User
from . import db
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy import desc

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/img/products'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/api/latest-products')
def latest_products():
    products = Product.query.order_by(desc(Product.date_added)).limit(6).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'category': p.category,
        'quantity': p.quantity,
        'unit': p.unit,
        'base_price': p.base_price,
        'image_path': p.image_path
    } for p in products])

@views.route('/api/products')
def filter_products():
    category = request.args.get('category')
    sort_by = request.args.get('sort')
    search = request.args.get('search')
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(Product.name.ilike(search_term))
    
    if sort_by == 'price_low':
        query = query.order_by(Product.base_price)
    elif sort_by == 'price_high':
        query = query.order_by(desc(Product.base_price))
    else:  # newest
        query = query.order_by(desc(Product.date_added))
    
    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'category': p.category,
        'quantity': p.quantity,
        'unit': p.unit,
        'base_price': p.base_price,
        'image_path': p.image_path
    } for p in products])

@views.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'farmer':
        products = Product.query.filter_by(user_id=current_user.id).all()
    else:
        products = Product.query.all()
    return render_template("dashboard.html", user=current_user, products=products)

@views.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if current_user.user_type != 'farmer':
        flash('Only farmers can add products!', category='error')
        return redirect(url_for('views.dashboard'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        quantity = float(request.form.get('quantity'))
        unit = request.form.get('unit')
        base_price = float(request.form.get('base_price'))
        image = request.files.get('image')

        if not all([name, description, category, quantity, unit, base_price]):
            flash('Please fill all fields!', category='error')
        else:
            image_path = None
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = f'img/products/{filename}'
                image.save(os.path.join(UPLOAD_FOLDER, filename))

            new_product = Product(
                name=name,
                description=description,
                category=category,
                quantity=quantity,
                unit=unit,
                base_price=base_price,
                image_path=image_path,
                user_id=current_user.id
            )
            db.session.add(new_product)
            db.session.commit()
            flash('Product added!', category='success')
            return redirect(url_for('views.dashboard'))

    return render_template("new_product.html", user=current_user)

@views.route('/product/<int:id>')
@login_required
def view_product(id):
    product = Product.query.get_or_404(id)
    # Get unique bids ordered by amount in descending order
    bids = Bid.query.filter_by(product_id=id).distinct(Bid.amount).order_by(desc(Bid.amount)).all()
    return render_template("product.html", user=current_user, product=product, bids=bids)

@views.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if product.user_id != current_user.id:
        flash('You can only edit your own products!', category='error')
        return redirect(url_for('views.dashboard'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.category = request.form.get('category')
        product.quantity = float(request.form.get('quantity'))
        product.unit = request.form.get('unit')
        product.base_price = float(request.form.get('base_price'))
        
        image = request.files.get('image')
        if image and allowed_file(image.filename):
            # Delete old image if exists
            if product.image_path:
                try:
                    os.remove(os.path.join('app/static', product.image_path))
                except:
                    pass
            
            filename = secure_filename(image.filename)
            image_path = f'img/products/{filename}'
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            product.image_path = image_path
        
        db.session.commit()
        flash('Product updated successfully!', category='success')
        return redirect(url_for('views.view_product', id=id))
    
    return render_template("edit_product.html", user=current_user, product=product)

@views.route('/product/<int:id>/bid', methods=['POST'])
@login_required
def place_bid(id):
    if current_user.user_type != 'merchant':
        return jsonify({'error': 'Only merchants can place bids'}), 403

    product = Product.query.get_or_404(id)
    amount = float(request.form.get('amount'))

    if amount <= product.base_price:
        return jsonify({'error': 'Bid must be higher than base price'}), 400

    # Check if a bid with the same amount from the same user already exists
    existing_bid = Bid.query.filter_by(
        product_id=id,
        user_id=current_user.id,
        amount=amount
    ).first()

    if existing_bid:
        return jsonify({'error': 'You have already placed a bid with this amount'}), 400

    bid = Bid(
        amount=amount,
        product_id=id,
        user_id=current_user.id
    )
    db.session.add(bid)
    db.session.commit()

    return jsonify({
        'message': 'Bid placed successfully',
        'amount': amount,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'bidder_name': current_user.name
    })

@views.route('/product/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    if product.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    if product.image_path:
        try:
            os.remove(os.path.join('app/static', product.image_path))
        except:
            pass
            
    db.session.delete(product)
    db.session.commit()
    
    return '', 204

@views.route('/about')
def about():
    return render_template("about.html", user=current_user)

@views.route('/contact')
def contact():
    return render_template("contact.html", user=current_user)

@views.route('/admin/users')
@login_required
def admin_users():
    # Check if user is admin (you might want to add an admin role to your User model)
    if current_user.email != 'admin@example.com':  # Replace with your admin check
        flash('Access denied. Admin only.', category='error')
        return redirect(url_for('views.home'))

    # Get all users with their products and bids
    users = User.query.all()
    return render_template("admin_users.html", user=current_user, users=users)

@views.route('/admin/cleanup-duplicate-bids')
@login_required
def cleanup_duplicate_bids():
    if current_user.email != 'admin@example.com':
        flash('Access denied. Admin only.', category='error')
        return redirect(url_for('views.home'))
    
    # Get all products
    products = Product.query.all()
    duplicates_removed = 0
    
    for product in products:
        # Get all bids for this product
        bids = Bid.query.filter_by(product_id=product.id).order_by(Bid.date).all()
        seen_bids = set()
        
        for bid in bids:
            # Create a unique key for each bid based on user and amount
            bid_key = (bid.user_id, bid.amount)
            
            if bid_key in seen_bids:
                # This is a duplicate bid, remove it
                db.session.delete(bid)
                duplicates_removed += 1
            else:
                seen_bids.add(bid_key)
    
    if duplicates_removed > 0:
        db.session.commit()
        flash(f'Cleaned up {duplicates_removed} duplicate bids', category='success')
    else:
        flash('No duplicate bids found', category='info')
    
    return redirect(url_for('views.admin_users')) 