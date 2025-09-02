// Chrome Console Diagnostic Script for Cart Issues
// Run this in Chrome Developer Console to diagnose cart problems

(function() {
    console.log('🔍 CULTIVAR CART DIAGNOSTICS STARTING...');

    // Initialize diagnostic object
    window.cartDiagnostics = {
        issues: [],
        warnings: [],
        success: [],
        log: function(level, message) {
            if (level === 'error') this.issues.push(message);
            else if (level === 'warning') this.warnings.push(message);
            else this.success.push(message);
            console.log(`[${level.toUpperCase()}] ${message}`);
        }
    };

    // 1. Check if cart utilities script is loaded
    if (window.cart) {
        cartDiagnostics.log('success', '✅ cart-utilities.js script is loaded and window.cart exists');
    } else {
        cartDiagnostics.log('error', '❌ cart-utilities.js script NOT loaded - window.cart is undefined');
    }

    // 2. Check base template structure
    const headerRight = document.querySelector('.header-right');
    if (headerRight) {
        cartDiagnostics.log('success', '✅ .header-right element exists');

        // Check if cart nav exists
        const cartNav = headerRight.querySelector('.cart-nav, #cart-nav');
        if (cartNav) {
            cartDiagnostics.log('success', '✅ Cart navigation element exists');

            // Check cart counter
            const cartCounter = cartNav.querySelector('#cart-counter');
            if (cartCounter) {
                cartDiagnostics.log('success', '✅ Cart counter element exists');
                cartDiagnostics.log('info', `Cart counter current value: ${cartCounter.textContent}`);
            } else {
                cartDiagnostics.log('error', '❌ Cart counter (#cart-counter) element is missing');
            }

            // Check cart link
            const cartLink = cartNav.querySelector('a[href*="/cart"]');
            if (cartLink) {
                cartDiagnostics.log('success', '✅ Cart link exists with correct href');
            } else {
                cartDiagnostics.log('error', '❌ Cart link with /cart href not found');
            }

        } else {
            cartDiagnostics.log('error', '❌ Cart navigation element (.cart-nav or #cart-nav) not found in .header-right');
        }

    } else {
        cartDiagnostics.log('error', '❌ .header-right element not found - base template may be incomplete');
    }

    // 3. Check for "Add to Cart" buttons
    const addToCartBtns = document.querySelectorAll('.add-to-cart, .buy-seed, .add-gear');
    const regularBtns = document.querySelectorAll('button:contains("Add to Cart"), button:contains("Buy"), button:contains("Install")');

    if (addToCartBtns.length > 0) {
        cartDiagnostics.log('success', `✅ Found ${addToCartBtns.length} cart buttons with correct classes`);
        addToCartBtns.forEach((btn, index) => {
            console.log(`  Button ${index + 1}:`, {
                text: btn.textContent,
                classes: btn.className,
                parentCard: !!btn.closest('.card')
            });
        });
    } else {
        cartDiagnostics.log('warning', '⚠️ No buttons with cart classes (.add-to-cart, .buy-seed, .add-gear) found');

        // Check for alternative button text
        const anyPurchaseButtons = Array.from(regularBtns).filter(btn =>
            btn.textContent.toLowerCase().includes('buy') ||
            btn.textContent.toLowerCase().includes('add to cart') ||
            btn.textContent.toLowerCase().includes('install')
        );

        if (anyPurchaseButtons.length > 0) {
            cartDiagnostics.log('warning', `⚠️ Found ${anyPurchaseButtons.length} purchase-related buttons, but they may not have correct classes`);
        } else {
            cartDiagnostics.log('error', '❌ No purchase/add-to-cart buttons found at all');
        }
    }

    // 4. Check DOM structure expectations
    const extensionCards = document.querySelectorAll('.extension-card');
    if (extensionCards.length > 0) {
        cartDiagnostics.log('success', `✅ Found ${extensionCards.length} extension cards`);

        // Check first card structure
        const firstCard = extensionCards[0];
        const cardTitle = firstCard.querySelector('.card-title');
        const cardPrice = firstCard.querySelector('.text-success, .extension-card-price');
        const cardImage = firstCard.querySelector('img');

        if (cardTitle) cartDiagnostics.log('success', '✅ Card titles are present');
        else cartDiagnostics.log('error', '❌ Card titles missing (.card-title)');

        if (cardPrice) cartDiagnostics.log('success', '✅ Card pricing elements exist');
        else cartDiagnostics.log('error', '❌ Card pricing elements missing');

        if (cardImage) cartDiagnostics.log('success', '✅ Card images are present');
        else cartDiagnostics.log('warning', '⚠️ Cards may be missing images');

    } else {
        cartDiagnostics.log('warning', '⚠️ No extension cards (.extension-card) found');
    }

    // 5. Check for cart page
    const isCartPage = window.location.pathname.includes('/cart');
    if (isCartPage) {
        cartDiagnostics.log('info', '📍 Currently on cart page - checking cart page structure');

        const cartItems = document.querySelectorAll('.cart-item');
        const cartEmpty = document.querySelector('.empty-cart, #empty-cart');
        const cartTable = document.querySelector('.cart-table, #cart-table');

        if (cartEmpty && cartItems.length === 0) {
            cartDiagnostics.log('success', '✅ Empty cart state properly displayed');
        } else if (cartItems.length > 0) {
            cartDiagnostics.log('success', `✅ ${cartItems.length} cart items found`);
        } else {
            cartDiagnostics.log('error', '❌ Cart page loaded but no items container or empty state found');
        }

    } else {
        cartDiagnostics.log('info', '📍 Not on cart page - checking market page structure');
    }

    // 6. Check for JavaScript errors
    if ('console' in window && 'error' in console) {
        // Temporary override to capture errors
        const originalError = console.error;
        const jsErrors = [];
        console.error = function(...args) {
            jsErrors.push(args.join(' '));
            originalError.apply(console, args);
        };

        // Restore after a brief delay
        setTimeout(() => {
            console.error = originalError;
            if (jsErrors.length > 0) {
                jsErrors.forEach(error => cartDiagnostics.log('warning', `⚠️ JS Error detected: ${error}`));
            } else {
                cartDiagnostics.log('success', '✅ No JavaScript errors detected in past 3 seconds');
            }
        }, 3000);
    }

    // 7. Test cart functionality if available
    if (window.cart) {
        cartDiagnostics.log('info', '🧪 Testing cart functionality...');

        try {
            // Test cart loading
            const cartData = window.cart.getCart();
            cartDiagnostics.log('success', '✅ Cart.getCart() works');

            // Test cart state
            const itemCount = window.cart.getItemCount();
            cartDiagnostics.log('info', `Cart item count: ${itemCount}`);

            const totalPrice = window.cart.getTotalPrice();
            cartDiagnostics.log('info', `Cart total price: $${totalPrice.toFixed(2)}`);

            // Test navigation update
            window.cart.updateNavigation();
            cartDiagnostics.log('success', '✅ Cart.updateNavigation() works');

        } catch (error) {
            cartDiagnostics.log('error', `❌ Cart functionality error: ${error.message}`);
        }
    }

    // 8. Summary report
    setTimeout(() => {
        console.log('\n📊 DIAGNOSTIC SUMMARY REPORT');
        console.log('=====================================');
        console.log(`✅ Success: ${cartDiagnostics.success.length} checks passed`);
        console.log(`⚠️ Warnings: ${cartDiagnostics.warnings.length} potential issues`);
        console.log(`❌ Errors: ${cartDiagnostics.issues.length} critical problems`);

        if (cartDiagnostics.issues.length > 0) {
            console.log('\n🔴 CRITICAL ISSUES FOUND:');
            cartDiagnostics.issues.forEach((issue, index) => console.log(`  ${index + 1}. ${issue}`));
        }

        if (cartDiagnostics.warnings.length > 0) {
            console.log('\n🟡 WARNINGS:');
            cartDiagnostics.warnings.forEach((warning, index) => console.log(`  ${index + 1}. ${warning}`));
        }

        if (cartDiagnostics.success.length > 0) {
            console.log('\n🟢 WORKING COMPONENTS:');
            cartDiagnostics.success.forEach((success, index) => console.log(`  ${index + 1}. ${success}`));
        }

        console.log('=====================================');
        console.log('🔍 Run diagnostics complete!');
    }, 3500);

})();