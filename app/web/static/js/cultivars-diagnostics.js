/**
 * Cultivars Page Diagnostics
 * Specific diagnostics for the cultivars page
 */

function initCultivarsPageDiagnostics() {
    // Make sure the diagnostics module is loaded
    if (typeof CultivARDiagnostics === 'undefined') {
        console.error('CultivARDiagnostics module not loaded');
        return;
    }
    
    CultivARDiagnostics.info('Initializing cultivars page diagnostics');
    
    // Check if we're on the cultivars page
    if (!window.location.pathname.includes('/cultivars')) {
        CultivARDiagnostics.info('Not on cultivars page, skipping diagnostics');
        return;
    }
    
    // Enable AJAX monitoring
    CultivARDiagnostics.monitorAjax();
    
    // Track button clicks
    CultivARDiagnostics.trackEvents('.edit-cultivar', ['click']);
    CultivARDiagnostics.trackEvents('.delete-cultivar', ['click']);
    
    // Check if buttons exist
    const editButtons = document.querySelectorAll('.edit-cultivar');
    const deleteButtons = document.querySelectorAll('.delete-cultivar');
    
    CultivARDiagnostics.info('Cultivar buttons found', {
        editButtons: editButtons.length,
        deleteButtons: deleteButtons.length
    });
    
    // Check if onclick handlers are properly set
    if (editButtons.length > 0) {
        const firstEditButton = editButtons[0];
        const onclickAttr = firstEditButton.getAttribute('onclick');
        const cultivarId = firstEditButton.getAttribute('data-cultivar-id');
        
        CultivARDiagnostics.debug('Edit button inspection', {
            button: firstEditButton.outerHTML,
            onclick: onclickAttr,
            cultivarId: cultivarId
        });
        
        // Test if the editCultivar function exists
        if (typeof editCultivar === 'function') {
            CultivARDiagnostics.info('editCultivar function exists');
            
            // Create a wrapper for the editCultivar function
            const originalEditCultivar = window.editCultivar;
            window.editCultivar = function(cultivarId) {
                CultivARDiagnostics.info('editCultivar called with ID: ' + cultivarId);
                try {
                    return originalEditCultivar(cultivarId);
                } catch (error) {
                    CultivARDiagnostics.error('Error in editCultivar', {
                        message: error.message,
                        stack: error.stack
                    });
                    throw error;
                }
            };
        } else {
            CultivARDiagnostics.error('editCultivar function does not exist');
        }
    }
    
    // Check if deleteCultivar function exists and wrap it
    if (typeof deleteCultivar === 'function') {
        CultivARDiagnostics.info('deleteCultivar function exists');
        
        const originalDeleteCultivar = window.deleteCultivar;
        window.deleteCultivar = function(cultivarId) {
            CultivARDiagnostics.info('deleteCultivar called with ID: ' + cultivarId);
            try {
                return originalDeleteCultivar(cultivarId);
            } catch (error) {
                CultivARDiagnostics.error('Error in deleteCultivar', {
                    message: error.message,
                    stack: error.stack
                });
                throw error;
            }
        };
    } else {
        CultivARDiagnostics.error('deleteCultivar function does not exist');
    }
    
    // Check modal functionality
    CultivARDiagnostics.checkElement('#addCultivarModal', 'Cultivar Modal');
    
    // Test jQuery modal functionality
    if (typeof jQuery !== 'undefined' && typeof jQuery.fn.modal !== 'undefined') {
        CultivARDiagnostics.info('jQuery modal plugin is available');
    } else {
        CultivARDiagnostics.error('jQuery modal plugin is NOT available');
        
        // Check what version of Bootstrap is loaded
        if (typeof bootstrap !== 'undefined') {
            CultivARDiagnostics.info('Bootstrap version', bootstrap.Tooltip.VERSION || 'unknown');
        } else {
            CultivARDiagnostics.warn('Bootstrap is not loaded or not available in global scope');
        }
    }
    
    // Add a test button to manually trigger diagnostics
    const testButton = document.createElement('button');
    testButton.className = 'btn btn-warning';
    testButton.innerHTML = 'Run Diagnostics';
    testButton.style.position = 'fixed';
    testButton.style.top = '10px';
    testButton.style.right = '10px';
    testButton.style.zIndex = '9999';
    
    testButton.addEventListener('click', function() {
        runCultivarsPageDiagnostics();
    });
    
    document.body.appendChild(testButton);
    
    CultivARDiagnostics.info('Cultivars page diagnostics initialized');
}

function runCultivarsPageDiagnostics() {
    CultivARDiagnostics.info('Running cultivars page diagnostics');
    
    // Show the diagnostics panel
    CultivARDiagnostics.showPanel();
    
    // Check all relevant elements
    CultivARDiagnostics.checkElement('.cultivar-item', 'Cultivar Items');
    CultivARDiagnostics.checkElement('.edit-cultivar', 'Edit Buttons');
    CultivARDiagnostics.checkElement('.delete-cultivar', 'Delete Buttons');
    CultivARDiagnostics.checkElement('#addCultivarModal', 'Add Cultivar Modal');
    
    // Check if functions exist
    ['editCultivar', 'deleteCultivar', 'closeModal', 'showAddCultivarModal'].forEach(funcName => {
        if (typeof window[funcName] === 'function') {
            CultivARDiagnostics.info(`Function ${funcName} exists`);
        } else {
            CultivARDiagnostics.error(`Function ${funcName} does not exist`);
        }
    });
    
    // Check jQuery and Bootstrap
    if (typeof jQuery !== 'undefined') {
        CultivARDiagnostics.info('jQuery version', jQuery.fn.jquery);
        
        if (typeof jQuery.fn.modal !== 'undefined') {
            CultivARDiagnostics.info('jQuery modal plugin is available');
            
            // Test modal functionality
            try {
                $('#addCultivarModal').modal('hide');
                CultivARDiagnostics.info('jQuery modal hide method works');
            } catch (error) {
                CultivARDiagnostics.error('Error using jQuery modal hide method', {
                    message: error.message,
                    stack: error.stack
                });
            }
        } else {
            CultivARDiagnostics.error('jQuery modal plugin is NOT available');
        }
    } else {
        CultivARDiagnostics.error('jQuery is not loaded');
    }
    
    // Check Bootstrap
    if (typeof bootstrap !== 'undefined') {
        CultivARDiagnostics.info('Bootstrap is loaded');
        
        if (typeof bootstrap.Modal !== 'undefined') {
            CultivARDiagnostics.info('Bootstrap Modal class is available');
            
            // Test Bootstrap modal
            try {
                const modalElement = document.getElementById('addCultivarModal');
                if (modalElement) {
                    const modal = new bootstrap.Modal(modalElement);
                    CultivARDiagnostics.info('Bootstrap Modal instance created successfully');
                } else {
                    CultivARDiagnostics.error('Modal element not found');
                }
            } catch (error) {
                CultivARDiagnostics.error('Error creating Bootstrap Modal instance', {
                    message: error.message,
                    stack: error.stack
                });
            }
        } else {
            CultivARDiagnostics.error('Bootstrap Modal class is NOT available');
        }
    } else {
        CultivARDiagnostics.warn('Bootstrap is not loaded or not available in global scope');
    }
    
    // Check for console errors
    if (console.error.toString().includes('native code')) {
        // Console hasn't been overridden, so we'll override it to catch errors
        const originalConsoleError = console.error;
        console.error = function() {
            CultivARDiagnostics.error('Console error:', Array.from(arguments));
            originalConsoleError.apply(console, arguments);
        };
        CultivARDiagnostics.info('Console error monitoring enabled');
    }
    
    CultivARDiagnostics.info('Diagnostics complete');
}

// Initialize when the page is loaded
if (document.readyState === 'complete') {
    initCultivarsPageDiagnostics();
} else {
    window.addEventListener('load', initCultivarsPageDiagnostics);
}