'''
{COPYRIGHT-TOP}
IBM Confidential
(C) Copyright IBM Corp. 2019, 2022, 2023, 2024

<< 5608-WC0/5608-PC4 >>

All Rights Reserved
Licensed Material - Property of IBM
The source code for this program is not published or otherwise
divested of its trade secrets, irrespective of what has
been deposited with the U. S. Copyright Office.

U.S. Government Users Restricted Rights
- Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
{COPYRIGHT-END}
'''

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64
from backend.constants.constants import SECRET_KEY

class EncryptionService:
    """
    A class to handle encryption and decryption operations.
    """

    def __init__(self):
        """
        Initializes an instance of EncryptionService with the provided encryption key.

        Args:
            encryption_key (str): A secure key to encrypt/decrypt values.
        """
        encryption_key=os.getenv(SECRET_KEY)
        self.encryption_key = base64.b64decode(encryption_key)

    def decrypt_value(self, encrypted_value: str) -> str:
        """
        Decrypts an encrypted value using AES decryption.

        Args:
            encrypted_value (str): The Base64 encoded encrypted value.

        Returns:
            str: The decrypted value.

        Raises:
            ValueError: If decryption fails.
        """
        try:
            # Decode the Base64 encoded string
            encrypted_value_bytes = base64.b64decode(encrypted_value)
            
            # Extract the IV (first 16 bytes) and ciphertext (remaining bytes)
            iv = encrypted_value_bytes[:16]  # First 16 bytes are IV
            ciphertext = encrypted_value_bytes[16:]  # Remaining bytes are the ciphertext
            
            # Create the AES Cipher object with CBC mode
            cipher = Cipher(algorithms.AES(self.encryption_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()

            # Decrypt and finalize the decryption
            decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove PKCS7 padding
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
            decrypted_value = unpadder.update(decrypted_padded) + unpadder.finalize()

            return decrypted_value.decode('utf-8')  # Decode to UTF-8 string

        except Exception as e:
            print(f"Decryption error: {e}")
            raise ValueError("Decryption failed.")
