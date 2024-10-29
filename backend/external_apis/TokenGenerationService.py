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
import time
from backend.constants.constants import X_API_KEY, ACCEPT, APPLICATION_JSON

cached_token = {}
token_expiry_time = {}


class TokenGenerationService:

    @classmethod
    def generate_api_token(cls, base_url, tenant_id, api_key):
        global cached_token
        global token_expiry_time
        current_time = time.time()

        if (
            tenant_id in cached_token
            and tenant_id in token_expiry_time
            and current_time < token_expiry_time[tenant_id]
        ):
            return cached_token[tenant_id]

        headers = {
            X_API_KEY: api_key,
            ACCEPT: APPLICATION_JSON,
        }

        token_url = f"{base_url}tenants/{tenant_id}/token"
        try:
            response = requests.post(token_url, headers=headers)
            response.raise_for_status()
            token_data = response.json().get("result")
            new_token = token_data.get("token")

            token_expiry_time[tenant_id] = current_time + 720

            cached_token[tenant_id] = new_token
            return new_token
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Unable to fetch X-API-Token: {e}", flush=True)
            return None
