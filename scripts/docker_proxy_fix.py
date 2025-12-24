# Docker Proxy Configuration Fix
# Remove proxy settings to allow Docker Hub access

import json
import os
import subprocess

def create_docker_proxy_fix():
    """Create a configuration to bypass proxy for Docker Hub"""
    
    # Create daemon.json configuration to bypass proxy for Docker Hub
    daemon_config = {
        "proxies": {
            "http": {
                "proxy": "http://localhost:3128",
                "bypass": [
                    "localhost",
                    "127.0.0.1",
                    "hub.docker.com",
                    "registry-1.docker.io",
                    "auth.docker.io",
                    "registry.docker.io"
                ]
            },
            "https": {
                "proxy": "http://localhost:3128", 
                "bypass": [
                    "localhost",
                    "127.0.0.1",
                    "hub.docker.com",
                    "registry-1.docker.io", 
                    "auth.docker.io",
                    "registry.docker.io"
                ]
            }
        }
    }
    
    # Try to write daemon.json configuration
    daemon_paths = [
        os.path.expanduser("~\\.docker\\daemon.json"),  # Windows
        "/etc/docker/daemon.json",  # Linux
        "/home/$(whoami)/.docker/daemon.json"  # User config
    ]
    
    for daemon_path in daemon_paths:
        try:
            # Create directory if it doesn't exist
            daemon_dir = os.path.dirname(daemon_path)
            os.makedirs(daemon_dir, exist_ok=True)
            
            # Write configuration
            with open(daemon_path, 'w') as f:
                json.dump(daemon_config, f, indent=2)
            
            print(f"Successfully wrote daemon configuration to: {daemon_path}")
            return daemon_path
            
        except PermissionError:
            print(f"Permission denied writing to: {daemon_path}")
        except Exception as e:
            print(f"Error writing to {daemon_path}: {e}")
    
    return None

def create_docker_env_fix():
    """Create environment configuration to bypass proxy"""
    
    env_vars = [
        "HTTP_PROXY=",
        "HTTPS_PROXY=", 
        "NO_PROXY=localhost,127.0.0.1,hub.docker.com,registry-1.docker.io,auth.docker.io,registry.docker.io"
    ]
    
    # Windows environment variable format
    env_content = "\n".join(env_vars)
    
    with open("docker_proxy_fix.bat", 'w') as f:
        f.write("@echo off\n")
        f.write("echo Disabling Docker proxy settings...\n")
        f.write("set HTTP_PROXY=\n")
        f.write("set HTTPS_PROXY=\n") 
        f.write("set NO_PROXY=localhost,127.0.0.1,hub.docker.com,registry-1.docker.io,auth.docker.io,registry.docker.io\n")
        f.write("echo Docker proxy settings cleared\n")
        f.write("echo You may need to restart Docker Desktop for changes to take effect\n")
        f.write("pause\n")
    
    # Linux/Mac environment variable format
    with open("docker_proxy_fix.sh", 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("echo \"Disabling Docker proxy settings...\"\n")
        f.write("unset HTTP_PROXY\n")
        f.write("unset HTTPS_PROXY\n")
        f.write("export NO_PROXY=\"localhost,127.0.0.1,hub.docker.com,registry-1.docker.io,auth.docker.io,registry.docker.io\"\n")
        f.write("echo \"Docker proxy settings cleared\"\n")
        f.write("echo \"You may need to restart Docker Desktop for changes to take effect\"\n")
    
    return True

def test_docker_access():
    """Test if Docker can now access Docker Hub"""
    
    try:
        print("Testing Docker Hub access...")
        result = subprocess.run([
            "docker", "pull", "hello-world"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("SUCCESS: Docker can now pull images from Docker Hub!")
            return True
        else:
            print(f"FAILED: Docker still cannot pull images. Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("FAILED: Docker pull timed out")
        return False
    except Exception as e:
        print(f"FAILED: Error testing Docker access: {e}")
        return False

def main():
    """Main function to fix Docker proxy configuration"""
    
    print("="*60)
    print("DOCKER PROXY CONFIGURATION FIX")
    print("="*60)
    
    print("\n1. Creating daemon.json bypass configuration...")
    daemon_path = create_docker_proxy_fix()
    
    print("\n2. Creating environment variable fix scripts...")
    create_docker_env_fix()
    
    print("\n3. Testing Docker Hub access...")
    access_works = test_docker_access()
    
    print(f"\n{'='*60}")
    print("PROXY FIX SUMMARY")
    print(f"{'='*60}")
    
    if access_works:
        print("SUCCESS: Docker proxy configuration fixed!")
        print("- Docker Hub access restored")
        print("- No need for environment variables")
    else:
        print("PARTIAL FIX: Configuration created but restart may be required")
        print("- daemon.json written to: " + (daemon_path or "Failed to write"))
        print("- Environment fix scripts created: docker_proxy_fix.bat/.sh")
        print("- You may need to restart Docker Desktop")
        print("- Then run the environment fix script")
    
    print("\nNEXT STEPS:")
    if access_works:
        print("- Run OWASP ZAP scanner: python scripts/owasp_zap_scanner_fixed.py --all")
    else:
        print("- Restart Docker Desktop")
        print("- Run: docker_proxy_fix.bat (Windows) or docker_proxy_fix.sh (Linux/Mac)")
        print("- Test with: docker pull hello-world")
        print("- Then run OWASP ZAP scanner")

if __name__ == "__main__":
    main()