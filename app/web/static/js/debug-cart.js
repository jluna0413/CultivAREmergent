// Console Debug Script - Copy all lines at once:
// Open browser console (F12), then:
// - Press Ctrl+A (select all)
// - Copy this entire code block
// - Go to your app (http://localhost:5000)
// - Open console and paste the code
// - Press Enter to run

(() => {
    'use strict';

    const results = {
        server: false,
        cartLoaded: false,
        cartCounter: false,
        marketRoute: 'unknown',
        authRoute: 'unknown'
    };

    console.log('🚀 TESTING CART SYSTEM - Please wait...\n');

    // Test 1: Server Connectivity
    fetch('/').then(r => {
        console.log(`${r.ok ? '✅' : '❌'} Server Response: ${r.status}`);
        results.server = r.ok;
    }).catch(e => {
        console.log('❌ Server Error:', e.message);
        results.server = false;
    });

    // Test 2: Cart System Loaded
    setTimeout(() => {
        console.log(`${window.cart ? '✅' : '❌'} Cart System:`, window.cart ? 'Loaded' : 'MISSING');
        results.cartLoaded = !!window.cart;

        if (window.cart) {
            console.log('🛒 Cart Methods Available:', typeof window.cart.addItem);
            console.log('📊 Current Cart:', window.cart.getItems());
        }
    }, 100);

    // Test 3: Cart Counter Element
    setTimeout(() => {
        const counter = document.getElementById('cart-counter');
        console.log(`${counter ? '✅' : '❌'} Cart Counter:`, counter ? 'Found' : 'MISSING');
        results.cartCounter = !!counter;
    }, 150);

    // Test 4: Market Route Access
    setTimeout(() => {
        fetch('/market/extensions')
            .then(r => {
                console.log(`🎯 Market Route: ${r.status} (${r.ok ? 'Working' : 'Redirect/Broken'})`);
                results.marketRoute = r.status;
            })
            .catch(e => {
                console.log('❌ Market Route Error:', e.message);
                results.marketRoute = 'error';
            });

        // Test Authentication
        fetch('/auth/login')
            .then(r => {
                console.log(`🔐 Auth Check: ${r.status} (${r.url.includes('login') ? 'Redirect Working' : 'Issue'})`);
                results.authRoute = r.status;
            })
            .catch(e => {
                console.log('❌ Auth Route Error:', e.message);
                results.authRoute = 'error';
            });
    }, 200);

    // Final Summary
    setTimeout(() => {
        console.log('\n📋 FINAL STATUS REPORT:');
        console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━`);
        console.log(`Server Online: ${results.server ? '✅ Yes' : '❌ No'}`);
        console.log(`Cart System: ${results.cartLoaded ? '✅ Loaded' : '❌ Missing'}`);
        console.log(`Cart Counter: ${results.cartCounter ? '✅ Found' : '❌ Missing'}`);
        console.log(`Market Route: ${results.marketRoute === 302 ? '✅ Working (Redirect)' : results.marketRoute === 404 ? '❌ Broken' : '⚠️ Unknown'}`);
        console.log(`Authentication: ${results.authRoute === 200 ? '✅ Ready' : '❌ Issue'}`);
        console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━`);

        if (results.server && results.cartLoaded && results.cartCounter) {
            console.log('🎉 CART SYSTEM IS WORKING!');
            console.log('Next: Test "Add to Cart" buttons → Look for green toast + cart counter');
        } else {
            console.log('⚠️ CART SYSTEM NEEDS FIXES');
            console.log('Check the specific failing tests above');
        }
    }, 1000);

})();

// === END OF SCRIPT - DON'T COPY THIS LINE ===