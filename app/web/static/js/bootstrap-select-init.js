//
Bootstrap-select
initialization

// Initialize bootstrap-select
.ready(function() {
    // Check if bootstrap-select is loaded
    if ($.fn.selectpicker) {
        console.log(\ Bootstrap-select is loaded\);
        
        // Initialize bootstrap-select
        .selectpicker();
        
        // Log when the timezone is changed
        .on(\changed.bs.select\, function() {
            console.log(\Timezone changed to: \ + .val());
        });
    } else {
        console.log(\Bootstrap-select is not loaded\);
    }
});
