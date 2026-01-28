#!/bin/bash
# SSL Certificate Installation Script
# Run this ONLY after DNS points to 34.100.223.247

echo "============================================"
echo "tstr.directory - SSL Certificate Installation"
echo "============================================"
echo ""

# Check if domain resolves correctly
echo "Step 1: Verifying DNS resolution..."
RESOLVED_IP=$(dig +short tstr.directory @8.8.8.8 | head -n 1)
EXPECTED_IP="34.100.223.247"

if [ "$RESOLVED_IP" != "$EXPECTED_IP" ]; then
    echo "❌ ERROR: DNS not yet updated"
    echo "Current IP: $RESOLVED_IP"
    echo "Expected IP: $EXPECTED_IP"
    echo ""
    echo "Please wait for DNS propagation and try again."
    echo "Check status: nslookup tstr.directory"
    exit 1
fi

echo "✅ DNS correctly points to $EXPECTED_IP"
echo ""

# Install Certbot if not already installed
echo "Step 2: Checking Certbot installation..."
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    sudo apt-get update
    sudo apt-get install -y certbot python3-certbot-apache
fi
echo "✅ Certbot ready"
echo ""

# Stop Apache temporarily
echo "Step 3: Preparing web server..."
sudo systemctl stop apache2
echo "✅ Web server prepared"
echo ""

# Obtain SSL certificate
echo "Step 4: Obtaining SSL certificate from Let's Encrypt..."
sudo certbot certonly --standalone \
    -d tstr.directory \
    -d www.tstr.directory \
    --agree-tos \
    --email tstr.directory1@gmail.com \
    --non-interactive \
    --preferred-challenges http

if [ $? -eq 0 ]; then
    echo "✅ SSL certificate obtained successfully!"
else
    echo "❌ Failed to obtain certificate"
    sudo systemctl start apache2
    exit 1
fi
echo ""

# Configure Apache for HTTPS
echo "Step 5: Configuring Apache for HTTPS..."

# Enable required modules
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod headers

# Create HTTPS virtual host
cat > /tmp/tstr-ssl.conf << 'EOF'
<VirtualHost *:443>
    ServerName tstr.directory
    ServerAlias www.tstr.directory
    
    DocumentRoot /var/www/html
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/tstr.directory/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/tstr.directory/privkey.pem
    
    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    
    <Directory /var/www/html>
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/tstr-ssl-error.log
    CustomLog ${APACHE_LOG_DIR}/tstr-ssl-access.log combined
</VirtualHost>

# Redirect HTTP to HTTPS
<VirtualHost *:80>
    ServerName tstr.directory
    ServerAlias www.tstr.directory
    
    RewriteEngine On
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
</VirtualHost>
EOF

sudo mv /tmp/tstr-ssl.conf /etc/apache2/sites-available/tstr-ssl.conf
sudo a2ensite tstr-ssl.conf
echo "✅ Apache configured"
echo ""

# Update WordPress URLs
echo "Step 6: Updating WordPress URLs..."
sudo wp option update siteurl 'https://tstr.directory' --allow-root --path=/var/www/html
sudo wp option update home 'https://tstr.directory' --allow-root --path=/var/www/html
echo "✅ WordPress URLs updated"
echo ""

# Start Apache
echo "Step 7: Starting web server..."
sudo systemctl start apache2
sudo systemctl reload apache2
echo "✅ Web server running"
echo ""

# Set up auto-renewal
echo "Step 8: Configuring automatic renewal..."
sudo certbot renew --dry-run
echo "✅ Auto-renewal configured"
echo ""

echo "============================================"
echo "✅ SSL INSTALLATION COMPLETE!"
echo "============================================"
echo ""
echo "Your site is now available at:"
echo "  🔒 https://tstr.directory"
echo "  🔒 https://www.tstr.directory"
echo ""
echo "Certificate details:"
echo "  Issuer: Let's Encrypt"
echo "  Valid for: 90 days"
echo "  Auto-renewal: Enabled"
echo ""
echo "Next steps:"
echo "  1. Test: Open https://tstr.directory in browser"
echo "  2. Verify: Green padlock should appear"
echo "  3. Update: All marketing materials to use https://"
echo ""
echo "Certificate will auto-renew 30 days before expiry."
echo "============================================"
