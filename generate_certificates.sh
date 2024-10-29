#!/bin/bash

# This script generates a self-signed SSL certificate and private key,
# storing them in both the "frontend/certificates" and "backend/certificates" directories.
# It performs the following steps:
# 1. Creates "frontend/certificates" and "backend/certificates" directories if they don't already exist.
# 2. Generates a private key (server.key) and encrypts it with AES-256.
# 3. Creates a Certificate Signing Request (CSR) using the private key.
# 4. Generates a self-signed certificate (server.crt) valid for 365 days.
# 5. Cleans up the CSR file, leaving only the .crt and .key files.

# Directory paths for frontend and backend certificates
FRONTEND_CERT_DIR="frontend/certificates"
BACKEND_CERT_DIR="backend/certificates"

# File names for the private key and certificate
KEY_FILE="certificate.key"
CERT_FILE="certificate.crt"

# Create the frontend and backend cert directories if they don't exist
mkdir -p "$FRONTEND_CERT_DIR"
mkdir -p "$BACKEND_CERT_DIR"

# Step 1: Generate a private key with RSA encryption
echo "Generating private key..."
openssl genpkey -algorithm RSA -out "$KEY_FILE" -aes256
if [ $? -ne 0 ]; then
  echo "Failed to generate private key"
  exit 1
fi

# Step 2: Generate a Certificate Signing Request (CSR) using the private key
echo "Generating CSR..."
openssl req -new -key "$KEY_FILE" -out "server.csr"
if [ $? -ne 0 ]; then
  echo "Failed to generate CSR"
  exit 1
fi

# Step 3: Generate a self-signed certificate using the CSR and the private key
echo "Generating self-signed certificate..."
openssl x509 -req -days 365 -in "server.csr" -signkey "$KEY_FILE" -out "$CERT_FILE"
if [ $? -ne 0 ]; then
  echo "Failed to generate certificate"
  exit 1
fi

# Step 4: Copy the .key and .crt files to both frontend and backend cert directories
cp "$KEY_FILE" "$FRONTEND_CERT_DIR/"
cp "$CERT_FILE" "$FRONTEND_CERT_DIR/"
cp "$KEY_FILE" "$BACKEND_CERT_DIR/"
cp "$CERT_FILE" "$BACKEND_CERT_DIR/"

# Step 5: Clean up the CSR file
echo "Cleaning up..."
rm "server.csr"

# Success message
echo "Self-signed certificate and private key have been generated and copied to frontend/cert and backend/cert."

