#!/bin/bash

# SSL/TLS Certificate Setup Script for CultivAR Application
# This script helps set up SSL certificates for development and production

set -e

echo "🔒 CultivAR SSL/TLS Certificate Setup"
echo "====================================="

# Function to create development certificates
create_dev_certificates() {
    echo "Creating development self-signed certificates..."
    mkdir -p ssl

    # Create private key
    openssl genrsa -out ssl/server.key 2048

    # Create certificate signing request
    cat > ssl/server.csr.cnf << EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = Development
L = Development
O = Development
OU = Development
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
IP.1 = 127.0.0.1
EOF

    # Create self-signed certificate (valid for 365 days)
    openssl req -new -x509 -key ssl/server.key -out ssl/server.crt -days 365 -config ssl/server.csr.cnf -sha256

    echo "✅ Development certificates created in ssl/ directory"
    echo "   - Private key: ssl/server.key"
    echo "   - Certificate: ssl/server.crt"
    echo ""
    echo "To use development certificates:"
    echo "export SSL_ENABLED=true"
    echo "export SSL_CERT_PATH=\$(pwd)/ssl/server.crt"
    echo "export SSL_KEY_PATH=\$(pwd)/ssl/server.key"
}

# Function to setup production certificates with Let's Encrypt (example)
setup_prod_certbot() {
    echo "Setting up Let's Encrypt certificates for production..."

    if ! command -v certbot &> /dev/null; then
        echo "Certbot not found. Installing..."
        # For Ubuntu/Debian
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y certbot
        # For CentOS/RHEL
        elif command -v yum &> /dev/null; then
            sudo yum install -y certbot
        else
            echo "❌ Unable to install certbot. Please install manually for your distribution."
            exit 1
        fi
    fi

    read -p "Enter your domain name: " domain
    if [ -z "$domain" ]; then
        echo "❌ Domain name is required for production certificates."
        exit 1
    fi

    echo "Obtaining SSL certificate for $domain..."
    sudo certbot certonly --standalone -d "$domain"

    cert_path="/etc/letsencrypt/live/$domain/fullchain.pem"
    key_path="/etc/letsencrypt/live/$domain/privkey.pem"

    echo "✅ Production certificates obtained from Let's Encrypt"
    echo "   - Certificate: $cert_path"
    echo "   - Private key: $key_path"
    echo ""
    echo "To use production certificates:"
    echo "export SSL_ENABLED=true"
    echo "export SSL_CERT_PATH=$cert_path"
    echo "export SSL_KEY_PATH=$key_path"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [option]"
    echo ""
    echo "Options:"
    echo "  dev       Create development self-signed certificates"
    echo "  prod      Setup production certificates with Let's Encrypt"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev    # Create development certificates"
    echo "  $0 prod   # Setup production certificates"
}

# Main execution
case "$1" in
    "dev")
        create_dev_certificates
        ;;
    "prod")
        if [ "$EUID" -eq 0 ]; then
            echo "❌ Please run as regular user (not root) for certbot setup."
            exit 1
        fi
        setup_prod_certbot
        ;;
    "help"|"-h"|"--help"|"")
        show_usage
        ;;
    *)
        echo "❌ Invalid option: $1"
        show_usage
        exit 1
        ;;
esac

echo ""
echo "🔄 Remember to set SSL environment variables in your production configuration!"
echo "   For Docker: Set them in your docker-compose.yml"
echo "   For direct deployment: Set them in your environment before starting the app"