// Sensor Settings
.click(function() {
    const row = .closest(\ tr\);
    const sensorName = row.find(\td:first\).text();
    alert(\Edit sensor: \ + sensorName);
});

.click(function() {
    const row = .closest(\tr\);
    const sensorName = row.find(\td:first\).text();
    if (confirm(\Are you sure you want to delete \ + sensorName + \?\)) {
        alert(\Sensor would be deleted in a real application\);
    }
});

.click(function() {
    alert(\Add new sensor form would open here\);
});

.click(function() {
    alert(\Sensor settings saved successfully!\);
});
