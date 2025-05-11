/**
 * Settings Page JavaScript
 * Handles all settings page functionality
 */

.ready(function() {
    console.log(\ Settings page loaded\);
    
    // Initialize Bootstrap tabs
    .on(\click\, function(e) {
        e.preventDefault();
        .tab(\show\);
    });
    
    // Store active tab in localStorage
    .on(\shown.bs.tab\, function(e) {
        localStorage.setItem(\settingsActiveTab\, .attr(\href\));
    });
    
    // Restore active tab from localStorage
    var activeTab = localStorage.getItem(\settingsActiveTab\);
    if (activeTab) {
        .tab(\show\);
    }
    
    // General Settings Form
    .on(\click\, function() {
        console.log(\Saving general settings\);
        // In a real application, this would save the settings to the server
        alert(\General settings saved successfully!\);
    });
    
    // Sensor Settings
    .on(\click\, function() {
        var sensorName = .closest(\tr\).find(\td:first\).text();
        console.log(\Editing sensor: \ + sensorName);
        alert(\Editing sensor: \ + sensorName);
    });
    
    .on(\click\, function() {
        var sensorName = .closest(\tr\).find(\td:first\).text();
        console.log(\Deleting sensor: \ + sensorName);
        if (confirm(\Are you sure you want to delete \ + sensorName + \?\)) {
            alert(\Sensor would be deleted in a real application\);
        }
    });
    
    .on(\click\, function() {
        console.log(\Adding new sensor\);
        alert(\Add new sensor form would open here\);
    });
    
    .on(\click\, function() {
        console.log(\Saving sensor settings\);
        alert(\Sensor settings saved successfully!\);
    });
    
    // Theme toggle
    .on(\change\, function() {
        if (.is(\:checked\)) {
            .removeClass(\light-theme\).addClass(\dark-theme\);
            localStorage.setItem(\theme\, \dark\);
        } else {
            .removeClass(\dark-theme\).addClass(\light-theme\);
            localStorage.setItem(\theme\, \light\);
        }
    });
    
    // Apply saved theme
    var savedTheme = localStorage.getItem(\theme\);
    if (savedTheme === \light\) {
        .prop(\checked\, false);
        .removeClass(\dark-theme\).addClass(\light-theme\);
    }
});
