# Architecture Overview

Understanding CultivAR's system architecture, design patterns, and component interactions.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CultivAR System                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend Layer                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Web UI        │  │   Mobile UI     │  │   AI Apps   │  │
│  │   (Bootstrap)   │  │   (Responsive)  │  │   (MCP)     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  API Layer                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   REST API      │  │   MCP Server    │  │   WebSocket │  │
│  │   (Flask)       │  │   (AsyncIO)     │  │   (Future)  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Business Logic Layer                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Plant Mgmt    │  │   Sensor Data   │  │   User Mgmt │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Strain DB     │  │   Analytics     │  │   Security  │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Data Access Layer                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   SQLAlchemy    │  │   File Storage  │  │   Cache     │  │
│  │   (ORM)         │  │   (Images)      │  │   (Redis)   │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │   Database      │  │   Web Server    │  │   Monitoring│  │
│  │   (SQLite/PG)   │  │   (Gunicorn)    │  │   (Logs)    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Flask Application (`cultivar_app.py`)

**Purpose**: Main application factory and configuration
**Responsibilities**:
- Application initialization and configuration
- Blueprint registration
- Database setup
- Security configuration (Talisman, rate limiting)
- Session management

**Key Features**:
```python
def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
```

### 2. Database Layer (`app/models/`)

**Architecture**: SQLAlchemy ORM with declarative base
**Database Support**: SQLite (development), PostgreSQL (production)

**Core Models**:
```python
# Base Models (base_models.py)
├── User              # Authentication and user management
├── Plant             # Core plant tracking
├── Strain            # Cannabis strain database
├── Activity          # Plant activities (water, feed, etc.)
├── Measurement       # Plant measurements (height, pH, etc.)
├── PlantImage        # Image uploads and tracking
└── SensorData        # Environmental sensor data

# Sensor Integration Models
├── ACInfinityDevice  # AC Infinity sensor integration
├── EcowittDevice     # Ecowitt weather station integration
└── SystemActivity    # System-level activity logging
```

**Relationships**:
```
User (1) ──────── (N) Plant
Plant (1) ─────── (N) Activity
Plant (1) ─────── (N) Measurement
Plant (1) ─────── (N) PlantImage
Plant (N) ─────── (1) Strain
Sensor (1) ────── (N) SensorData
```

### 3. API Layer (`app/routes/`)

**REST API Structure**:
```
/api/v1/
├── /plants          # Plant CRUD operations
├── /strains         # Strain database
├── /activities      # Plant activities
├── /measurements    # Plant measurements
├── /sensors         # Sensor data and configuration
├── /images          # Image upload and management
├── /users           # User management (admin)
└── /auth            # Authentication endpoints
```

**Authentication Flow**:
```
Request → Rate Limiter → Authentication → Authorization → Controller → Service → Database
```

### 4. MCP Integration (`mcp_server.py`)

**Purpose**: AI/LLM integration via Model Context Protocol
**Architecture**: Async server with tool-based interface

**MCP Tools**:
```python
Available Tools:
├── get_plants           # Query plant data
├── get_plant_details    # Detailed plant information
├── get_strains          # Strain database queries
├── get_environmental_data # Sensor data retrieval
├── add_plant_activity   # Record plant activities
└── get_grow_room_status # Current environment status
```

**Communication Flow**:
```
AI Assistant ←─ MCP Protocol ─→ MCP Server ←─ REST API ─→ CultivAR Database
```

## Design Patterns

### 1. Application Factory Pattern

```python
# Application factory for flexible configuration
def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    return app
```

### 2. Blueprint Pattern

```python
# Modular route organization
from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
```

### 3. Repository Pattern

```python
class PlantRepository:
    @staticmethod
    def get_all_active():
        return Plant.query.filter_by(status='active').all()
    
    @staticmethod
    def get_by_id(plant_id):
        return Plant.query.get_or_404(plant_id)
```

### 4. Service Layer Pattern

```python
class PlantService:
    def __init__(self, plant_repo):
        self.plant_repo = plant_repo
    
    def create_plant(self, plant_data):
        # Business logic
        plant = Plant(**plant_data)
        self.plant_repo.save(plant)
        return plant
```

## Security Architecture

### Authentication & Authorization

```
User Request
     ↓
Rate Limiter (Flask-Limiter)
     ↓
Authentication (Flask-Login)
     ↓
CSRF Protection (Flask-WTF)
     ↓
Authorization Check
     ↓
Business Logic
```

### Security Features

**1. Headers Security (Flask-Talisman)**
```python
Talisman(app, {
    'force_https': True,
    'strict_transport_security': True,
    'content_security_policy': {
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'"
    }
})
```

**2. Rate Limiting**
```python
@limiter.limit("10 per minute")
@app.route('/api/plants')
def get_plants():
    pass
```

**3. Input Validation**
```python
from bleach import clean

def sanitize_input(data):
    return clean(data, tags=[], strip=True)
```

## Data Flow

### 1. Plant Management Flow

```
User Input → Validation → Sanitization → Business Logic → Database → Response
```

### 2. Sensor Data Flow

```
Sensor → API Endpoint → Data Validation → Database Storage → Real-time Updates
```

### 3. MCP Integration Flow

```
AI Assistant → MCP Request → Authentication → Tool Execution → Data Retrieval → Response
```

## Configuration Management

### Environment-Based Configuration

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

## Performance Considerations

### 1. Database Optimization

**Indexing Strategy**:
```sql
CREATE INDEX idx_plant_status ON plant(status_id);
CREATE INDEX idx_activity_plant_date ON plant_activity(plant_id, date);
CREATE INDEX idx_sensor_timestamp ON sensor_data(timestamp);
```

**Query Optimization**:
```python
# Eager loading to avoid N+1 queries
plants = Plant.query.options(
    joinedload(Plant.strain),
    joinedload(Plant.activities)
).all()
```

### 2. Caching Strategy

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@cache.memoize(timeout=300)
def get_strain_statistics():
    return db.session.query(Strain).count()
```

### 3. File Storage

```python
# Efficient image handling
def save_plant_image(file, plant_id):
    filename = f"plant_{plant_id}_{timestamp}.jpg"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    # Generate thumbnail
    image = Image.open(file)
    image.thumbnail((200, 200))
    image.save(os.path.join(app.config['THUMBNAIL_FOLDER'], filename))
```

## Deployment Architecture

### Development
```
SQLite Database + Flask Dev Server + Local File Storage
```

### Production
```
PostgreSQL + Gunicorn + Nginx + Redis Cache + Cloud Storage
```

### Container Deployment
```
Docker Container → Load Balancer → Application Instances → Database Cluster
```

## Extension Points

### 1. Plugin System

```python
class SensorPlugin:
    def connect(self):
        pass
    
    def read_data(self):
        pass
    
    def disconnect(self):
        pass
```

### 2. Custom Analytics

```python
class AnalyticsEngine:
    def calculate_growth_rate(self, plant_id):
        pass
    
    def predict_harvest_date(self, plant_id):
        pass
```

### 3. Integration APIs

```python
class ExternalIntegration:
    def sync_to_external_service(self, data):
        pass
    
    def import_from_external(self, source):
        pass
```

## Testing Architecture

### Unit Tests
```python
# Model tests
def test_plant_creation():
    plant = Plant(name="Test Plant")
    assert plant.name == "Test Plant"

# Service tests
def test_plant_service_create():
    service = PlantService()
    plant = service.create_plant({'name': 'Test'})
    assert plant.id is not None
```

### Integration Tests
```python
# API tests
def test_get_plants_endpoint(client):
    response = client.get('/api/plants')
    assert response.status_code == 200
```

### MCP Tests
```python
# MCP integration tests
async def test_mcp_get_plants():
    result = await mcp_server.call_tool('get_plants', {})
    assert 'plants' in result
```

## 🔗 See Also

- [API Reference](api-reference.md) - Complete API documentation
- [Database Schema](database-schema.md) - Detailed schema reference
- [Security Model](security.md) - Security implementation details
- [Deployment Guide](deployment.md) - Production deployment strategies

---

*This architecture supports the current feature set while remaining extensible for future enhancements.*