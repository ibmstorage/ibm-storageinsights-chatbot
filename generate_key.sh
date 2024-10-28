#!/bin/bash

# This script generates an AES encryption key of a specified size using OpenSSL.
# It provides a function to create keys of 128, 192, or 256 bits, with base64 encoding.
# Usage is included to generate and display a 256-bit AES key.

generate_aes_key() {
  local key_size=$1

  if [[ $key_size != 128 && $key_size != 192 && $key_size != 256 ]]; then
    echo "Key size must be 128, 192, or 256 bits." >&2
    exit 1
  fi

  # Generate key_size / 8 random bytes, and base64 encode the output
  openssl rand -base64 $((key_size / 8))
}

# Usage:
key_256=$(generate_aes_key 256)  # 256-bit AES key

echo "256-bit key: $key_256"
