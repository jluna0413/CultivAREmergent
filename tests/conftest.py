from pathlib import Path
from dotenv import load_dotenv

# Load test env before any app import
env_path = Path(__file__).parent / ".env.test"
load_dotenv(dotenv_path=env_path)