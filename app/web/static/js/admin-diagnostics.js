/**
 * CultivAR Admin Diagnostics
 *
 * This script provides diagnostic tools for debugging client-side issues.
 * It can be enabled/disabled from the admin dashboard.
 */

(function() {
    console.log('Admin diagnostics script loaded');

    // Check if diagnostics are enabled
    const diagnosticsEnabled = localStorage.getItem('diagnostics_enabled') === 'true';

    if (!diagnosticsEnabled) {
        console.log('Diagnostics are disabled. Enable them from the admin dashboard.');
        return; // Exit if diagnostics are not enabled
    }

    console.log('Diagnostics are enabled. Initializing...');

    // Create diagnostics panel
    function createDiagnosticsPanel() {
        // Remove any existing panel
        const existingPanel = document.getElementById('diagnostics-panel');
        if (existingPanel) {
            existingPanel.remove();
        }

        const panel = document.createElement('div');
        panel.id = 'diagnostics-panel';
        panel.style.position = 'fixed';
        panel.style.bottom = '10px';
        panel.style.right = '10px';
        panel.style.width = '400px';
        panel.style.maxHeight = '500px';
        panel.style.overflowY = 'auto';
        panel.style.backgroundColor = 'rgba(0, 0, 0, 0.9)';
        panel.style.color = '#00ff00';
        panel.style.fontFamily = 'monospace';
        panel.style.fontSize = '12px';
        panel.style.padding = '15px';
        panel.style.zIndex = '9999';
        panel.style.borderTop = '3px solid #00ff00';
        panel.style.borderLeft = '3px solid #00ff00';
        panel.style.borderRight = '1px solid #00ff00';
        panel.style.borderBottom = '1px solid #00ff00';
        panel.style.boxShadow = '0 0 20px rgba(0, 255, 0, 0.3)';
        panel.style.borderRadius = '5px';

        // Add header
        const header = document.createElement('div');
        header.style.display = 'flex';
        header.style.justifyContent = 'space-between';
        header.style.alignItems = 'center';
        header.style.marginBottom = '10px';
        header.style.borderBottom = '1px solid #00ff00';
        header.style.paddingBottom = '5px';

        const title = document.createElement('h3');
        title.textContent = 'CultivAR Diagnostics';
        title.style.margin = '0';
        title.style.color = '#00ff00';
        title.style.fontSize = '14px';

        const closeBtn = document.createElement('button');
        closeBtn.textContent = 'X';
        closeBtn.style.backgroundColor = 'transparent';
        closeBtn.style.border = '1px solid #00ff00';
        closeBtn.style.color = '#00ff00';
        closeBtn.style.cursor = 'pointer';
        closeBtn.style.padding = '2px 6px';
        closeBtn.addEventListener('click', function() {
            panel.style.display = 'none';
        });

        header.appendChild(title);
        header.appendChild(closeBtn);
        panel.appendChild(header);

        // Add content container
        const content = document.createElement('div');
        content.id = 'diagnostics-content';
        panel.appendChild(content);

        // Add controls
        const controls = document.createElement('div');
        controls.style.marginTop = '10px';
        controls.style.display = 'flex';
        controls.style.gap = '5px';

        const clearBtn = document.createElement('button');
        clearBtn.textContent = 'Clear';
        clearBtn.style.backgroundColor = 'transparent';
        clearBtn.style.border = '1px solid #00ff00';
        clearBtn.style.color = '#00ff00';
        clearBtn.style.cursor = 'pointer';
        clearBtn.style.padding = '2px 6px';
        clearBtn.addEventListener('click', function() {
            document.getElementById('diagnostics-content').innerHTML = '';
        });

        const disableBtn = document.createElement('button');
        disableBtn.textContent = 'Disable Diagnostics';
        disableBtn.style.backgroundColor = 'transparent';
        disableBtn.style.border = '1px solid #00ff00';
        disableBtn.style.color = '#00ff00';
        disableBtn.style.cursor = 'pointer';
        disableBtn.style.padding = '2px 6px';
        disableBtn.addEventListener('click', function() {
            localStorage.setItem('diagnostics_enabled', 'false');
            panel.remove();
            logMessage('Diagnostics disabled. Refresh page to apply changes.');
        });

        controls.appendChild(clearBtn);
        controls.appendChild(disableBtn);
        panel.appendChild(controls);

        return panel;
    }

    // Log message to diagnostics panel
    function logMessage(message, type = 'info') {
        const content = document.getElementById('diagnostics-content');
        if (!content) return;

        const entry = document.createElement('div');
        entry.style.marginBottom = '5px';
        entry.style.borderBottom = '1px dotted rgba(0, 255, 0, 0.3)';
        entry.style.paddingBottom = '5px';

        const timestamp = new Date().toLocaleTimeString();

        let color = '#00ff00'; // Default color (info)
        if (type === 'error') {
            color = '#ff5555';
        } else if (type === 'warn') {
            color = '#ffff55';
        } else if (type === 'debug') {
            color = '#55aaff';
        }

        entry.innerHTML = `<span style="color: #aaaaaa;">[${timestamp}]</span> <span style="color: ${color};">${message}</span>`;
        content.appendChild(entry);

        // Auto-scroll to bottom
        content.scrollTop = content.scrollHeight;
    }

    // Initialize diagnostics
    function initDiagnostics() {
        // Add panel to the document
        const panel = createDiagnosticsPanel();
        document.body.appendChild(panel);

        // Log initial information with a prominent header
        logMessage('=== CULTIVAR DIAGNOSTICS INITIALIZED ===', 'debug');
        logMessage('Diagnostics panel is now active', 'debug');
        logMessage(`Page: ${window.location.pathname}`);
        logMessage(`URL: ${window.location.href}`);
        logMessage(`User Agent: ${navigator.userAgent}`);
        logMessage('=== SYSTEM INFORMATION ===', 'debug');

        // Collect page performance metrics
        if (window.performance) {
            setTimeout(() => {
                const perfData = window.performance.timing;
                const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
                const domReadyTime = perfData.domComplete - perfData.domLoading;

                logMessage(`Page Load Time: ${pageLoadTime}ms`);
                logMessage(`DOM Ready Time: ${domReadyTime}ms`);
            }, 0);
        }

        // Monitor AJAX requests
        monitorAjaxRequests();

        // Monitor JavaScript errors
        monitorJsErrors();

        // Check for specific page diagnostics
        const diagnosticsPage = localStorage.getItem('diagnostics_page');
        if (diagnosticsPage && window.location.pathname === diagnosticsPage) {
            logMessage(`Running diagnostics for ${diagnosticsPage}`, 'debug');
            runPageSpecificDiagnostics(diagnosticsPage);
        }
    }

    // Monitor AJAX requests
    function monitorAjaxRequests() {
        const originalXHR = window.XMLHttpRequest;

        function newXHR() {
            const xhr = new originalXHR();

            xhr.addEventListener('load', function() {
                const url = this._url;
                const status = this.status;
                const statusText = this.statusText;

                if (status >= 200 && status < 300) {
                    logMessage(`AJAX Success: ${url} (${status} ${statusText})`);
                } else {
                    logMessage(`AJAX Error: ${url} (${status} ${statusText})`, 'error');
                }
            });

            xhr.addEventListener('error', function() {
                logMessage(`AJAX Failed: ${this._url}`, 'error');
            });

            xhr.addEventListener('timeout', function() {
                logMessage(`AJAX Timeout: ${this._url}`, 'warn');
            });

            const originalOpen = xhr.open;
            xhr.open = function(method, url) {
                this._url = url;
                this._method = method;
                logMessage(`AJAX Request: ${method} ${url}`, 'debug');
                return originalOpen.apply(this, arguments);
            };

            return xhr;
        }

        window.XMLHttpRequest = newXHR;
    }

    // Monitor JavaScript errors
    function monitorJsErrors() {
        window.addEventListener('error', function(event) {
            const message = event.message;
            const source = event.filename;
            const line = event.lineno;
            const column = event.colno;

            logMessage(`JS Error: ${message} at ${source}:${line}:${column}`, 'error');
        });

        window.addEventListener('unhandledrejection', function(event) {
            logMessage(`Unhandled Promise Rejection: ${event.reason}`, 'error');
        });
    }

    // Run page-specific diagnostics
    function runPageSpecificDiagnostics(page) {
        // Check for common elements
        setTimeout(() => {
            // Check for forms
            const forms = document.querySelectorAll('form');
            if (forms.length > 0) {
                logMessage(`Found ${forms.length} form(s) on the page`, 'debug');

                forms.forEach((form, index) => {
                    const formId = form.id || `form-${index}`;
                    logMessage(`Form: ${formId} (${form.method || 'GET'} to ${form.action || 'current page'})`, 'debug');

                    // Monitor form submissions
                    form.addEventListener('submit', function(e) {
                        logMessage(`Form submitted: ${formId}`, 'info');
                    });
                });
            }

            // Check for AJAX-loaded content
            const ajaxContainers = document.querySelectorAll('[data-ajax-url]');
            if (ajaxContainers.length > 0) {
                logMessage(`Found ${ajaxContainers.length} AJAX container(s)`, 'debug');
            }

            // Check for charts
            if (window.Chart) {
                const canvases = document.querySelectorAll('canvas');
                const potentialCharts = Array.from(canvases).filter(canvas => canvas.chart);
                if (potentialCharts.length > 0) {
                    logMessage(`Found ${potentialCharts.length} Chart.js chart(s)`, 'debug');
                }
            }
        }, 1000);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initDiagnostics);
    } else {
        initDiagnostics();
    }
})();
