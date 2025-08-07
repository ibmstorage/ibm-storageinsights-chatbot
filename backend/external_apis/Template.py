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

from fastapi import HTTPException
from backend.constants.constants import (
    STATUS,
    IDENTIFIER,
    TEXT,
    MESSAGE,
    BAD_REQUEST,
    TENANT_ID,
    X_API_TOKEN,
    ACCEPT,
    APPLICATION_JSON,
    X_INTEGRATION,
    X_INTEGRATION_VERSION,
    STORAGE_INSIGHTS_CHATBOT,
    VERSION,
    STORAGE_SYSTEM_METRIC,
    intentDescMap,
    STORAGE_SYSTEM_METRIC,
    DURATION,
)
from backend.external_apis.TokenGenerationService import TokenGenerationService
from backend.utils.Helpers import generate_error_response


class API(object):
    name = None
    parameters = None
    description = None

    @classmethod
    def call(cls, base_url, parameters, api_key, intent, logger):

        try:
            # Step 1: Make sure all required parameters are collected
            missing_parameters = cls._missing_parameters(parameters)
            if len(missing_parameters) > 0:
                intent_message = intentDescMap.get(intent)
                # Check for specific intent
                if intent == STORAGE_SYSTEM_METRIC and 'types' in missing_parameters:
                    response = (
                        "To proceed, I need the: %s like for e.g. cpu_utilization, usable_capacity, etc."
                        % (", ".join(missing_parameters))
                    )
                else:
                    response = (
                        "%s. To proceed, I need the: %s"
                        % (intent_message, ", ".join(missing_parameters))
                    )
                # Check for specific response condition
                json_response = {STATUS: BAD_REQUEST, MESSAGE: response, IDENTIFIER: TEXT}
                # Return JSON response with custom HTTP status code 400 (Bad Request)
                raise HTTPException(status_code=400, detail=json_response)

            # Step 2: Generate API otken to make API call
            headers = cls._get_headers(base_url, parameters[TENANT_ID], api_key)

            # Step 2: Check if the duration parameter stored in states is valid or not
            if intent != STORAGE_SYSTEM_METRIC and DURATION in parameters:
                parameters[DURATION] = cls._validate_duration_and_update(
                    parameters[DURATION]
                )
            # Step 4: Make API request and validate the response
            response = cls._invoke_and_validate(base_url, parameters, headers, logger)

            return response  # No display to show
        except HTTPException as e:
            raise e
        except Exception:
            error_msg = "Oops! Something went wrong on our side. Please try again in a moment."
            raise HTTPException(
                status_code=500,
                detail=generate_error_response(
                    status_code=500, error_msg=error_msg, identifier=TEXT
                ),
            )

    @classmethod
    def _invoke_and_validate(cls, base_url, parameters, api_key, logger):
        raise NotImplementedError

    @classmethod
    def _missing_parameters(cls, parameters):
        if cls.parameters:
            return [p for p in cls.parameters if p not in parameters]
        return []

    @classmethod
    def _get_api_token(cls, base_url, tenant_id, api_key) -> str:
        # Use the TokenGenerationService to get the X-API-Token dynamically
        return TokenGenerationService.generate_api_token(base_url, tenant_id, api_key)

    @classmethod
    def _get_headers(cls, base_url, tenant_id, api_key) -> dict:

        headers = {
            X_API_TOKEN: cls._get_api_token(base_url, tenant_id, api_key),
            ACCEPT: APPLICATION_JSON,
            X_INTEGRATION: STORAGE_INSIGHTS_CHATBOT,
            X_INTEGRATION_VERSION: VERSION
        }

        return headers

    @classmethod
    def _validate_duration_and_update(cls, duration: str):
        """
        Method to check if the duration is greater than 30 days. APIS other than storage-system-metric only supports
        duration upto 30 days
        :param duration: extracted duration
        :return:
        """
        duration_day = 0
        if "m" in duration.lower():
            # if duration is given in minutes, convert in days for comparison
            duration_day = (int(duration.replace("m", "")) / 60) / 24
        elif "h" in duration.lower():
            # if duration is given in hours, convert in days for comparison
            duration_day = int(duration.replace("h", "")) / 24
        elif "d" in duration.lower():
            duration_day = int(duration.replace("d", ""))

        # check if the duration is less than 30 days
        if duration_day < 30:
            return duration
        else:
            return "30d"
