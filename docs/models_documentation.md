# CultivAR Models Documentation

## Database Models

### User Model
The User model handles authentication and user management.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `username` (String, Unique, Required): User's login name
- `password_hash` (String, Required): Hashed password
- `phone` (String): Phone number for contact
- `email` (String): Email address
- `force_password_change` (Boolean): Force password change on next login
- `is_admin` (Boolean): Admin privileges flag
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Methods:**
- `set_password(password)`: Hash and set password
- `check_password(password)`: Verify password

### Plant Model
The Plant model represents individual cannabis plants.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Plant name
- `description` (Text): Plant description
- `status_id` (Integer, Foreign Key): Growth status reference
- `strain_id` (Integer, Foreign Key): Associated strain
- `zone_id` (Integer, Foreign Key): Growing zone
- `current_day` (Integer): Days since planting
- `current_week` (Integer): Weeks since planting
- `current_height` (String): Current plant height
- `height_date` (DateTime): Height measurement date
- `last_water_date` (DateTime): Last watering date
- `last_feed_date` (DateTime): Last feeding date
- `is_clone` (Boolean): Clone indicator
- `start_dt` (DateTime): Planting date
- `harvest_weight` (Float): Final harvest weight
- `harvest_date` (DateTime): Harvest date
- `cycle_time` (Integer): Growth cycle duration
- `strain_url` (String): Strain information URL
- `est_harvest_date` (DateTime): Estimated harvest date
- `autoflower` (Boolean): Autoflowering type
- `parent_id` (Integer, Foreign Key): Parent plant for clones

**Properties:**
- `status_name`: Current status name
- `strain_name`: Associated strain name
- `breeder_name`: Strain breeder name
- `zone_name`: Growing zone name
- `parent_name`: Parent plant name
- `latest_image`: Most recent plant image

### Strain Model
The Strain model represents cannabis strains.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Strain name
- `breeder_id` (Integer, Foreign Key): Associated breeder
- `indica` (Integer): Indica percentage
- `sativa` (Integer): Sativa percentage
- `autoflower` (Boolean): Autoflowering type
- `description` (Text): Strain description
- `seed_count` (Integer): Available seeds
- `cycle_time` (Integer): Growth cycle duration
- `url` (String): Strain information URL
- `short_description` (Text): Brief description

**Properties:**
- `breeder_name`: Associated breeder name

### Sensor Model
The Sensor model represents environmental sensors.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Sensor name
- `zone_id` (Integer, Foreign Key): Associated zone
- `source` (String): Data source
- `device` (String): Device type
- `type` (String): Sensor type
- `show` (Boolean): Display flag
- `unit` (String): Measurement unit
- `ac_infinity_device_id` (Integer, Foreign Key): AC Infinity device
- `ecowitt_device_id` (Integer, Foreign Key): Ecowitt device
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Properties:**
- `zone_name`: Associated zone name

### Activity Model
The Activity model represents plant care activities.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Activity name

### PlantActivity Model
The PlantActivity model links activities to plants.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `plant_id` (Integer, Foreign Key): Associated plant
- `name` (String, Required): Activity name
- `note` (Text): Activity notes
- `date` (DateTime): Activity date
- `activity_id` (Integer, Foreign Key): Activity type

### Measurement Model
The Measurement model stores plant measurements.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `plant_id` (Integer, Foreign Key): Associated plant
- `metric_id` (Integer, Foreign Key): Measurement type
- `name` (String, Required): Measurement name
- `value` (Float, Required): Measurement value
- `date` (DateTime): Measurement date

### Metric Model
The Metric model defines measurement types.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Metric name
- `unit` (String, Required): Measurement unit

### Breeder Model
The Breeder model represents seed breeders.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Breeder name

### Zone Model
The Zone model represents growing zones.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Zone name

### Status Model
The Status model represents plant growth stages.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `status` (String, Required): Status name
- `plant_id` (Integer, Foreign Key): Associated plant
- `date` (DateTime): Status change date

### PlantImage Model
The PlantImage model stores plant photographs.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `plant_id` (Integer, Foreign Key): Associated plant
- `image_path` (String, Required): Image file path
- `image_description` (Text): Image description
- `image_order` (Integer): Display order
- `image_date` (DateTime): Image capture date
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### SensorData Model
The SensorData model stores sensor readings.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `sensor_id` (Integer, Foreign Key): Associated sensor
- `value` (Float, Required): Sensor reading
- `created_at` (DateTime): Reading timestamp

**Properties:**
- `sensor_name`: Associated sensor name

### Settings Model
The Settings model stores application settings.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `key` (String, Unique, Required): Setting key
- `value` (Text): Setting value
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Stream Model
The Stream model represents video streams.

**Fields:**
- `id` (Integer, Primary Key): Unique identifier
- `name` (String, Required): Stream name
- `url` (String, Required): Stream URL
- `zone_id` (Integer, Foreign Key): Associated zone
- `visible` (Boolean): Visibility flag

**Properties:**
- `zone_name`: Associated zone name
