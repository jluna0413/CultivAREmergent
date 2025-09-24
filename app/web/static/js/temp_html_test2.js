// Extracted from temp_html_test2.txt
// Purpose: externalize inline DOMContentLoaded script for CSP compliance.
// Note: Created automatically. Review event handlers and selectors for compatibility.

document.addEventListener('DOMContentLoaded', function() {
    // Modern Hamburger Menu Handler with Apple-style animations
    const hamburgerBtn = document.getElementById('hamburger-menu');
    const appContainer = document.querySelector('.app-container');

    if (hamburgerBtn && appContainer) {
        hamburgerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();

            // Add Apple-style ripple effect
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);

            // Toggle sidebar with smooth animation
            appContainer.classList.toggle('sidebar-collapsed');
            document.body.classList.toggle('sidebar-open');
        });
    }

    // Modern User Menu Dropdown
    const userMenuBtn = document.getElementById('userMenuDropdown');
    const userDropdown = document.querySelector('.user-dropdown');

    if (userMenuBtn && userDropdown) {
        // Toggle dropdown
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.classList.toggle('active');

            // Rotate icon
            const icon = this.querySelector('.material-icons:last-child');
            if (icon) {
                icon.style.transform = userDropdown.classList.contains('active')
                    ? 'rotate(180deg)'
                    : '';
            }
        });

        // Close when clicking outside
        document.addEventListener('click', function() {
            userDropdown.classList.remove('active');
            const icon = userMenuBtn.querySelector('.material-icons:last-child');
            if (icon) icon.style.transform = '';
        });
    }

    // Modern Alert System
    document.querySelectorAll('.alert-close').forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                setTimeout(() => {
                    alert.parentNode.removeChild(alert);
                }, 300);
            }
        });
    });

    console.log('? Modern UI initialized - Apple/Samsung Design System active');
});
