# Copyright 2024. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from backend.constants.constants import (
    IDENTIFIER,
    MESSAGE,
    STATUS,
    ERROR,
    INVALID_CREDENTIALS_MESSAGE,
    TEXT,
    USERNAME,
    TENANT_ID
)
from backend.login_module.ApiKeyValidation import key_validation_service


class UserLoginModule:
    """
    A class to handle user login operations.

    This class provides functionality to authenticate users based on their
    username/email, tenant ID, and API key. It performs the validation through
    a key validation service and generates a JWT token upon successful login.
    """
    def __init__(self):
        """
        Initializes an instance of UserLoginModule.

        No arguments are passed during initialization.
        """
        pass

    def login_user(self, username_or_email: str, tenant_id: str, api_key: str):
        """
        Authenticates a user using their username/email, tenant ID, and API key.

        Args:
            username_or_email (str): The username or email of the user.
            tenant_id (str): The tenant ID associated with the user.
            api_key (str): The API key for the tenant.

        Returns:
            tuple: A tuple containing:
                - access_token (str or None): The JWT token generated on successful login.
                - user_data_response (dict or None): Dictionary containing user data like USERNAME and TENANT_ID.
                - error_response (dict or None): Error message and details in case of a failure.
                - status_code (int): The HTTP status code indicating success (200) or failure (401 or 500).
        """
        try:
            is_valid = key_validation_service(tenant_id, api_key)
            if is_valid:
                user_data_response = {
                        USERNAME: username_or_email,
                        TENANT_ID:tenant_id,
                }  
                return user_data_response, None, 200
            else:
                status_code = 401
                error_response = {
                    STATUS: ERROR,
                    MESSAGE: INVALID_CREDENTIALS_MESSAGE,
                    IDENTIFIER: TEXT,
                }
                return None, None, error_response, status_code

        except Exception as e:
            print(f"Error logging in user: {e}")
            return None, None, "Failed to login user.", 500