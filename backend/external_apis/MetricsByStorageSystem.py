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
from fastapi import HTTPException

from backend.constants.constants import (
    STORAGE_SYSTEM_METRIC,
    TENANT_ID,
    STORAGE_SYSTEM_ID,
    TYPES,
    DURATION,
    METADATA,
    MESSAGE,
    TEXT,
)
from backend.external_apis.Template import API
from backend.utils.Helpers import generate_error_response


class MetricsByStorageSystem(API):
    name = STORAGE_SYSTEM_METRIC
    parameters = {
        TENANT_ID: str,
        STORAGE_SYSTEM_ID: str,
        TYPES: str,
    }
    description = "Get metrics for a specific storage system"

    @classmethod
    def _invoke_and_validate(cls, base_url, parameters, headers, logger):

        get_url = f"{base_url}tenants/{parameters['tenant_id']}/storage-systems/{parameters['storage_system_id']}/metrics"
        logger.info(f"Making the API call:{get_url}")

        request_params = {TYPES: parameters[TYPES]}
        if DURATION in parameters:
            request_params[DURATION] = parameters[DURATION]
        try:
            response = requests.get(get_url, params=request_params, headers=headers)
            # check if the response is empty or not
            if response.content:
                response_data = response.json()
            else:
                response_data = ""
            # handling any errors thrown by external apis, ex. "Parameter duration value can't be greater then 30 days"
            # so that UI can show the error message properly instead of 500 error. If "metadata" is present in
            # response_data, that means an error has occurred
            if METADATA in response_data:
                error_msg = response_data[METADATA][MESSAGE]
                raise HTTPException(
                    status_code=400,
                    detail=generate_error_response(
                        status_code=400, error_msg=error_msg, identifier=TEXT
                    ),
                )
        except Exception as e:
            logger.error(f"[ERROR] Unable to make the API call: {e}", e)
            raise e

        return response_data
