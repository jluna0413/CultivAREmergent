#!/usr/bin/env python3
"""
CultivAR Production Security Deployment Script
Handles SSL certificate setup, environment validation, and security hardening
"""

import os
import sys
import subprocess
import secrets
import logging
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography import x509
from cryptography.x509.oid import NameOID
import base64

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityDeployer:
    """Production security deployment handler"""
    
    def __init__(self):
        self.domain = os.getenv("DOMAIN", "cultivar-app.com")
        self.email = os.getenv("LETSENCRYPT_EMAIL", "admin@cultivar-app.com")
        self.ssl_dir = Path("/etc/ssl/cultivar")
        self.cert_path = self.ssl_dir / "cultivar.crt"
        self.key_path = self.ssl_dir / "cultivar.key"
        self.csr_path = self.ssl_dir / "cultivar.csr"
        
    def check_environment(self) -> bool:
        """Check if environment is properly configured"""
        logger.info("Checking production environment configuration...")
        
        required_vars = [
            "JWT_SECRET_KEY",
            "DATABASE_URL", 
            "REDIS_URL",
            "ENVIRONMENT"
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            logger.error(f"Missing required environment variables: {missing}")
            return False
        
        # Validate JWT secret key strength
        jwt_secret = os.getenv("JWT_SECRET_KEY")
        if len(jwt_secret) < 32:
            logger.error("JWT_SECRET_KEY must be at least 32 characters")
            return False
        
        logger.info("Environment configuration validated")
        return True
    
    def generate_jwt_secret(self) -> str:
        """Generate a secure JWT secret key"""
        logger.info("Generating secure JWT secret key...")
        secret = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode()
        logger.info(f"Generated JWT secret: {secret[:20]}...")
        return secret
    
    def setup_ssl_directories(self):
        """Create SSL directories with proper permissions"""
        logger.info("Setting up SSL directories...")
        
        # Create directory
        self.ssl_dir.mkdir(parents=True, exist_ok=True)
        
        # Set restrictive permissions
        os.chmod(self.ssl_dir, 0o700)
        
        logger.info(f"SSL directory created: {self.ssl_dir}")
    
    def generate_self_signed_cert(self):
        """Generate self-signed certificate for development/testing"""
        logger.info("Generating self-signed SSL certificate...")
        
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            
            # Generate certificate
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CA"),
                x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CultivAR"),
                x509.NameAttribute(NameOID.COMMON_NAME, self.domain),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                __import__('datetime').datetime.utcnow()
            ).not_valid_after(
                __import__('datetime').datetime.utcnow() + __import__('datetime').timedelta(days=365)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName(self.domain),
                    x509.DNSName(f"www.{self.domain}"),
                    x509.DNSName(f"api.{self.domain}"),
                ]),
                critical=False,
            ).sign(private_key, SHA256())
            
            # Write certificate
            with open(self.cert_path, "wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            # Write private key
            with open(self.key_path, "wb") as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                ))
            
            # Set proper permissions
            os.chmod(self.cert_path, 0o644)
            os.chmod(self.key_path, 0o600)
            
            logger.info(f"Self-signed certificate generated: {self.cert_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to generate SSL certificate: {e}")
            return False
    
    def setup_letsencrypt(self):
        """Setup Let's Encrypt certificate (requires certbot)"""
        logger.info("Setting up Let's Encrypt certificate...")
        
        try:
            # Check if certbot is installed
            subprocess.run(["certbot", "--version"], check=True, capture_output=True)
            
            # Generate certificate
            cmd = [
                "certbot", "certonly",
                "--standalone",
                "--non-interactive",
                "--agree-tos",
                "--email", self.email,
                "-d", self.domain,
                "-d", f"www.{self.domain}",
                "-d", f"api.{self.domain}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Let's Encrypt certificate obtained successfully")
                # Copy certificates to our location
                certbot_cert = f"/etc/letsencrypt/live/{self.domain}/fullchain.pem"
                certbot_key = f"/etc/letsencrypt/live/{self.domain}/privkey.pem"
                
                if Path(certbot_cert).exists() and Path(certbot_key).exists():
                    subprocess.run(["cp", certbot_cert, self.cert_path], check=True)
                    subprocess.run(["cp", certbot_key, self.key_path], check=True)
                    
                    os.chmod(self.cert_path, 0o644)
                    os.chmod(self.key_path, 0o600)
                    
                    logger.info("Certificates copied to application directory")
                    return True
            else:
                logger.error(f"Certbot failed: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError:
            logger.error("Certbot not found. Install with: sudo apt install certbot")
            return False
        except Exception as e:
            logger.error(f"Let's Encrypt setup failed: {e}")
            return False
    
    def validate_ssl_files(self):
        """Validate SSL certificate and key files"""
        logger.info("Validating SSL files...")
        
        if not self.cert_path.exists():
            logger.error(f"Certificate file not found: {self.cert_path}")
            return False
        
        if not self.key_path.exists():
            logger.error(f"Private key file not found: {self.key_path}")
            return False
        
        # Check file permissions
        cert_stat = os.stat(self.cert_path)
        key_stat = os.stat(self.key_path)
        
        # Certificate should be readable by all (644)
        if oct(cert_stat.st_mode)[-3:] != "644":
            logger.warning(f"Certificate permissions should be 644, got {oct(cert_stat.st_mode)[-3:]}")
        
        # Private key should be restricted (600)
        if oct(key_stat.st_mode)[-3:] != "600":
            logger.warning(f"Private key permissions should be 600, got {oct(key_stat.st_mode)[-3:]}")
        
        logger.info("SSL files validated")
        return True
    
    def test_ssl_configuration(self):
        """Test SSL configuration"""
        logger.info("Testing SSL configuration...")
        
        try:
            # Test certificate
            result = subprocess.run([
                "openssl", "x509", "-in", str(self.cert_path), "-text", "-noout"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error("Invalid certificate format")
                return False
            
            # Test private key
            result = subprocess.run([
                "openssl", "rsa", "-in", str(self.key_path), "-check"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error("Invalid private key format")
                return False
            
            logger.info("SSL configuration test passed")
            return True
            
        except Exception as e:
            logger.error(f"SSL test failed: {e}")
            return False
    
    def create_env_template(self):
        """Create environment template file"""
        logger.info("Creating environment template...")
        
        template_content = f"""# CultivAR Production Environment Template
# Copy this to .env and update with your values

ENVIRONMENT=production
DEBUG=false

# Database
DATABASE_URL=postgresql+asyncpg://cultivar_user:secure_password@localhost:5432/cultivar_db

# JWT Configuration
JWT_SECRET_KEY={self.generate_jwt_secret()}
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379/0

# SSL Configuration
SSL_CERT_PATH={self.cert_path}
SSL_KEY_PATH={self.key_path}
FORCE_HTTPS=true

# CORS
CORS_ALLOWED_ORIGINS=https://{self.domain},https://www.{self.domain},https://api.{self.domain}

# Security Headers
ENABLE_CSP=true
ENABLE_HSTS=true
ENABLE_XFRAME_OPTIONS=true
ENABLE_XCONTENT_TYPE_OPTIONS=true

# Rate Limiting
RATE_LIMIT=100
RATE_WINDOW=60

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=noreply@{self.domain}
SMTP_PASSWORD=your_smtp_password

# Monitoring
SENTRY_DSN=your_sentry_dsn_here
"""
        
        template_path = Path(".env.production.template")
        with open(template_path, "w") as f:
            f.write(template_content)
        
        logger.info(f"Environment template created: {template_path}")
    
    def deploy(self):
        """Run complete security deployment"""
        logger.info("Starting production security deployment...")
        
        # Check environment
        if not self.check_environment():
            logger.error("Environment validation failed")
            return False
        
        # Setup SSL directories
        self.setup_ssl_directories()
        
        # Try Let's Encrypt first, fallback to self-signed
        ssl_success = self.setup_letsencrypt()
        if not ssl_success:
            logger.info("Falling back to self-signed certificate...")
            ssl_success = self.generate_self_signed_cert()
        
        if not ssl_success:
            logger.error("SSL setup failed")
            return False
        
        # Validate SSL files
        if not self.validate_ssl_files():
            logger.error("SSL file validation failed")
            return False
        
        # Test SSL configuration
        if not self.test_ssl_configuration():
            logger.error("SSL configuration test failed")
            return False
        
        # Create environment template
        self.create_env_template()
        
        logger.info("Production security deployment completed successfully!")
        return True

def main():
    """Main deployment function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test-ssl":
            deployer = SecurityDeployer()
            deployer.validate_ssl_files()
            deployer.test_ssl_configuration()
            return
        elif sys.argv[1] == "--gen-secret":
            secret = SecurityDeployer().generate_jwt_secret()
            print(f"JWT_SECRET_KEY={secret}")
            return
    
    # Full deployment
    deployer = SecurityDeployer()
    success = deployer.deploy()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()