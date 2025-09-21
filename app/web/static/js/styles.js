/**
 * CultivAR Application Styles JavaScript
 * Additional functionality for the modern design system
 */

// Initialize all style-related functionality
class StylesManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupScrollEffects();
        this.setupInteractiveElements();
        this.setupResponsiveObservers();
        console.log('🎨 StylesManager initialized');
    }

    // Scroll-triggered effects
    setupScrollEffects() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && !entry.target.classList.contains('animate-in')) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe elements that should animate on scroll
        setTimeout(() => {
            // Target landing page elements for lazy loading
            document.querySelectorAll('.feature-card, .benefit-item, .stat-card, .features, .benefits, .newsletter, .cta').forEach(el => {
                observer.observe(el);
            });
        }, 100);
    }

    // Set up interactive elements
    setupInteractiveElements() {
        // Button hover effects
        document.querySelectorAll('.btn:not(.btn-icon)').forEach(btn => {
            btn.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-1px)';
            });

            btn.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });

        // Cards hover effects
        document.querySelectorAll('.card, .glass-card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-4px)';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = '';
            });
        });
    }

    // Responsive observers
    setupResponsiveObservers() {
        // Handle window resize events
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        });
    }

    handleResize() {
        // Handle mobile menu visibility
        const viewportWidth = window.innerWidth;
        const hamburgerMenu = document.getElementById('hamburger-menu');

        if (hamburgerMenu) {
            if (viewportWidth <= 768) {
                hamburgerMenu.style.display = 'flex';
            } else {
                hamburgerMenu.style.display = 'none';
                // Auto-collapse sidebar on desktop
                document.querySelector('.app-container')?.classList.remove('sidebar-collapsed');
                document.body.classList.remove('sidebar-open');
            }
        }
    }
}

// Utility functions for modern UI
const StylesUtils = {
    // Add ripple effect to buttons (Apple-style)
    addRippleEffect(button) {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.className = 'ripple-effect';

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    },

    // Smooth page transitions
    smoothPageTransition(targetUrl, delay = 300) {
        document.body.classList.add('page-transitioning');
        setTimeout(() => {
            window.location.href = targetUrl;
        }, delay);
    },

    // Show loading state for buttons
    setLoadingState(button, isLoading = true) {
        const originalContent = button.innerHTML;

        if (isLoading) {
            button.disabled = true;
            button.dataset.originalContent = originalContent;
            button.innerHTML = `
                <div class="loading-spinner">
                    <i class="fas fa-sync-alt spinning" aria-hidden="true"></i>
                    Loading...
                </div>
            `;
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalContent;
            delete button.dataset.originalContent;
        }
    }
};

// Add CSS for ripple effects
const rippleStyles = `
.ripple-effect {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    pointer-events: none;
    animation: ripple 0.6s ease-out;
    transform: scale(0);
}

@keyframes ripple {
    to {
        transform: scale(2);
        opacity: 0;
    }
}

.btn, .glass-card, .card {
    position: relative;
    overflow: hidden;
}

.page-transitioning {
    opacity: 0.7;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

.loading-spinner {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.spinning {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
`;

// Inject ripple styles
const styleSheet = document.createElement('style');
// Add CSP nonce for Content Security Policy compliance
if (window.cspNonce) {
    styleSheet.setAttribute('nonce', window.cspNonce);
}
styleSheet.textContent = rippleStyles;
document.head.appendChild(styleSheet);

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    // Initialize StylesManager
    new StylesManager();

    // Add ripple effects to interactive buttons
    document.querySelectorAll('.btn:not(.btn-icon)').forEach(btn => {
        StylesUtils.addRippleEffect(btn);
    });

    // Setup smooth page transitions for internal links
    document.querySelectorAll('a[href^="/"]').forEach(link => {
        link.addEventListener('click', function(e) {
            const targetUrl = this.getAttribute('href');
            if (targetUrl && targetUrl !== '#' && !this.hasAttribute('target')) {
                e.preventDefault();
                StylesUtils.smoothPageTransition(targetUrl);
            }
        });
    });
});

// Global utility functions
window.StylesUtils = StylesUtils;
