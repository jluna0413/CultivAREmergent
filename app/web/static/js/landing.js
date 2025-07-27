/**
 * CultivAR Landing Page JavaScript
 * Apple/Samsung style interactions and animations
 */

class LandingPage {
    constructor() {
        this.init();
    }

    init() {
        this.setupSmoothScrolling();
        this.setupMobileMenu();
        this.setupNewsletterForm();
        this.setupScrollAnimations();
        this.setupParallaxEffects();
        this.setupTypewriter();
    }

    // Smooth scrolling for navigation links
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Mobile menu toggle
    setupMobileMenu() {
        const mobileToggle = document.querySelector('.nav-mobile');
        const navLinks = document.querySelector('.nav-links');
        
        if (mobileToggle && navLinks) {
            mobileToggle.addEventListener('click', () => {
                navLinks.classList.toggle('active');
            });

            // Close menu when clicking on a link
            navLinks.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', () => {
                    navLinks.classList.remove('active');
                });
            });
        }
    }

    // Newsletter form handling
    setupNewsletterForm() {
        const form = document.getElementById('newsletter-form');
        const phoneInput = document.getElementById('phone-input');
        const successMessage = document.getElementById('newsletter-success');

        if (form && phoneInput && successMessage) {
            // Phone number formatting
            phoneInput.addEventListener('input', (e) => {
                let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
                if (value.length >= 6) {
                    value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
                } else if (value.length >= 3) {
                    value = value.replace(/(\d{3})(\d{0,3})/, '($1) $2');
                }
                e.target.value = value;
            });

            // Form submission
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const phone = phoneInput.value.replace(/\D/g, ''); // Clean phone number
                
                if (phone.length !== 10) {
                    this.showNotification('Please enter a valid 10-digit phone number', 'error');
                    return;
                }

                try {
                    // Show loading state
                    const submitBtn = form.querySelector('button[type="submit"]');
                    const originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
                    submitBtn.disabled = true;

                    // Simulate API call (replace with actual endpoint)
                    await this.subscribeToNewsletter(phone);
                    
                    // Show success
                    form.style.display = 'none';
                    successMessage.style.display = 'flex';
                    
                    // Track conversion
                    this.trackEvent('newsletter_signup', { phone: phone });
                    
                } catch (error) {
                    console.error('Newsletter signup error:', error);
                    this.showNotification('Something went wrong. Please try again.', 'error');
                    
                    // Reset button
                    const submitBtn = form.querySelector('button[type="submit"]');
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            });
        }
    }

    // Newsletter API call
    async subscribeToNewsletter(phone) {
        // Replace with your actual API endpoint
        const response = await fetch('/api/newsletter/subscribe', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phone })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        return response.json();
    }

    // Scroll animations using Intersection Observer
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.feature-card, .benefit-item, .testimonial, .stat-card').forEach(el => {
            observer.observe(el);
        });

        // Add CSS for animations
        this.addAnimationStyles();
    }

    // Add CSS animations dynamically
    addAnimationStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .feature-card,
            .benefit-item,
            .testimonial,
            .stat-card {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            }
            
            .feature-card.animate-in,
            .benefit-item.animate-in,
            .testimonial.animate-in,
            .stat-card.animate-in {
                opacity: 1;
                transform: translateY(0);
            }
            
            /* Stagger animation delays */
            .feature-card:nth-child(2) { transition-delay: 0.1s; }
            .feature-card:nth-child(3) { transition-delay: 0.2s; }
            .feature-card:nth-child(4) { transition-delay: 0.3s; }
            .feature-card:nth-child(5) { transition-delay: 0.4s; }
            .feature-card:nth-child(6) { transition-delay: 0.5s; }
            
            .stat-card:nth-child(2) { transition-delay: 0.1s; }
            .stat-card:nth-child(3) { transition-delay: 0.2s; }
            .stat-card:nth-child(4) { transition-delay: 0.3s; }
        `;
        document.head.appendChild(style);
    }

    // Parallax effects for hero section
    setupParallaxEffects() {
        const heroVisual = document.querySelector('.hero-visual');
        
        if (heroVisual) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                
                if (scrolled < window.innerHeight) {
                    heroVisual.style.transform = `translateY(${rate}px)`;
                }
            });
        }
    }

    // Typewriter effect for hero title
    setupTypewriter() {
        const heroTitle = document.querySelector('.hero-title');
        if (!heroTitle) return;

        const text = heroTitle.innerHTML;
        heroTitle.innerHTML = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        };

        // Start typewriter after a delay
        setTimeout(typeWriter, 1000);
    }

    // Show notification
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'check-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#ff4444' : '#4CAF50'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            z-index: 10000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(400px)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    }

    // Analytics tracking
    trackEvent(eventName, properties = {}) {
        // Replace with your analytics service (Google Analytics, Mixpanel, etc.)
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, properties);
        }
        
        console.log('Event tracked:', eventName, properties);
    }

    // Interactive dashboard demo
    setupDashboardDemo() {
        const dashboard = document.querySelector('.hero-dashboard');
        if (!dashboard) return;

        // Add click interactions to dashboard elements
        const widgets = dashboard.querySelectorAll('.widget');
        widgets.forEach(widget => {
            widget.addEventListener('click', () => {
                widget.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    widget.style.transform = 'scale(1)';
                }, 200);
            });
        });

        // Animate numbers
        this.animateNumbers();
    }

    // Animate counter numbers
    animateNumbers() {
        const counters = document.querySelectorAll('.stat-number, .widget-number');
        
        counters.forEach(counter => {
            const target = parseInt(counter.innerText.replace(/\D/g, ''));
            let current = 0;
            const increment = target / 100;
            
            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    counter.innerText = Math.ceil(current).toLocaleString();
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.innerText = target.toLocaleString();
                }
            };
            
            // Start animation when element is visible
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        updateCounter();
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(counter);
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LandingPage();
});

// Add mobile navigation styles
const mobileNavStyles = `
    @media (max-width: 768px) {
        .nav-links {
            position: fixed;
            top: 0;
            right: -100%;
            width: 100%;
            height: 100vh;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            flex-direction: column;
            justify-content: center;
            align-items: center;
            transition: right 0.3s ease;
            z-index: 999;
        }
        
        .nav-links.active {
            right: 0;
        }
        
        .nav-links a {
            font-size: 1.5rem;
            margin: 1rem 0;
        }
        
        .nav-mobile {
            z-index: 1001;
        }
    }
`;

// Add the mobile styles
const styleSheet = document.createElement('style');
styleSheet.textContent = mobileNavStyles;
document.head.appendChild(styleSheet);