// Shopping Cart Utilities - Global Cart Management
class ShoppingCart {
    constructor() {
        this.cartKey = 'cultivar_cart';
        this.init();
    }

    init() {
        this.loadCart();
        this.bindEvents();
        this.updateNavigation();
    }

    // Event binding for dynamic elements
    bindEvents() {
        // Event delegation for cart buttons
        document.addEventListener('click', (e) => {
            const button = e.target.closest('.add-to-cart, .buy-seed, .add-gear, .remove-item, .quantity-btn');
            if (!button) return;

            e.preventDefault();

            if (button.classList.contains('add-to-cart') ||
                button.classList.contains('buy-seed') ||
                button.classList.contains('add-gear')) {
                this.handleAddToCart(button);
            } else if (button.classList.contains('remove-item')) {
                this.handleRemoveItem(button);
            } else if (button.classList.contains('quantity-btn')) {
                this.handleQuantityUpdate(button);
            }
        });

        // Clear cart event
        document.addEventListener('click', (e) => {
            if (e.target.id === 'clear-cart') {
                if (confirm('Are you sure you want to clear your cart?')) {
                    this.clearCart();
                }
            }
        });

        // Checkout event
        document.addEventListener('click', (e) => {
            if (e.target.id === 'checkout-btn') {
                this.checkout();
            }
        });
    }

    // Product data extraction
    extractProductData(button) {
        const card = button.closest('.card');

        if (!card) return null;

        const productId = button.getAttribute('data-product-id') || button.getAttribute('data-seed-id') || button.getAttribute('data-gear-id') || 'unknown';

        return {
            id: productId,
            name: card.querySelector('.card-title')?.textContent?.trim() || 'Unknown Product',
            category: card.querySelector('.badge')?.textContent?.trim() || 'General',
            price: parseFloat(card.querySelector('.text-success')?.textContent?.replace('$', '') || '0'),
            image: card.querySelector('img')?.src || '/static/images/product-placeholder.jpg',
            unit_price: parseFloat(card.querySelector('.text-success')?.textContent?.replace('$', '') || '0')
        };
    }

    // Add to cart handlers
    handleAddToCart(button) {
        const product = this.extractProductData(button);
        if (product) {
            this.addItem(product);
            this.showToast(`${product.name} added to cart!`);
        }
    }

    handleRemoveItem(button) {
        const cartItem = button.closest('.cart-item');
        if (cartItem) {
            const productId = cartItem.dataset.id;
            this.removeItem(productId);
            this.showToast('Item removed from cart!');
        }
    }

    handleQuantityUpdate(button) {
        const cartItem = button.closest('.cart-item');
        if (!cartItem) return;

        const productId = cartItem.dataset.id;
        const action = button.dataset.action;

        this.updateQuantity(productId, action);
    }

    // Cart operations
    getCart() {
        try {
            const cartData = localStorage.getItem(this.cartKey);
            return cartData ? JSON.parse(cartData) : {};
        } catch (error) {
            console.error('Error loading cart:', error);
            return {};
        }
    }

    saveCart(cart) {
        try {
            localStorage.setItem(this.cartKey, JSON.stringify(cart));
        } catch (error) {
            console.error('Error saving cart:', error);
        }
    }

    loadCart() {
        try {
            this.cart = this.getCart();
        } catch (error) {
            console.error('Error loading cart:', error);
            this.cart = {};
        }
    }

    addItem(product) {
        if (!product) return;

        if (this.cart[product.id]) {
            this.cart[product.id].quantity += 1;
        } else {
            // Initialize new cart item
            this.cart[product.id] = {
                ...product,
                quantity: 1,
                total_price: product.unit_price,
                added_at: new Date().toISOString()
            };
        }

        this.cart[product.id].total_price = this.cart[product.id].quantity * this.cart[product.id].unit_price;
        this.saveCart(this.cart);

        // Update navigation counter
        this.updateNavigation();

        // Dispatch custom event for other scripts
        window.dispatchEvent(new CustomEvent('cartUpdate', { detail: this.cart }));
    }

    removeItem(productId) {
        delete this.cart[productId];
        this.saveCart(this.cart);

        // Update navigation counter
        this.updateNavigation();

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('cartUpdate', { detail: this.cart }));
    }

    updateQuantity(productId, action) {
        if (!this.cart[productId]) return;

        if (action === 'increase') {
            this.cart[productId].quantity += 1;
        } else if (action === 'decrease') {
            this.cart[productId].quantity = Math.max(0, this.cart[productId].quantity - 1);
            if (this.cart[productId].quantity === 0) {
                this.removeItem(productId);
                return;
            }
        }

        this.cart[productId].total_price = this.cart[productId].quantity * this.cart[productId].unit_price;
        this.saveCart(this.cart);

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('cartUpdate', { detail: this.cart }));
    }

    clearCart() {
        this.cart = {};
        this.saveCart(this.cart);

        // Update navigation counter
        this.updateNavigation();

        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('cartUpdate', { detail: this.cart }));

        this.showToast('Cart cleared!');
    }

    getItemCount() {
        if (!this.cart) return 0;
        return Object.values(this.cart).reduce((total, item) => total + (item.quantity || 0), 0);
    }

    getTotalPrice() {
        if (!this.cart) return 0;
        return Object.values(this.cart).reduce((total, item) => total + (item.total_price || 0), 0);
    }

    // Navigation and UI updates
    updateNavigation() {
        const itemCount = this.getItemCount();
        const cartCounter = document.getElementById('cart-counter');

        if (cartCounter) {
            cartCounter.textContent = itemCount;
            cartCounter.style.display = itemCount > 0 ? 'inline-block' : 'none';
        }
    }

    // Toast notifications
    showToast(message) {
        // Remove existing toasts
        document.querySelectorAll('.cart-toast').forEach(toast => toast.remove());

        const toast = document.createElement('div');
        toast.className = 'toast align-items-center text-white bg-success border-0 position-fixed cart-toast';
        toast.style.zIndex = '9999';
        toast.style.right = '20px';
        toast.style.top = '80px';
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas fa-shopping-cart me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        setTimeout(() => {
            if (document.body.contains(toast)) {
                document.body.removeChild(toast);
            }
        }, 4000);
    }

    // Checkout functionality
    checkout() {
        if (Object.keys(this.cart).length === 0) {
            this.showToast('Your cart is empty!');
            return;
        }

        // Create checkout summary
        const summary = Object.values(this.cart).map(item =>
            `${item.name} x${item.quantity} - $${item.total_price.toFixed(2)}`
        ).join('\n');

        const total = this.getTotalPrice();

        alert(`🛒 Checkout Summary:\n\n${summary}\n\n💰 Total: $${total.toFixed(2)}\n\n🚀 Thank you for your order! This is a demo shopping cart. In a real application, you would be redirected to a payment processor.`);
    }
}

// Initialize cart on page load
document.addEventListener('DOMContentLoaded', function() {
    // Create global cart instance
    window.cart = new ShoppingCart();
});