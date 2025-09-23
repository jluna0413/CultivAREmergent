/**
 * CultivAR Theme Manager
 * Light/Dark theme system with Apple/Samsung aesthetics
 * Light theme as default, with persistent storage
 */

class ThemeManager {
    constructor() {
        this.currentTheme = 'light';
        this.init();
    }

    init() {
        // Check system preference
        const savedTheme = this.getSavedTheme();
        const systemTheme = this.getSystemTheme();

        // Priority: saved > system > default (light)
        this.currentTheme = savedTheme || systemTheme || 'light';

        // Apply theme immediately
        this.applyTheme(this.currentTheme);

        // Set up theme toggle listeners
        this.setupThemeToggle();

        // Watch for system theme changes
        this.watchSystemTheme();

        console.log(`ThemeManager initialized: ${this.currentTheme} theme`);
    }

    getSavedTheme() {
        try {
            return localStorage.getItem('cultivar-theme');
        } catch (e) {
            return null;
        }
    }

    saveTheme(theme) {
        try {
            localStorage.setItem('cultivar-theme', theme);
        } catch (e) {
            console.warn('Failed to save theme preference');
        }
    }

    getSystemTheme() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            return 'dark';
        }
        return 'light'; // Default to light as requested
    }

    watchSystemTheme() {
        // Listen for system theme changes when no saved preference exists
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                if (!this.getSavedTheme()) {
                    const newTheme = e.matches ? 'dark' : 'light';
                    this.applyTheme(newTheme);
                }
            });
        }
    }

    applyTheme(theme) {
        this.currentTheme = theme;

        // Apply theme attribute to document root
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }

        // Update meta theme-color for mobile browsers
        this.updateMetaThemeColor(theme);

        // Update all theme toggle buttons
        this.updateThemeToggleButtons(theme);

        // Dispatch theme change event
        this.dispatchThemeChangeEvent(theme);

        // Save preference
        this.saveTheme(theme);
    }

    updateMetaThemeColor(theme) {
        const existingMeta = document.querySelector('meta[name="theme-color"]');
        const targetColor = theme === 'dark' ? '#000000' : '#ffffff';

        if (existingMeta) {
            existingMeta.setAttribute('content', targetColor);
        } else {
            const meta = document.createElement('meta');
            meta.name = 'theme-color';
            meta.content = targetColor;
            document.head.appendChild(meta);
        }
    }

    updateThemeToggleButtons(theme) {
        const toggles = document.querySelectorAll('.theme-toggle');
        toggles.forEach(toggle => {
            toggle.classList.toggle('active', theme === 'dark');

            // Update accessibility attributes
            toggle.setAttribute('aria-label',
                theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme'
            );
        });
    }

    dispatchThemeChangeEvent(theme) {
        const event = new CustomEvent('themeChanged', {
            detail: { theme, isDark: theme === 'dark' }
        });
        document.dispatchEvent(event);
    }

    setupThemeToggle() {
        // Set up click handlers for theme toggle buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('.theme-toggle')) {
                e.preventDefault();
                this.toggleTheme();
            }
        });

        // Set up keyboard support
        document.addEventListener('keydown', (e) => {
            if (e.target.closest('.theme-toggle') && (e.key === 'Enter' || e.key === ' ')) {
                e.preventDefault();
                this.toggleTheme();
            }
        });

        // Update initial button state
        this.updateThemeToggleButtons(this.currentTheme);
    }

    toggleTheme(animate = true) {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';

        if (animate) {
            // Add transition class to body for smooth theme change
            document.body.classList.add('theme-transitioning');

            setTimeout(() => {
                this.applyTheme(newTheme);
                setTimeout(() => {
                    document.body.classList.remove('theme-transitioning');
                }, 300);
            }, 100);
        } else {
            this.applyTheme(newTheme);
        }
    }

    setTheme(theme, animate = true) {
        if (theme !== 'light' && theme !== 'dark') {
            console.warn('Invalid theme:', theme);
            return;
        }

        if (theme !== this.currentTheme) {
            this.toggleTheme(animate);
        }
    }

    getCurrentTheme() {
        return this.currentTheme;
    }

    isDark() {
        return this.currentTheme === 'dark';
    }

    // Utility methods for other scripts
    prefersHighContrast() {
        return window.matchMedia && window.matchMedia('(prefers-contrast: high)').matches;
    }

    prefersReducedMotion() {
        return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    }

    // Save theme once per user action (debounced)
    saveThemePreference = (() => {
        let timeout;
        const delay = 1000;

        return (theme) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => this.saveTheme(theme), delay);
        };
    })();
}

// Global theme manager instance
window.themeManager = new ThemeManager();

// Theme toggle convenience functions for templates
window.toggleTheme = () => window.themeManager.toggleTheme();
window.setLightTheme = () => window.themeManager.setTheme('light');
window.setDarkTheme = () => window.themeManager.setTheme('dark');

// Add smooth theme transitions
const themeTransitionStyles = `
.theme-transitioning * {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease !important;
}
`;

const themeStyleSheet = document.createElement('style');
// Add CSP nonce for Content Security Policy compliance
if (window.cspNonce) {
    themeStyleSheet.setAttribute('nonce', window.cspNonce);
}
themeStyleSheet.textContent = themeTransitionStyles;
document.head.appendChild(themeStyleSheet);

// Export for modules if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
