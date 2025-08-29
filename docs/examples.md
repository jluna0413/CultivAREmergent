# CultivAR API Examples

## Python Examples

### Authentication

#### Login
```python
import requests

# Login
login_data = {
    "username": "john_doe",
    "password": "secure_password123"
}

response = requests.post("http://localhost:5000/login", data=login_data)
session_cookie = response.cookies.get("session")

# Use session cookie for subsequent requests
headers = {"Cookie": f"session={session_cookie}"}
```

#### Signup
```python
import requests

signup_data = {
    "phone": "+1234567890",
    "email": "john@example.com",
    "password": "secure_password123"
}

response = requests.post("http://localhost:5000/signup", data=signup_data)
print(response.text)  # Success message with generated username
```

### Plant Management

#### Get All Plants
```python
import requests

# Assuming you have a session cookie
headers = {"Cookie": "session=your_session_cookie"}

response = requests.get("http://localhost:5000/plants", headers=headers)
plants = response.json()

for plant in plants["plants"]:
    print(f"Plant: {plant['name']} - Status: {plant['status']}")
```

#### Get Specific Plant
```python
import requests

headers = {"Cookie": "session=your_session_cookie"}

response = requests.get("http://localhost:5000/plants/1", headers=headers)
plant = response.json()

print(f"Plant: {plant['name']}")
print(f"Status: {plant['status']}")
print(f"Current Day: {plant['current_day']}")
print(f"Last Watered: {plant['days_since_watering']} days ago")

# Print measurements
for measurement in plant["measurements"]:
    print(f"Measurement: {measurement['name']} = {measurement['value']}")

# Print activities
for activity in plant["activities"]:
    print(f"Activity: {activity['name']} on {activity['date']}")
```

#### Create Plant
```python
import requests

headers = {
    "Cookie": "session=your_session_cookie",
    "Content-Type": "application/json"
}

plant_data = {
    "name": "Blue Dream #1",
    "description": "First Blue Dream plant from seed",
    "strain_id": 1,
    "zone_id": 1,
    "status_id": 2,  # Vegetative
    "is_clone": False,
    "autoflower": False
}

response = requests.post("http://localhost:5000/plants", 
                        json=plant_data, headers=headers)
result = response.json()

if result["success"]:
    print(f"Plant created with ID: {result['plant_id']}")
else:
    print(f"Error: {result['error']}")
```

#### Update Plant
```python
import requests

headers = {
    "Cookie": "session=your_session_cookie",
    "Content-Type": "application/json"
}

update_data = {
    "name": "Blue Dream #1 - Updated",
    "description": "Updated description",
    "current_height": "50cm"
}

response = requests.put("http://localhost:5000/plants/1", 
                       json=update_data, headers=headers)
result = response.json()

if result["success"]:
    print("Plant updated successfully")
else:
    print(f"Error: {result['error']}")
```

#### Delete Plant
```python
import requests

headers = {"Cookie": "session=your_session_cookie"}

response = requests.delete("http://localhost:5000/plants/1", headers=headers)
result = response.json()

if result["success"]:
    print("Plant deleted successfully")
else:
    print(f"Error: {result['error']}")
```

### Sensor Management

#### Get All Sensors
```python
import requests

headers = {"Cookie": "session=your_session_cookie"}

response = requests.get("http://localhost:5000/sensors", headers=headers)
sensors = response.json()

for sensor in sensors["sensors"]:
    print(f"Sensor: {sensor['name']} ({sensor['type']}) - {sensor['unit']}")
```

#### Create Sensor
```python
import requests

headers = {
    "Cookie": "session=your_session_cookie",
    "Content-Type": "application/json"
}

sensor_data = {
    "name": "Humidity Sensor",
    "type": "humidity",
    "unit": "%",
    "zone_id": 1,
    "source": "AC Infinity",
    "device": "Controller 69"
}

response = requests.post("http://localhost:5000/sensors", 
                        json=sensor_data, headers=headers)
result = response.json()

if result["success"]:
    print(f"Sensor created with ID: {result['sensor_id']}")
else:
    print(f"Error: {result['error']}")
```

### Admin Functions

#### Get All Users
```python
import requests

headers = {"Cookie": "session=your_session_cookie"}

response = requests.get("http://localhost:5000/admin/users", headers=headers)
users_data = response.json()

print(f"Total users: {users_data['statistics']['total_users']}")
print(f"Admin users: {users_data['statistics']['admin_users']}")

for user in users_data["users"]:
    print(f"User: {user['username']} ({'Admin' if user['is_admin'] else 'User'})")
```

#### Create User
```python
import requests

headers = {
    "Cookie": "session=your_session_cookie",
    "Content-Type": "application/json"
}

user_data = {
    "username": "new_grower",
    "password": "secure_password123",
    "email": "grower@example.com",
    "phone": "+1234567890",
    "is_admin": False,
    "force_password_change": True
}

response = requests.post("http://localhost:5000/admin/users/create", 
                        json=user_data, headers=headers)
result = response.json()

if result["success"]:
    print(f"User created with ID: {result['user_id']}")
else:
    print(f"Error: {result['error']}")
```

### Export Functions

#### Export Plants CSV
```python
import requests

headers = {"Cookie": "session=your_session_cookie"}

response = requests.get("http://localhost:5000/admin/export/plants/csv", 
                        headers=headers)

if response.status_code == 200:
    with open("plants_export.csv", "wb") as f:
        f.write(response.content)
    print("Plants exported to plants_export.csv")
else:
    print("Export failed")
```

#### Export Plants JSON
```python
import requests
import json

headers = {"Cookie": "session=your_session_cookie"}

response = requests.get("http://localhost:5000/admin/export/plants/json", 
                        headers=headers)

if response.status_code == 200:
    with open("plants_export.json", "wb") as f:
        f.write(response.content)
    print("Plants exported to plants_export.json")
else:
    print("Export failed")
```

## JavaScript Examples

### Authentication

#### Login
```javascript
async function login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('/login', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        console.log('Login successful');
        return true;
    } else {
        console.log('Login failed');
        return false;
    }
}

// Usage
login('john_doe', 'secure_password123');
```

#### Signup
```javascript
async function signup(phone, email, password) {
    const formData = new FormData();
    formData.append('phone', phone);
    formData.append('email', email);
    formData.append('password', password);

    const response = await fetch('/signup', {
        method: 'POST',
        body: formData
    });

    const result = await response.text();
    console.log(result);
}

// Usage
signup('+1234567890', 'john@example.com', 'secure_password123');
```

### Plant Management

#### Get All Plants
```javascript
async function getPlants() {
    const response = await fetch('/plants');
    const data = await response.json();
    
    data.plants.forEach(plant => {
        console.log(`Plant: ${plant.name} - Status: ${plant.status}`);
    });
}

getPlants();
```

#### Create Plant
```javascript
async function createPlant(plantData) {
    const response = await fetch('/plants', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(plantData)
    });

    const result = await response.json();
    
    if (result.success) {
        console.log(`Plant created with ID: ${result.plant_id}`);
    } else {
        console.log(`Error: ${result.error}`);
    }
}

// Usage
const plantData = {
    name: 'Blue Dream #1',
    description: 'First Blue Dream plant',
    strain_id: 1,
    zone_id: 1,
    status_id: 2,
    is_clone: false,
    autoflower: false
};

createPlant(plantData);
```

#### Update Plant
```javascript
async function updatePlant(plantId, updateData) {
    const response = await fetch(`/plants/${plantId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updateData)
    });

    const result = await response.json();
    
    if (result.success) {
        console.log('Plant updated successfully');
    } else {
        console.log(`Error: ${result.error}`);
    }
}

// Usage
const updateData = {
    name: 'Updated Plant Name',
    current_height: '50cm'
};

updatePlant(1, updateData);
```

### Sensor Management

#### Get Sensors
```javascript
async function getSensors() {
    const response = await fetch('/sensors');
    const data = await response.json();
    
    data.sensors.forEach(sensor => {
        console.log(`Sensor: ${sensor.name} (${sensor.type}) - ${sensor.unit}`);
    });
}

getSensors();
```

#### Create Sensor
```javascript
async function createSensor(sensorData) {
    const response = await fetch('/sensors', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(sensorData)
    });

    const result = await response.json();
    
    if (result.success) {
        console.log(`Sensor created with ID: ${result.sensor_id}`);
    } else {
        console.log(`Error: ${result.error}`);
    }
}

// Usage
const sensorData = {
    name: 'Temperature Sensor',
    type: 'temperature',
    unit: '°C',
    zone_id: 1
};

createSensor(sensorData);
```

## Complete Workflow Example

### Plant Lifecycle Management
```python
import requests
from datetime import datetime

class CultivARClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, username, password):
        """Login and establish session"""
        login_data = {"username": username, "password": password}
        response = self.session.post(f"{self.base_url}/login", data=login_data)
        return response.ok
    
    def create_plant(self, name, strain_id, zone_id):
        """Create a new plant"""
        plant_data = {
            "name": name,
            "strain_id": strain_id,
            "zone_id": zone_id,
            "status_id": 1,  # Seedling
            "is_clone": False,
            "autoflower": False
        }
        
        response = self.session.post(f"{self.base_url}/plants", json=plant_data)
        result = response.json()
        
        if result["success"]:
            return result["plant_id"]
        else:
            raise Exception(result["error"])
    
    def add_measurement(self, plant_id, metric_name, value):
        """Add a measurement to a plant"""
        measurement_data = {
            "plant_id": plant_id,
            "name": metric_name,
            "value": value,
            "metric_id": 1  # Height
        }
        
        response = self.session.post(f"{self.base_url}/measurements", json=measurement_data)
        result = response.json()
        
        if not result["success"]:
            raise Exception(result["error"])
    
    def add_activity(self, plant_id, activity_name, note=""):
        """Add an activity to a plant"""
        activity_data = {
            "plant_id": plant_id,
            "name": activity_name,
            "note": note,
            "activity_id": 1  # Water
        }
        
        response = self.session.post(f"{self.base_url}/activities", json=activity_data)
        result = response.json()
        
        if not result["success"]:
            raise Exception(result["error"])
    
    def get_plant_status(self, plant_id):
        """Get current plant status"""
        response = self.session.get(f"{self.base_url}/plants/{plant_id}")
        return response.json()

# Usage example
def main():
    client = CultivARClient()
    
    # Login
    if not client.login("john_doe", "secure_password123"):
        print("Login failed")
        return
    
    try:
        # Create a new plant
        plant_id = client.create_plant("Blue Dream #1", strain_id=1, zone_id=1)
        print(f"Created plant with ID: {plant_id}")
        
        # Add initial measurement
        client.add_measurement(plant_id, "Initial Height", 5.0)
        print("Added initial measurement")
        
        # Add watering activity
        client.add_activity(plant_id, "Initial Watering", "First watering after planting")
        print("Added watering activity")
        
        # Check plant status
        plant = client.get_plant_status(plant_id)
        print(f"Plant: {plant['name']}")
        print(f"Status: {plant['status']}")
        print(f"Current Day: {plant['current_day']}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Error Handling Examples

### Python Error Handling
```python
import requests

def safe_api_call(func, *args, **kwargs):
    """Wrapper for safe API calls with error handling"""
    try:
        response = func(*args, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except ValueError as e:
        print(f"JSON parsing error: {e}")
        return None

# Usage
headers = {"Cookie": "session=your_session_cookie"}

# Safe API call
result = safe_api_call(requests.get, "http://localhost:5000/plants", headers=headers)
if result:
    print("API call successful")
else:
    print("API call failed")
```

### JavaScript Error Handling
```javascript
async function safeApiCall(url, options = {}) {
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        return null;
    }
}

// Usage
const result = await safeApiCall('/plants');
if (result) {
    console.log('API call successful');
} else {
    console.log('API call failed');
}
```
