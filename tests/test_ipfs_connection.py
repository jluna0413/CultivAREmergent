import requests
import sys
import os

# Add app to path
sys.path.append(os.getcwd())
try:
    from app.config import Config
except ImportError:
    # Fallback/Mock config if running outside app context improperly, 
    # but we should rely on PYTHONPATH
    class Config:
        IPFS_API_URL = os.getenv("IPFS_API_URL", "http://ipfs:5001/api/v0")

def test_ipfs():
    # If running inside docker, 'ipfs' hostname should resolve.
    # If running locally without mapping 5001, it might fail or need localhost.
    # We assume usage: docker-compose run ... python tests/test_ipfs_connection.py
    
    url = Config.IPFS_API_URL
    print(f"Testing IPFS connection at {url}...")
    try:
        # Check version or ID (POST is standard for RPC even for reads in some IPFS API versions, but /id is often POST)
        response = requests.post(f"{url}/id")
        response.raise_for_status()
        data = response.json()
        print(f"IPFS ID Check: Success.")
        print(f"Node ID: {data.get('ID')}")
        print(f"Agent Version: {data.get('AgentVersion')}")
        
        # Test Add
        files = {'file': ('test_file.txt', b'Hello CultivAR IPFS')}
        add_response = requests.post(f"{url}/add", files=files)
        add_response.raise_for_status()
        add_data = add_response.json()
        print(f"IPFS Add Check: Success.")
        print(f"Hash (CID): {add_data.get('Hash')}")
        
    except Exception as e:
        print(f"IPFS Connection Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_ipfs()
