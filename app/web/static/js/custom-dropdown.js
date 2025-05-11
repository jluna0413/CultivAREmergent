//
Custom
Dropdown
Implementation

// Custom Dropdown Implementation for Bootstrap
document.addEventListener(\ DOMContentLoaded\, function() {
    console.log(\Custom dropdown script loaded\);
    
    // Initialize custom dropdowns
    var customDropdowns = document.querySelectorAll(\.custom-dropdown-wrapper\);
    
    if (customDropdowns.length > 0) {
        console.log(\Found \ + customDropdowns.length + \ custom dropdowns\);
        
        // Initialize each custom dropdown
        customDropdowns.forEach(function(dropdown) {
            var dropdownToggle = dropdown.querySelector(\.dropdown-toggle\);
            var dropdownMenu = dropdown.querySelector(\.dropdown-menu\);
            var hiddenInput = dropdown.querySelector(\input[type=\hidden\]\);
            var dropdownItems = dropdown.querySelectorAll(\.dropdown-item\);
            
            // Add click event to toggle button
            if (dropdownToggle) {
                dropdownToggle.addEventListener(\click\, function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Toggle the dropdown menu
                    dropdownMenu.classList.toggle(\show\);
                    dropdownToggle.setAttribute(\aria-expanded\, dropdownMenu.classList.contains(\show\));
                    
                    console.log(\Dropdown toggle clicked\);
                });
            }
            
            // Add click event to dropdown items
            if (dropdownItems.length > 0) {
                dropdownItems.forEach(function(item) {
                    item.addEventListener(\click\, function(e) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // Get the value and text
                        var value = this.getAttribute(\data-value\);
                        var text = this.textContent;
                        
                        // Update the hidden input value
                        if (hiddenInput) {
                            hiddenInput.value = value;
                        }
                        
                        // Update the toggle button text
                        if (dropdownToggle) {
                            dropdownToggle.textContent = text;
                        }
                        
                        // Close the dropdown
                        dropdownMenu.classList.remove(\show\);
                        dropdownToggle.setAttribute(\aria-expanded\, \false\);
                        
                        console.log(\Selected value: \ + value);
                    });
                });
            }
            
            // Close dropdown when clicking outside
            document.addEventListener(\click\, function(e) {
                if (!dropdown.contains(e.target)) {
                    dropdownMenu.classList.remove(\show\);
                    if (dropdownToggle) {
                        dropdownToggle.setAttribute(\aria-expanded\, \false\);
                    }
                }
            });
        });
    } else {
        console.log(\No custom dropdowns found\);
    }
});
