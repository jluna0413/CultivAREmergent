// Quick Cart Test - Copy and paste this into browser console
(function() {
    console.log('🧪 QUICK CART TEST STARTING...');

    // Check Flask server availability
    fetch('/').then(function(response) {
        if (response.ok) {
            console.log('✅ Flask server responding at /');
            console.log('Status:', response.status, response.statusText);

            // Test market route
            return fetch('/market/extensions');
        } else {
            console.log('❌ Flask server not responding:', response.status);
            return Promise.reject('Server not responding');
        }
    }).then(function(response) {
        console.log('📊 /market/extensions response:');
        console.log('Status:', response.status, response.statusText);
        console.log('Content-Type:', response.headers.get('content-type'));

        if (response.ok) {
            console.log('✅ Route accessible');
            return response.text().then(function(text) {
                console.log('Response contains HTML:', text.length, 'characters');
                if (text.includes('extension-card')) {
                    console.log('✅ Market extensions HTML found');
                } else {
                    console.log('⚠️ Market extensions HTML not found');
                }
            });
        } else {
            return fetch('/auth/login').then(function(loginResponse) {
                if (loginResponse.redirected) {
                    console.log('🔒 Route requires authentication - redirected to:', loginResponse.url);
                    return loginResponse.text().then(function(loginHtml) {
                        console.log('Login page content length:', loginHtml.length);
                        if (loginHtml.includes('login')) {
                            console.log('✅ Login page found');
                            console.log('💡 SOLUTION: Access /market/extensions after logging in!');
                        }
                    });
                } else {
                    console.log('❌ Authentication redirect not working:', loginResponse.status);
                }
            });
        }
    }).catch(function(error) {
        console.log('❌ Network error:', error);
    });

    // Check cart utilities loading
    setTimeout(function() {
        console.log('\n🛒 CART UTILITIES STATUS:');
        if (window.cart) {
            console.log('✅ window.cart exists');
            try {
                console.log('Cart item count:', window.cart.getItemCount());
                const cart = window.cart.getCart();
                console.log('Cart contents:', Object.keys(cart).length, 'items');
            } catch(e) {
                console.log('⚠️ Cart method error:', e.message);
            }
        } else {
            console.log('❌ window.cart not found - cart utilities not loaded');
        }
    }, 1000);

    console.log('🚀 Test complete. Check results above.');
})();