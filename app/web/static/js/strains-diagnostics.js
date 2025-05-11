/**
 * Strains Page Diagnostics
 * Specific diagnostics for the strains page
 */

function initStrainsPageDiagnostics() {
    // Make sure the diagnostics module is loaded
    if (typeof CultivARDiagnostics === 'undefined') {
        console.error('CultivARDiagnostics module not loaded');
        return;
    }
    
    CultivARDiagnostics.info('Initializing strains page diagnostics');
    
    // Check if we're on the strains page
    if (!window.location.pathname.includes('/strains')) {
        CultivARDiagnostics.info('Not on strains page, skipping diagnostics');
        return;
    }
    
    // Enable AJAX monitoring
    CultivARDiagnostics.monitorAjax();
    
    // Track button clicks
    CultivARDiagnostics.trackEvents('.edit-strain', ['click']);
    CultivARDiagnostics.trackEvents('.delete-strain', ['click']);
    
    // Check if buttons exist
    const editButtons = document.querySelectorAll('.edit-strain');
    const deleteButtons = document.querySelectorAll('.delete-strain');
    
    CultivARDiagnostics.info('Strain buttons found', {
        editButtons: editButtons.length,
        deleteButtons: deleteButtons.length
    });
    
    // Check if onclick handlers are properly set
    if (editButtons.length > 0) {
        const firstEditButton = editButtons[0];
        const onclickAttr = firstEditButton.getAttribute('onclick');
        const strainId = firstEditButton.getAttribute('data-strain-id');
        
        CultivARDiagnostics.debug('Edit button inspection', {
            button: firstEditButton.outerHTML,
            onclick: onclickAttr,
            strainId: strainId
        });
        
        // Test if the editStrain function exists
        if (typeof editStrain === 'function') {
            CultivARDiagnostics.info('editStrain function exists');
            
            // Create a wrapper for the editStrain function
            const originalEditStrain = window.editStrain;
            window.editStrain = function(strainId) {
                CultivARDiagnostics.info('editStrain called with ID: ' + strainId);
                try {
                    return originalEditStrain(strainId);
                } catch (error) {
                    CultivARDiagnostics.error('Error in editStrain', {
                        message: error.message,
                        stack: error.stack
                    });
                    throw error;
                }
            };
        } else {
            CultivARDiagnostics.error('editStrain function does not exist');
        }
    }
    
    // Check if deleteStrain function exists and wrap it
    if (typeof deleteStrain === 'function') {
        CultivARDiagnostics.info('deleteStrain function exists');
        
        const originalDeleteStrain = window.deleteStrain;
        window.deleteStrain = function(strainId) {
            CultivARDiagnostics.info('deleteStrain called with ID: ' + strainId);
            try {
                return originalDeleteStrain(strainId);
            } catch (error) {
                CultivARDiagnostics.error('Error in deleteStrain', {
                    message: error.message,
                    stack: error.stack
                });
                throw error;
            }
        };
    } else {
        CultivARDiagnostics.error('deleteStrain function does not exist');
    }
    
    // Check modal functionality
    CultivARDiagnostics.checkElement('#addStrainModal', 'Strain Modal');
    
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
        runStrainsPageDiagnostics();
    });
    
    document.body.appendChild(testButton);
    
    CultivARDiagnostics.info('Strains page diagnostics initialized');
}

function runStrainsPageDiagnostics() {
    CultivARDiagnostics.info('Running strains page diagnostics');
    
    // Show the diagnostics panel
    CultivARDiagnostics.showPanel();
    
    // Check all relevant elements
    CultivARDiagnostics.checkElement('.strain-item', 'Strain Items');
    CultivARDiagnostics.checkElement('.edit-strain', 'Edit Buttons');
    CultivARDiagnostics.checkElement('.delete-strain', 'Delete Buttons');
    CultivARDiagnostics.checkElement('#addStrainModal', 'Add Strain Modal');
    
    // Check if functions exist
    ['editStrain', 'deleteStrain', 'closeModal', 'showAddStrainModal'].forEach(funcName => {
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
                $('#addStrainModal').modal('hide');
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
                const modalElement = document.getElementById('addStrainModal');
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
    initStrainsPageDiagnostics();
} else {
    window.addEventListener('load', initStrainsPageDiagnostics);
}
