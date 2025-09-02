# SSL/TLS Setup Guide for CultivAR Application

This guide covers how to configure SSL/TLS certificates for secure HTTPS connections in both development and production environments.

## Quick Start

### Development Environment
For development, use self-signed certificates:

```bash
# Create development certificates
./scripts/setup_ssl.sh dev

# Set environment variables
export SSL_ENABLED=true
export SSL_CERT_PATH=$(pwd)/ssl/server.crt
export SSL_KEY_PATH=$(pwd)/ssl/server.key

# Run the application
python cultivar_app.py
```

### Production Environment
For production, use Let's Encrypt certificates:

```bash
# Setup production certificates
sudo ./scripts/setup_ssl.sh prod

# Set environment variables (adjust paths based on certbot output)
export SSL_ENABLED=true
export SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
export SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SSL_ENABLED` | Enable/disable SSL | `false` |
| `SSL_CERT_PATH` | Path to SSL certificate | `/path/to/certificate.pem` |
| `SSL_KEY_PATH` | Path to SSL private key | `/path/to/private_key.pem` |

## Security Features Configured

### Session Security
- **HttpOnly**: Session cookies are not accessible via JavaScript
- **Secure**: Session cookies only sent over HTTPS (in production)
- **SameSite**: Set to 'Strict' to prevent CSRF attacks
- **Session Regeneration**: New session ID generated after login/logout

### HTTPS Enforcement
- **Force HTTPS**: All HTTP requests redirected to HTTPS in production
- **HSTS**: HTTP Strict Transport Security enabled in production
- **SSL Context**: Automatic SSL context creation when certificates are available

### Security Headers (via Flask-Talisman)
- Content Security Policy
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin

## Docker Deployment

### docker-compose.yml Configuration
```yaml
version: '3.8'
services:
  cultivar:
    build: .
    ports:
      - "443:5000"  # HTTPS port
    environment:
      - SSL_ENABLED=true
      - SSL_CERT_PATH=/etc/ssl/certs/cultivar.crt
      - SSL_KEY_PATH=/etc/ssl/private/cultivar.key
      - DEBUG=false
    volumes:
      - ./ssl:/etc/ssl/certs:ro
      - ./ssl:/etc/ssl/private:ro
    restart: unless-stopped
```

### Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Production Deployment Options

### Option 1: Direct Flask with SSL
```bash
export SSL_ENABLED=true
export SSL_CERT_PATH=/etc/letsencrypt/live/yourdomain.com/fullchain.pem
export SSL_KEY_PATH=/etc/letsencrypt/live/yourdomain.com/privkey.pem
python cultivar_app.py
```

### Option 2: Gunicorn with SSL
```bash
gunicorn --certfile=/etc/letsencrypt/live/yourdomain.com/fullchain.pem \
         --keyfile=/etc/letsencrypt/live/yourdomain.com/privkey.pem \
         --bind 0.0.0.0:443 \
         cultivar_app:create_app()
```

### Option 3: Nginx + Gunicorn
Most secure production setup:
1. Nginx handles SSL termination
2. Gunicorn runs the Flask application
3. Certificate renewal handled by certbot

## Certificate Renewal

### Let's Encrypt Auto-Renewal
```bash
# Add to crontab for weekly renewal checks
0 12 * * 1 certbot renew
```

### Manual Renewal
```bash
sudo certbot renew
sudo systemctl restart nginx  # or gunicorn/flask service
```

## Security Considerations

### Certificate Pinning
Consider implementing HPKP (HTTP Public Key Pinning) for additional security:

```python
# In cultivar_app.py
@app.after_request
def set_security_headers(response):
    response.headers['Public-Key-Pins'] = 'pin-sha256="..."'
    return response
```

### SSL/TLS Best Practices
- Use strong cipher suites (configured automatically)
- Enable HSTS preload
- Regular certificate renewal
- Monitor SSL/TLS configuration with tools like `sslscan`

## Troubleshooting

### Common Issues

**SSL Connection Error**
```bash
# Check if paths exist
ls -la $SSL_CERT_PATH $SSL_KEY_PATH

# Verify certificate
openssl x509 -in $SSL_CERT_PATH -text -noout
```

**Mixed Content Issues**
- Ensure all assets are served over HTTPS
- Check for hardcoded HTTP URLs in templates

**Browser Warnings**
- Self-signed certificates cause browser warnings (expected in development)
- Check certificate validity dates
- Verify certificate authority

### Debug Commands

```bash
# Check SSL certificate
openssl s_client -connect localhost:5000 -servername localhost

# Check certificate validity
openssl x509 -in server.crt -text -noout | grep -A 2 "Validity"
```

## References

- [Flask SSL Documentation](https://flask.palletsprojects.com/en/2.0.x/deploying/ssl/)
- [Let's Encrypt Documentation](https://certbot.eff.org/docs/)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)