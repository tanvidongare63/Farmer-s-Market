// Handle product filtering
document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const params = new URLSearchParams();
            
            for (let pair of formData.entries()) {
                if (pair[1]) {
                    params.append(pair[0], pair[1]);
                }
            }
            
            fetch(`/api/products?${params.toString()}`)
                .then(response => response.json())
                .then(products => updateProductList(products))
                .catch(error => console.error('Error:', error));
        });
    }
});

// Update product list with filtered results
function updateProductList(products) {
    const container = document.getElementById('products-container');
    if (!container) return;

    container.innerHTML = '';
    
    products.forEach(product => {
        const productHtml = `
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card h-100">
                    ${product.image_path 
                        ? `<img src="/static/${product.image_path}" class="card-img-top" alt="${product.name}">`
                        : `<div class="card-img-top bg-light text-center py-5">
                            <i class="fas fa-image fa-3x text-muted"></i>
                           </div>`
                    }
                    <div class="card-body">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text">${product.description}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-success">${product.category}</span>
                            <span>${product.quantity} ${product.unit}</span>
                        </div>
                        <p class="card-text mt-2">
                            <small class="text-muted">Base Price: ₹${product.base_price.toFixed(2)}</small>
                        </p>
                    </div>
                    <div class="card-footer bg-white border-top-0">
                        <a href="/product/${product.id}" class="btn btn-outline-success w-100">View Details</a>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += productHtml;
    });
}

// Handle bid form submission
const bidForm = document.getElementById('bid-form');
if (bidForm) {
    bidForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        const productId = window.location.pathname.split('/').pop();
        
        fetch(`/product/${productId}/bid`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                // Instead of adding the bid directly, reload the page to show updated bid list
                window.location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    });
}

// Handle product deletion
const deleteButton = document.getElementById('confirmDelete');
if (deleteButton) {
    deleteButton.addEventListener('click', function() {
        const productId = window.location.pathname.split('/').pop();
        fetch(`/product/${productId}/delete`, {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/dashboard';
            } else {
                alert('Failed to delete product');
            }
        })
        .catch(error => console.error('Error:', error));
    });
}

// Image preview for product upload
const imageInput = document.getElementById('image');
if (imageInput) {
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            if (file.size > 16 * 1024 * 1024) {
                alert('File size must be less than 16MB');
                this.value = '';
                return;
            }

            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.createElement('img');
                preview.src = e.target.result;
                preview.className = 'img-fluid mt-2 rounded';
                const container = imageInput.parentElement;
                const existingPreview = container.querySelector('img');
                if (existingPreview) {
                    container.removeChild(existingPreview);
                }
                container.appendChild(preview);
            }
            reader.readAsDataURL(file);
        }
    });
} 