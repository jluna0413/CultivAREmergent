# Developer Guide

This guide provides information for developers who want to contribute to the CultivAR project.

## Project Architecture

CultivAR is a Python application built with the Flask web framework. It follows a modular architecture using Flask Blueprints to organize the different parts of the application.

### Key Technologies

*   **Python:** The primary programming language.
*   **Flask:** A lightweight web framework for Python.
*   **SQLAlchemy:** An SQL toolkit and Object-Relational Mapper (ORM) for Python.
*   **Gunicorn:** A Python WSGI HTTP Server for UNIX.
*   **PostgreSQL or SQLite:** The application can be configured to work with either database.
*   **Jinja2:** The templating engine used by Flask.
*   **pytest:** The framework used for testing.

### Directory Structure

```
.
├── app/
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   └── ...
│   ├── config/
│   ├── handlers/
│   ├── models/
│   ├── static/
│   ├── templates/
│   └── ...
├── tests/
├── venv/
├── .env
├── .gitignore
├── cultivar_app.py
└── requirements.txt
```

*   **`app/`**: The main application directory.
    *   **`blueprints/`**: Contains the Flask Blueprints for the different parts of the application.
    *   **`config/`**: Contains the application's configuration.
    *   **`handlers/`**: Contains the business logic for the application.
    *   **`models/`**: Contains the SQLAlchemy database models.
    *   **`static/`**: Contains the static assets (CSS, JavaScript, images).
    *   **`templates/`**: Contains the Jinja2 templates.
*   **`tests/`**: Contains the application's tests.
*   **`cultivar_app.py`**: The main application factory.

## Getting Started with Development

### 1. Set up your environment

Follow the instructions in the [Installation Guide](Installation.md) to set up a local development environment.

### 2. Run the tests

To run the tests, use the following command:

```bash
pytest
```

### 3. Coding Conventions

Please follow the PEP 8 style guide for Python code. We also use `pylint` to enforce coding standards. You can run `pylint` with the following command:

```bash
pylint app/
```

## Contributing

We welcome contributions to the CultivAR project! If you would like to contribute, please follow these steps:

1.  Fork the repository on GitHub.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with a descriptive commit message.
4.  Push your changes to your fork.
5.  Open a pull request to the `main` branch of the main repository.

## Code Samples

### Creating a new Blueprint

To create a new Blueprint, create a new file in the `app/blueprints/` directory. Here is an example of a simple Blueprint:

```python
from flask import Blueprint, render_template

example_bp = Blueprint('example', __name__, template_folder='../templates')

@example_bp.route('/example')
def example_index():
    return render_template('example/index.html')
```

You will also need to register the Blueprint in `cultivar_app.py`:

```python
from app.blueprints.example import example_bp
app.register_blueprint(example_bp)
```

### Creating a new database model

To create a new database model, create a new class in one of the files in the `app/models/` directory. The class should inherit from `db.Model`.

Here is an example of a simple model:

```python
from app.models import db

class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
```
