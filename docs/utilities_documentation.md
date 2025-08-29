# CultivAR Utilities Documentation

## Helper Functions

### Date and Time Utilities

#### format_date(date)
Format a date as a string in MM/DD/YYYY format.

**Parameters:**
- `date` (datetime): The date to format

**Returns:**
- `str`: Formatted date string or empty string if date is None

**Example:**
```python
from app.utils.helpers import format_date
from datetime import datetime

date = datetime(2024, 1, 15)
formatted = format_date(date)  # Returns "01/15/2024"
```

#### format_datetime(date)
Format a datetime as a string in MM/DD/YYYY HH:MM AM/PM format.

**Parameters:**
- `date` (datetime): The datetime to format

**Returns:**
- `str`: Formatted datetime string or empty string if date is None

**Example:**
```python
from app.utils.helpers import format_datetime
from datetime import datetime

dt = datetime(2024, 1, 15, 14, 30)
formatted = format_datetime(dt)  # Returns "01/15/2024 02:30 PM"
```

#### parse_date(date_str)
Parse a date string into a datetime object.

**Parameters:**
- `date_str` (str): The date string to parse

**Returns:**
- `datetime`: Parsed datetime object or None if parsing fails

**Supported Formats:**
- YYYY-MM-DD
- MM/DD/YYYY
- DD/MM/YYYY
- YYYY-MM-DDTHH:MM
- YYYY-MM-DDTHH:MM:SS
- MM/DD/YYYY HH:MM AM/PM

**Example:**
```python
from app.utils.helpers import parse_date

date = parse_date("2024-01-15")  # Returns datetime object
date = parse_date("01/15/2024")  # Also works
```

#### calculate_days_since(date)
Calculate the number of days since a given date.

**Parameters:**
- `date` (datetime): The reference date

**Returns:**
- `int`: Number of days since the date, or None if date is None

**Example:**
```python
from app.utils.helpers import calculate_days_since
from datetime import datetime, timedelta

start_date = datetime.now() - timedelta(days=30)
days = calculate_days_since(start_date)  # Returns 30
```

#### calculate_weeks_since(date)
Calculate the number of weeks since a given date.

**Parameters:**
- `date` (datetime): The reference date

**Returns:**
- `int`: Number of weeks since the date, or None if date is None

**Example:**
```python
from app.utils.helpers import calculate_weeks_since
from datetime import datetime, timedelta

start_date = datetime.now() - timedelta(weeks=4)
weeks = calculate_weeks_since(start_date)  # Returns 4
```

### File and Image Utilities

#### is_valid_image(filename)
Check if a file is a valid image based on its extension.

**Parameters:**
- `filename` (str): The filename to check

**Returns:**
- `bool`: True if the file is a valid image, False otherwise

**Supported Formats:**
- .jpg
- .jpeg
- .png
- .gif

**Example:**
```python
from app.utils.helpers import is_valid_image

is_valid_image("photo.jpg")  # Returns True
is_valid_image("document.pdf")  # Returns False
```

#### get_file_extension(filename)
Get the file extension from a filename.

**Parameters:**
- `filename` (str): The filename to get the extension from

**Returns:**
- `str`: The file extension in lowercase

**Example:**
```python
from app.utils.helpers import get_file_extension

ext = get_file_extension("photo.JPG")  # Returns ".jpg"
ext = get_file_extension("document.PDF")  # Returns ".pdf"
```

### Text Utilities

#### slugify(text)
Convert a string to a URL-friendly slug.

**Parameters:**
- `text` (str): The text to convert

**Returns:**
- `str`: The slugified text

**Process:**
1. Convert to lowercase
2. Remove non-alphanumeric characters (except spaces and hyphens)
3. Replace spaces with hyphens
4. Remove multiple consecutive hyphens
5. Remove leading/trailing hyphens

**Example:**
```python
from app.utils.helpers import slugify

slug = slugify("Blue Dream Strain")  # Returns "blue-dream-strain"
slug = slugify("Plant #1 (Clone)")  # Returns "plant-1-clone"
slug = slugify("  Multiple   Spaces  ")  # Returns "multiple-spaces"
```

### Network Utilities

#### get_client_ip()
Get the client's IP address from the request.

**Returns:**
- `str`: The client's IP address

**Note:**
- Checks for X-Forwarded-For header first (for proxy setups)
- Falls back to request.remote_addr

**Example:**
```python
from app.utils.helpers import get_client_ip

ip = get_client_ip()  # Returns "192.168.1.100"
```

### Plant-Specific Utilities

#### estimate_harvest_date(start_date, cycle_time, autoflower=False)
Estimate the harvest date based on start date and cycle time.

**Parameters:**
- `start_date` (datetime): The plant start date
- `cycle_time` (int): The cycle time in days
- `autoflower` (bool): Whether the plant is an autoflower

**Returns:**
- `datetime`: The estimated harvest date, or None if parameters are invalid

**Logic:**
- For autoflowers: start_date + cycle_time days
- For photoperiod plants: start_date + 28 days (veg) + cycle_time days

**Example:**
```python
from app.utils.helpers import estimate_harvest_date
from datetime import datetime

start_date = datetime(2024, 1, 1)
harvest_date = estimate_harvest_date(start_date, 70, autoflower=True)
# Returns estimated harvest date for autoflower

harvest_date = estimate_harvest_date(start_date, 60, autoflower=False)
# Returns estimated harvest date for photoperiod (28 + 60 days)
```

## Usage Examples

### Working with Dates
```python
from app.utils.helpers import (
    format_date,
    parse_date,
    calculate_days_since,
    calculate_weeks_since
)

# Parse a date string
planting_date = parse_date("2024-01-01")

# Format for display
formatted_date = format_date(planting_date)  # "01/01/2024"

# Calculate growth time
days = calculate_days_since(planting_date)
weeks = calculate_weeks_since(planting_date)

print(f"Plant is {days} days old ({weeks} weeks)")
```

### File Validation
```python
from app.utils.helpers import is_valid_image, get_file_extension

def upload_plant_image(filename):
    if not is_valid_image(filename):
        return {"error": "Invalid image file"}
    
    ext = get_file_extension(filename)
    # Process image upload
    return {"success": True, "extension": ext}
```

### Creating Slugs
```python
from app.utils.helpers import slugify

def create_plant_url(plant_name):
    slug = slugify(plant_name)
    return f"/plants/{slug}"
```

### Estimating Harvest
```python
from app.utils.helpers import estimate_harvest_date
from datetime import datetime

def plan_harvest(plant_data):
    start_date = plant_data['start_date']
    cycle_time = plant_data['cycle_time']
    is_autoflower = plant_data['autoflower']
    
    harvest_date = estimate_harvest_date(start_date, cycle_time, is_autoflower)
    
    if harvest_date:
        return {
            "estimated_harvest": harvest_date,
            "days_remaining": (harvest_date - datetime.now()).days
        }
    return {"error": "Could not estimate harvest date"}
```
