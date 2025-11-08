/**
 * CultivAR Diagnostics Module
 * A utility for debugging JavaScript issues in the application
 */

const CultivARDiagnostics = (function() {
    // Configuration
    const config = {
        enabled: true,
        logToConsole: true,
        logToPanel: true,
        logLevel: 'debug', // 'debug', 'info', 'warn', 'error'
        maxLogs: 100
    };

    // Log storage
    const logs = [];
    
    // Log levels
    const LOG_LEVELS = {
        debug: 0,
        info: 1,
        warn: 2,
        error: 3
    };

    // Initialize the diagnostics panel
    function initPanel() {
        if (!config.logToPanel) return;
        
        // Create panel if it doesn't exist
        if (!document.getElementById('diagnostics-panel')) {
            const panel = document.createElement('div');
            panel.id = 'diagnostics-panel';
            panel.className = 'diagnostics-panel';
            panel.innerHTML = `
                <div class="diagnostics-header">
                    <h3>JavaScript Diagnostics</h3>
                    <div class="diagnostics-controls">
                        <button id="clear-logs-btn" class="btn btn-sm btn-secondary">Clear</button>
                        <button id="close-diagnostics-btn" class="btn btn-sm btn-danger">Close</button>
                    </div>
                </div>
                <div id="diagnostics-content" class="diagnostics-content"></div>
            `;
            
            // Add styles
            const style = document.createElement('style');
            style.textContent = `
                .diagnostics-panel {
                    position: fixed;
                    bottom: 0;
                    right: 0;
                    width: 50%;
                    height: 300px;
                    background-color: rgba(0, 0, 0, 0.8);
                    color: #fff;
                    z-index: 9999;
                    font-family: monospace;
                    display: none;
                    flex-direction: column;
                    border-top-left-radius: 5px;
                    overflow: hidden;
                }
                .diagnostics-panel.visible {
                    display: flex;
                }
                .diagnostics-header {
                    padding: 5px 10px;
                    background-color: #333;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                .diagnostics-header h3 {
                    margin: 0;
                    font-size: 14px;
                }
                .diagnostics-content {
                    flex: 1;
                    overflow-y: auto;
                    padding: 10px;
                    font-size: 12px;
                }
                .log-entry {
                    margin-bottom: 5px;
                    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                    padding-bottom: 5px;
                }
                .log-debug { color: #aaa; }
                .log-info { color: #6cf; }
                .log-warn { color: #fc6; }
                .log-error { color: #f66; }
                .log-time { color: #999; font-size: 10px; margin-right: 5px; }
                .diagnostics-toggle {
                    position: fixed;
                    bottom: 10px;
                    right: 10px;
                    background-color: rgba(0, 0, 0, 0.5);
                    color: #fff;
                    border: none;
                    border-radius: 50%;
                    width: 40px;
                    height: 40px;
                    font-size: 20px;
                    cursor: pointer;
                    z-index: 9998;
                }
            `;
            
            document.head.appendChild(style);
            document.body.appendChild(panel);
            
            // Add toggle button
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'diagnostics-toggle';
            toggleBtn.innerHTML = '🐞';
            toggleBtn.title = 'Toggle Diagnostics Panel';
            document.body.appendChild(toggleBtn);
            
            // Event listeners
            toggleBtn.addEventListener('click', function() {
                panel.classList.toggle('visible');
            });
            
            document.getElementById('clear-logs-btn').addEventListener('click', function() {
                clearLogs();
            });
            
            document.getElementById('close-diagnostics-btn').addEventListener('click', function() {
                panel.classList.remove('visible');
            });
        }
    }

    // Log a message
    function log(level, message, data) {
        if (!config.enabled) return;
        
        // Check if we should log based on level
        if (LOG_LEVELS[level] < LOG_LEVELS[config.logLevel]) return;
        
        const timestamp = new Date();
        const logEntry = {
            level,
            message,
            data,
            timestamp
        };
        
        // Add to logs array
        logs.push(logEntry);
        
        // Trim logs if needed
        if (logs.length > config.maxLogs) {
            logs.shift();
        }
        
        // Log to console
        if (config.logToConsole) {
            const consoleMethod = level === 'debug' ? 'log' : level;
            if (data) {
                console[consoleMethod](`[${timestamp.toISOString()}] ${message}`, data);
            } else {
                console[consoleMethod](`[${timestamp.toISOString()}] ${message}`);
            }
        }
        
        // Log to panel
        if (config.logToPanel) {
            updatePanel(logEntry);
        }
        
        return logEntry;
    }
    
    // Update the diagnostics panel with a new log entry
    function updatePanel(logEntry) {
        const panel = document.getElementById('diagnostics-content');
        if (!panel) return;
        
        const entryElement = document.createElement('div');
        entryElement.className = `log-entry log-${logEntry.level}`;
        
        const timeStr = logEntry.timestamp.toISOString().split('T')[1].split('.')[0];
        let message = `<span class="log-time">${timeStr}</span> ${logEntry.message}`;
        
        if (logEntry.data) {
            message += ` <span class="log-data">${JSON.stringify(logEntry.data)}</span>`;
        }
        
        entryElement.innerHTML = message;
        panel.appendChild(entryElement);
        
        // Scroll to bottom
        panel.scrollTop = panel.scrollHeight;
    }
    
    // Clear all logs
    function clearLogs() {
        logs.length = 0;
        
        const panel = document.getElementById('diagnostics-content');
        if (panel) {
            panel.innerHTML = '';
        }
        
        log('info', 'Logs cleared');
    }
    
    // Track DOM events
    function trackEvents(selector, events) {
        if (!config.enabled) return;
        
        const elements = document.querySelectorAll(selector);
        
        events.forEach(eventName => {
            elements.forEach(element => {
                element.addEventListener(eventName, function(e) {
                    const elementInfo = {
                        id: element.id,
                        classes: Array.from(element.classList),
                        tag: element.tagName,
                        attributes: {}
                    };
                    
                    // Get relevant attributes
                    ['data-cultivar-id', 'onclick', 'href', 'type'].forEach(attr => {
                        if (element.hasAttribute(attr)) {
                            elementInfo.attributes[attr] = element.getAttribute(attr);
                        }
                    });
                    
                    log('debug', `Event '${eventName}' on ${selector}`, elementInfo);
                });
            });
        });
        
        log('info', `Tracking ${events.join(', ')} events on ${selector} (${elements.length} elements)`);
    }
    
    // Test a function and log results
    function testFunction(funcName, func, ...args) {
        if (!config.enabled) return func(...args);
        
        log('info', `Testing function: ${funcName} with args:`, args);
        
        try {
            const result = func(...args);
            log('debug', `Function ${funcName} executed successfully`, result);
            return result;
        } catch (error) {
            log('error', `Error in function ${funcName}:`, {
                message: error.message,
                stack: error.stack
            });
            throw error;
        }
    }
    
    // Monitor AJAX requests
    function monitorAjax() {
        if (!config.enabled || !window.jQuery) return;
        
        const originalAjax = jQuery.ajax;
        
        jQuery.ajax = function(url, options) {
            // If url is an object of options
            if (typeof url === 'object') {
                options = url;
                url = options.url;
            } else {
                options = options || {};
            }
            
            const requestId = Date.now();
            
            log('debug', `AJAX Request #${requestId} to ${url}`, {
                type: options.type || 'GET',
                data: options.data
            });
            
            // Create callbacks to log response
            const originalSuccess = options.success;
            const originalError = options.error;
            const originalComplete = options.complete;
            
            options.success = function(data, textStatus, jqXHR) {
                log('info', `AJAX Request #${requestId} succeeded`, {
                    url,
                    status: jqXHR.status,
                    data: data
                });
                
                if (originalSuccess) {
                    originalSuccess.apply(this, arguments);
                }
            };
            
            options.error = function(jqXHR, textStatus, errorThrown) {
                log('error', `AJAX Request #${requestId} failed`, {
                    url,
                    status: jqXHR.status,
                    error: errorThrown,
                    response: jqXHR.responseText
                });
                
                if (originalError) {
                    originalError.apply(this, arguments);
                }
            };
            
            options.complete = function(jqXHR, textStatus) {
                log('debug', `AJAX Request #${requestId} completed with status: ${textStatus}`);
                
                if (originalComplete) {
                    originalComplete.apply(this, arguments);
                }
            };
            
            return originalAjax.call(this, options);
        };
        
        log('info', 'AJAX monitoring enabled');
    }
    
    // Check if an element exists and is visible
    function checkElement(selector, description) {
        const element = document.querySelector(selector);
        const exists = !!element;
        const visible = exists && (
            window.getComputedStyle(element).display !== 'none' && 
            window.getComputedStyle(element).visibility !== 'hidden'
        );
        
        log('debug', `Element check: ${description || selector}`, {
            exists,
            visible,
            element: exists ? {
                id: element.id,
                classes: Array.from(element.classList),
                style: {
                    display: window.getComputedStyle(element).display,
                    visibility: window.getComputedStyle(element).visibility,
                    position: window.getComputedStyle(element).position
                }
            } : null
        });
        
        return { exists, visible, element };
    }
    
    // Public API
    return {
        init: function(options = {}) {
            // Merge options with defaults
            Object.assign(config, options);
            
            if (config.enabled) {
                initPanel();
                log('info', 'CultivAR Diagnostics initialized', config);
                
                // Set up error handling
                window.addEventListener('error', function(event) {
                    log('error', 'Uncaught error:', {
                        message: event.message,
                        filename: event.filename,
                        lineno: event.lineno,
                        colno: event.colno,
                        error: event.error ? event.error.stack : null
                    });
                });
                
                // Set up promise rejection handling
                window.addEventListener('unhandledrejection', function(event) {
                    log('error', 'Unhandled promise rejection:', {
                        reason: event.reason
                    });
                });
            }
            
            return this;
        },
        
        // Logging methods
        debug: function(message, data) {
            return log('debug', message, data);
        },
        
        info: function(message, data) {
            return log('info', message, data);
        },
        
        warn: function(message, data) {
            return log('warn', message, data);
        },
        
        error: function(message, data) {
            return log('error', message, data);
        },
        
        // Utility methods
        trackEvents,
        testFunction,
        monitorAjax,
        checkElement,
        clearLogs,
        
        // Configuration
        setLogLevel: function(level) {
            if (LOG_LEVELS.hasOwnProperty(level)) {
                config.logLevel = level;
                log('info', `Log level set to ${level}`);
            }
        },
        
        enable: function() {
            config.enabled = true;
            initPanel();
            log('info', 'Diagnostics enabled');
        },
        
        disable: function() {
            log('info', 'Diagnostics disabled');
            config.enabled = false;
        },
        
        showPanel: function() {
            const panel = document.getElementById('diagnostics-panel');
            if (panel) {
                panel.classList.add('visible');
            }
        },
        
        hidePanel: function() {
            const panel = document.getElementById('diagnostics-panel');
            if (panel) {
                panel.classList.remove('visible');
            }
        },
        
        // Get all logs
        getLogs: function() {
            return [...logs];
        }
    };
})();

// Auto-initialize if the page is already loaded
if (document.readyState === 'complete') {
    CultivARDiagnostics.init();
} else {
    window.addEventListener('load', function() {
        CultivARDiagnostics.init();
    });
}
