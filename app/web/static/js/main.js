/**
 * Main JavaScript file for CultivAR
 * Cannabis Grow Journal by Eye Heart Hemp
 */

// Document ready function
$(document).ready(function() {

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Initialize popovers
    $('[data-toggle="popover"]').popover();

    // Initialize sidebar toggle
    initSidebarToggle();

    // Check screen size on load
    checkScreenSize();

    // Initialize sidebar dropdown menus
    initSidebarDropdowns();

    // Ensure hamburger menu is clickable
    $('#hamburger-menu').on('click', function(e) {
        console.log('Hamburger clicked directly'); // Debug log
        e.stopPropagation();
        e.preventDefault();
        $('.app-container').toggleClass('sidebar-collapsed');
        $('body').toggleClass('sidebar-open');
    });

    // Apply saved theme
    applyTheme();

    // Modal centering is now handled in plants.html to avoid conflicts
    // Removed duplicate modal initialization

    // Flash messages auto-close
    $('.alert-dismissible').each(function() {
        const $alert = $(this);
        setTimeout(function() {
            $alert.alert('close');
        }, 5000);
    });

    // Confirm delete actions
    $('.confirm-delete').click(function(e) {
        if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
            e.preventDefault();
        }
    });

    // Plant form handling
    if ($('#plant-form').length) {
        initPlantForm();
    }

    // Strain form handling
    if ($('#strain-form').length) {
        initStrainForm();
    }

    // Sensor graph handling
    if ($('#sensor-graph').length) {
        initSensorGraph();
    }

    // Initialize date inputs (HTML5 date inputs instead of jQuery datepicker)
    $('.datepicker').each(function() {
        const $input = $(this);
        if ($input.attr('type') !== 'date') {
            $input.attr('type', 'date');
        }
    });

    // Initialize select2 dropdowns if available
    if ($.fn.select2 && $('.select2').length) {
        $('.select2').select2({
            theme: 'bootstrap4',
            width: '100%'
        });
    }
});

/**
 * Initialize the plant form
 */
function initPlantForm() {
    // Toggle clone parent field
    $('#is_clone').change(function() {
        if ($(this).is(':checked')) {
            $('#parent_id_group').show();
        } else {
            $('#parent_id_group').hide();
        }
    });

    // Initialize date inputs (HTML5 instead of jQuery datepicker)
    $('.datepicker').each(function() {
        const $input = $(this);
        if ($input.attr('type') !== 'date') {
            $input.attr('type', 'date');
        }
    });

    // Handle form submission
    $('#plant-form').submit(function(e) {
        e.preventDefault();

        const formData = $(this).serialize();

        $.ajax({
            url: '/plant',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    window.location.href = '/plant/' + response.plant_id;
                } else {
                    alert('Error: ' + response.error);
                }
            },
            error: function() {
                alert('An error occurred while saving the plant.');
            }
        });
    });
}

/**
 * Initialize the strain form
 */
function initStrainForm() {
    // Handle form submission
    $('#strain-form').submit(function(e) {
        e.preventDefault();

        const formData = $(this).serialize();

        $.ajax({
            url: '/strains',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (response.success) {
                    window.location.href = '/strain/' + response.strain_id;
                } else {
                    alert('Error: ' + response.error);
                }
            },
            error: function() {
                alert('An error occurred while saving the strain.');
            }
        });
    });
}

/**
 * Initialize the sensor graph
 */
function initSensorGraph() {
    const sensorId = $('#sensor-graph').data('sensor-id');
    const ctx = document.getElementById('sensor-chart').getContext('2d');

    // Default to last 7 days
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 7);

    // Format dates for API
    const formattedStartDate = formatDate(startDate);
    const formattedEndDate = formatDate(endDate);

    // Load sensor data
    $.get('/sensorData', {
        sensor_id: sensorId,
        start_date: formattedStartDate,
        end_date: formattedEndDate
    }, function(response) {
        if (response.data && response.data.length > 0) {
            const labels = response.data.map(item => new Date(item.date));
            const values = response.data.map(item => item.value);

            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: response.sensor.name,
                        data: values,
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        borderWidth: 2,
                        pointRadius: 3,
                        pointBackgroundColor: '#3498db',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'day',
                                displayFormats: {
                                    day: 'MMM d'
                                }
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: response.sensor.unit
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `${context.dataset.label}: ${context.raw} ${response.sensor.unit}`;
                                }
                            }
                        }
                    }
                }
            });

            // Date range selector
            $('#date-range').change(function() {
                const range = $(this).val();
                let newStartDate = new Date();

                switch (range) {
                    case '1d':
                        newStartDate.setDate(newStartDate.getDate() - 1);
                        break;
                    case '7d':
                        newStartDate.setDate(newStartDate.getDate() - 7);
                        break;
                    case '30d':
                        newStartDate.setDate(newStartDate.getDate() - 30);
                        break;
                    case 'all':
                        newStartDate = null;
                        break;
                }

                updateChart(chart, sensorId, newStartDate, new Date());
            });
        } else {
            $('#sensor-chart-container').html('<p>No data available for this sensor.</p>');
        }
    });
}

/**
 * Update the sensor chart with new data
 */
function updateChart(chart, sensorId, startDate, endDate) {
    // Format dates for API
    const formattedStartDate = startDate ? formatDate(startDate) : null;
    const formattedEndDate = formatDate(endDate);

    // Load sensor data
    $.get('/sensorData', {
        sensor_id: sensorId,
        start_date: formattedStartDate,
        end_date: formattedEndDate
    }, function(response) {
        if (response.data && response.data.length > 0) {
            chart.data.labels = response.data.map(item => new Date(item.date));
            chart.data.datasets[0].data = response.data.map(item => item.value);
            chart.update();
        }
    });
}

/**
 * Format a date as YYYY-MM-DD
 */
function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

/**
 * Initialize sidebar toggle functionality
 */
function initSidebarToggle() {
    // Toggle sidebar on menu button click
    $('#menu-toggle, #hamburger-menu').on('click', function(e) {
        e.stopPropagation(); // Prevent event bubbling
        e.preventDefault(); // Prevent default action
        $('.app-container').toggleClass('sidebar-collapsed');
        $('body').toggleClass('sidebar-open');
    });

    // Close sidebar when close button is clicked
    $('#sidebar-close').on('click', function(e) {
        e.stopPropagation(); // Prevent event bubbling
        $('.app-container').addClass('sidebar-collapsed');
        $('body').removeClass('sidebar-open');
    });

    // Close sidebar when clicking on the overlay
    $('.sidebar-overlay').on('click', function(e) {
        e.stopPropagation(); // Prevent event bubbling
        $('.app-container').addClass('sidebar-collapsed');
        $('body').removeClass('sidebar-open');
    });

    // Prevent clicks inside sidebar from closing it
    $('.sidebar').on('click', function(e) {
        e.stopPropagation(); // Prevent event bubbling
    });

    // Close sidebar when clicking outside (desktop vs mobile behavior)
    $(document).on('click', function(e) {
        // Don't process click if it's on a sidebar toggle button
        if ($(e.target).closest('#menu-toggle, #hamburger-menu, .hamburger-menu').length) {
            return; // Let toggle buttons work normally
        }
        
        // Don't process click if it's on sidebar elements or close button
        if ($(e.target).closest('.sidebar, #sidebar-close').length) {
            return; // Let sidebar interactions work normally
        }
        
        // Don't process click if it's on form elements or UI components
        if ($(e.target).closest('.form-control, .form-group, .form-check, .btn, .modal, .dropdown, .popover, .tooltip, select, textarea, input[type="date"], input[type="text"], input[type="checkbox"], input[type="radio"], label').length) {
            return; // Skip form and UI element clicks
        }
        
        // Only close sidebar if we're in mobile view and clicking outside
        if (window.innerWidth < 768) {
            console.log('SIDEBAR DEBUG: Mobile view - closing sidebar on outside click');
            $('.app-container').addClass('sidebar-collapsed');
            $('body').removeClass('sidebar-open');
        }
        // Desktop view: Don't auto-close sidebar on outside click
    });

    // Add window resize listener
    $(window).on('resize', function() {
        checkScreenSize();
    });
}

/**
 * Check screen size and adjust UI accordingly
 */
function checkScreenSize() {
    if (window.innerWidth < 768) {
        // Mobile view - collapse sidebar by default
        $('.app-container').addClass('sidebar-collapsed');
        $('body').removeClass('sidebar-open');
    } else {
        // Desktop view - expand sidebar by default
        $('.app-container').removeClass('sidebar-collapsed');
        $('body').removeClass('sidebar-open');
    }
}

/**
 * Initialize sidebar dropdown menus
 */
function initSidebarDropdowns() {
    // Handle submenu toggle clicks
    $('.submenu-toggle').off('click').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        const target = $(this).data('target');
        console.log('Submenu toggle clicked, target:', target);

        // Normalize URL if this element has href or data-href
        const href = $(this).attr('href') || $(this).data('href');
        if (href) {
            const normalizedHref = normalizeUrl(href);
            console.log('NAVIGATION DEBUG: Original URL:', href, 'Normalized URL:', normalizedHref);

            // Redirect to normalized URL
            window.location.href = normalizedHref;
            return;
        }

        // Get the target submenu
        const $targetSubmenu = $(target);

        // Toggle the submenu
        if ($targetSubmenu.hasClass('show')) {
            $targetSubmenu.removeClass('show');
            $(this).attr('aria-expanded', 'false');
        } else {
            $targetSubmenu.addClass('show');
            $(this).attr('aria-expanded', 'true');
        }
    });

    // Handle submenu item clicks
    $('.submenu-item').off('click').on('click', function(e) {
        e.stopPropagation();

        const href = $(this).attr('href') || $(this).data('href');
        if (href) {
            const normalizedHref = normalizeUrl(href);
            console.log('NAVIGATION DEBUG: Submenu item clicked, Original URL:', href, 'Normalized URL:', normalizedHref);
            window.location.href = normalizedHref;
        }
    });
}

/**
 * Normalize a URL to prevent double slashes and other URL issues
 */
function normalizeUrl(url) {
    if (!url || typeof url !== 'string') {
        console.warn('NAVIGATION DEBUG: normalizeUrl received invalid URL:', url);
        return url;
    }

    // Remove protocol and domain to focus on path
    const urlObj = new URL(url, window.location.origin);
    let path = urlObj.pathname + urlObj.search + urlObj.hash;

    // Replace multiple consecutive slashes with single slash (except after protocol)
    path = path.replace(/\/+/g, '/');

    // Ensure path starts with single slash
    if (!path.startsWith('/')) {
        path = '/' + path;
    }

    // Reconstruct URL with normalized path
    const normalizedUrl = path + urlObj.search + urlObj.hash;

    console.log('NAVIGATION DEBUG: URL normalization complete:', {
        original: url,
        normalized: normalizedUrl,
        path: path
    });

    return normalizedUrl;
}

/**
 * Apply saved theme preference
 */
function applyTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        $('body').addClass('light-theme').removeClass('dark-theme');
    } else {
        $('body').addClass('dark-theme').removeClass('light-theme');
    }
}

/**
 * Show a toast notification
 */
function showToast(message, type = 'success') {
    // Create toast container if it doesn't exist
    if (!$('#toast-container').length) {
        $('body').append('<div id="toast-container" class="toast-container"></div>');
    }

    // Create unique ID for this toast
    const toastId = 'toast-' + Date.now();

    // Create toast HTML
    const toast = `
        <div id="${toastId}" class="toast toast-${type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <strong class="mr-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    // Add toast to container
    $('#toast-container').append(toast);

    // Show toast
    $(`#${toastId}`).toast({
        delay: 5000,
        autohide: true
    }).toast('show');

    // Remove toast after it's hidden
    $(`#${toastId}`).on('hidden.bs.toast', function() {
        $(this).remove();
    });
}
