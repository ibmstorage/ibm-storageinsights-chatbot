#!/bin/bash

generate_aes_key() {
  local key_size=$1

  if [[ $key_size != 128 && $key_size != 192 && $key_size != 256 ]]; then
    echo "Key size must be 128, 192, or 256 bits." >&2
    exit 1
  fi

  # Generate key_size / 8 random bytes, and base64 encode the output
  openssl rand -base64 $((key_size / 8))
}

# Example usage:
key_256=$(generate_aes_key 256)  # 256-bit AES key

echo "256-bit key: $key_256"
