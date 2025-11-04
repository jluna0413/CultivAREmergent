# CultivAR User Documentation

## Introduction

CultivAR is a self-hosted cannabis grow journal application. It allows you to track your plants, cultivars, and environmental data.

## Getting Started

### Logging In

1. Access the application at http://localhost:5000
2. Use the default credentials:
   - Username: admin
   - Password: isley
3. You will be prompted to change your password on first login.

### Dashboard

The dashboard provides an overview of your active plants and environmental data.

- **Active Plants**: Shows a list of all your living plants with their current status.
- **Environmental Data**: Displays the latest readings from your sensors.
- **Quick Actions**: Provides shortcuts to common actions.

### Plants

The Plants page allows you to manage your plants.

#### Adding a Plant

1. Click the "Add Plant" button.
2. Fill in the plant details:
   - Name: A name for your plant.
   - Description: Optional description.
   - Status: The current growth stage (Seedling, Vegetative, Flowering, etc.).
   - Cultivar: The cannabis cultivar.
   - Zone: The growing zone.
   - Is Clone: Check if the plant is a clone.
   - Parent: If it's a clone, select the parent plant.
3. Click "Save" to create the plant.

#### Plant Details

Click on a plant to view its details. From here, you can:

- Update plant information
- Record activities (watering, feeding, etc.)
- Take measurements (height, pH, etc.)
- Upload images
- View growth history

### Strains

The Cultivars page allows you to manage your cannabis cultivars.

#### Adding a Strain

1. Click the "Add Strain" button.
2. Fill in the strain details:
   - Name: The strain name.
   - Breeder: The breeder or seed bank.
   - Indica/Sativa: The indica/sativa percentages.
   - Autoflower: Check if it's an autoflowering strain.
   - Description: Strain description.
   - Seed Count: Number of seeds you have.
   - Cycle Time: Expected flowering time in days.
   - URL: Optional link to strain information.
3. Click "Save" to create the strain.

### Sensors

The Sensors page allows you to manage your environmental sensors.

#### Supported Sensor Systems

- AC Infinity
- Ecowitt

#### Configuring Sensors

1. Go to the Settings page.
2. Enable the sensor system you want to use.
3. Configure the connection details.
4. Click "Save Settings".
5. Go to the Sensors page and click "Scan for Sensors".

#### Viewing Sensor Data

Click on a sensor to view its historical data as a graph.

### Settings

The Settings page allows you to configure the application.

- **AC Infinity**: Enable/disable AC Infinity integration.
- **Ecowitt**: Enable/disable Ecowitt integration and set the server address.
- **Polling Interval**: How often to collect sensor data (in seconds).
- **Guest Mode**: Enable/disable guest access.
- **Stream Grabbing**: Enable/disable automatic image capture from video streams.

## Tips and Tricks

- **Watering Schedule**: Use the dashboard to quickly see which plants need watering.
- **Strain Selection**: Use the seed count to keep track of which strains you have available.
- **Environmental Data**: Monitor temperature and humidity trends to optimize growing conditions.
- **Plant Images**: Take regular photos to track plant development over time.
