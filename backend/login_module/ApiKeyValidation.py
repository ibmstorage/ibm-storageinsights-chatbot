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

import requests
from backend.constants.constants import BASE_URL, X_API_KEY, ACCEPT, APPLICATION_JSON


def key_validation_service(tenant_id: str, api_key: str) -> bool:
    """
    Validate the API key by making a request to the external service.

    Args:
        tenant_id (str): The identifier for the tenant.
        api_key (str): The API key to be validated.

    Returns:
        bool: True if the API key is valid, False otherwise.
    """
    url = f"{BASE_URL}tenants/{tenant_id}/token"
    headers = {
        X_API_KEY: api_key,
        ACCEPT: APPLICATION_JSON,
    }

    try:
        response = requests.post(url, headers=headers)
        if response.status_code in {200, 201}:
            return True
        return False
    except Exception as e:
        print(f"[ERROR] Unable to fetch X-API-Token: {e}", flush=True)
        raise e
