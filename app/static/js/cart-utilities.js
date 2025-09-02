((function() {
    'use strict';

    // Toast notification system
    function showToast(message, type = 'success') {
        // Create toast container if it doesn't exist
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
        }

        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');

        const toastContent = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        `;

        toast.innerHTML = toastContent;
        container.appendChild(toast);

        // Show toast
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        // Remove from DOM after hiding
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }

    // ShoppingCart class
    class ShoppingCart {
        constructor() {
            this.storageKey = 'shopping_cart';
            this.items = this.loadCart();
            this.init();
        }

        init() {
            this.bindEvents();
            this.updateUI();
            console.log('Cart utilities initialized', this.items);
        }

        loadCart() {
            try {
                const cart = localStorage.getItem(this.storageKey);
                return cart ? JSON.parse(cart) : [];
            } catch (error) {
                console.error('Error loading cart:', error);
                return [];
            }
        }

        saveCart() {
            try {
                localStorage.setItem(this.storageKey, JSON.stringify(this.items));
                console.log('Cart saved:', this.items);
            } catch (error) {
                console.error('Error saving cart:', error);
            }
        }

        // Add item to cart or increase quantity if it already exists
        addItem(productId, name, price, quantity = 1) {
            const existingItem = this.items.find(item => item.productId === productId);

            if (existingItem) {
                existingItem.quantity += quantity;
            } else {
                this.items.push({
                    productId,
                    name,
                    price: parseFloat(price),
                    quantity
                });
            }

            this.saveCart();
            this.updateUI();
            showToast(`Added ${name} to cart`, 'success');
            return this.items;
        }

        // Remove item from cart
        removeItem(productId) {
            const itemIndex = this.items.findIndex(item => item.productId === productId);
            if (itemIndex > -1) {
                const item = this.items[itemIndex];
                this.items.splice(itemIndex, 1);
                this.saveCart();
                this.updateUI();
                showToast(`Removed ${item.name} from cart`, 'warning');
                return true;
            }
            return false;
        }

        // Update item quantity
        updateQuantity(productId, quantity) {
            const item = this.items.find(item => item.productId === productId);
            if (item) {
                item.quantity = Math.max(0, parseInt(quantity));
                if (item.quantity === 0) {
                    this.removeItem(productId);
                } else {
                    this.saveCart();
                    this.updateUI();
                }
                return true;
            }
            return false;
        }

        // Get total number of items
        getTotalItems() {
            return this.items.reduce((total, item) => total + item.quantity, 0);
        }

        // Get total price
        getTotalPrice() {
            return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
        }

        // Clear entire cart
        clearCart() {
            this.items = [];
            this.saveCart();
            this.updateUI();
            showToast('Cart cleared', 'info');
        }

        // Get all items
        getItems() {
            return this.items;
        }

        // Check if item exists in cart
        hasItem(productId) {
            return this.items.some(item => item.productId === productId);
        }

        // Get item by product ID
        getItem(productId) {
            return this.items.find(item => item.productId === productId);
        }

        // Update UI elements
        updateUI() {
            this.updateCartCounter();
            console.log('Updated UI - Total items:', this.getTotalItems(), 'Total price:', this.getTotalPrice());
        }

        // Update cart counter badge
        updateCartCounter() {
            const counter = document.getElementById('cart-counter');
            if (counter) {
                const totalItems = this.getTotalItems();
                if (totalItems > 0) {
                    counter.textContent = totalItems;
                    counter.classList.remove('d-none');
                } else {
                    counter.classList.add('d-none');
                }
            }
        }

        // Bind event listeners using event delegation
        bindEvents() {
            // Delegate click events for add-to-cart buttons
            document.addEventListener('click', (event) => {
                const target = event.target;

                // Check if clicked element is an "Add to Cart" button
                if (target.classList.contains('add-to-cart') ||
                    (target.closest('.add-to-cart') && target.tagName !== 'BUTTON')) {

                    const button = target.classList.contains('add-to-cart') ?
                                  target : target.closest('.add-to-cart');

                    if (button) {
                        event.preventDefault();
                        this.handleAddToCart(button);
                    }
                }
            });
        }

        // Handle add to cart button click
        handleAddToCart(button) {
            const productId = button.getAttribute('data-product-id');
            const name = button.getAttribute('data-extension-name') ||
                        button.getAttribute('data-extension-name') ||
                        button.getAttribute('data-name') ||
                        'Product';

            const price = parseFloat(button.getAttribute('data-price') || '0.00');
            const quantity = parseInt(button.getAttribute('data-quantity') || '1');

            if (!productId) {
                showToast('Product ID missing', 'danger');
                console.error('No product ID found on button', button);
                return;
            }

            if (isNaN(price)) {
                showToast('Invalid product price', 'danger');
                console.error('Invalid price:', button.getAttribute('data-price'));
                return;
            }

            this.addItem(productId, name, price, quantity);
        }
    }

    // Make ShoppingCart globally available
    window.ShoppingCart = ShoppingCart;
    window.cart = new ShoppingCart();

    // Add global cart utility functions for easy access
    window.addToCart = function(productId, name, price, quantity = 1) {
        return window.cart.addItem(productId, name, price, quantity);
    };

    window.removeFromCart = function(productId) {
        return window.cart.removeItem(productId);
    };

    window.updateCartQuantity = function(productId, quantity) {
        return window.cart.updateQuantity(productId, quantity);
    };

    window.getCartTotal = function() {
        return window.cart.getTotalPrice();
    };

    window.getCartItems = function() {
        return window.cart.getItems();
    };

    window.clearCart = function() {
        return window.cart.clearCart();
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('Cart utilities DOM ready');
        });
    } else {
        console.log('Cart utilities loaded');
    }

})());