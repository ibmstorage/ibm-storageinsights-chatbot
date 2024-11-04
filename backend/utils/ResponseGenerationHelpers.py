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

from backend.utils.Helpers import bytes_to_gib, epoch_to_human_readable
from backend.constants.constants import (
    STORAGE_LIST,
    DATA,
    TIMESTAMP_FIELDS,
    STORAGE_SYSTEM_DETAILS,
    TENANT_ALERTS,
    TENANT_NOTIFICATIONS,
    STORAGE_SYSTEM_METRIC,
    STORAGE_SYSTEM_VOLUME,
    STORAGE_SYSTEM_ALERTS,
    STORAGE_SYSTEM_NOTIFICATIONS,
    STORAGE_SYSTEM_ID,
)
from backend.prompt.prompts import (
    storage_list_response_generation_instructions,
    storage_system_detail_response_generation_instructions,
    tenant_alert_response_generation_instructions,
    tenant_notification_response_generation_instructions,
    storage_system_alert_response_generation_instructions,
    storage_system_notification_response_generation_instructions,
)


def get_instructions_for_intent(intent: str):
    """
    This method returns the api specific instructions that we need to add to the prompt
    ex. what are the fields that always needs to be added to the llm response
    :param intent:
    :return:
    """
    if intent == STORAGE_LIST:
        return storage_list_response_generation_instructions
    elif intent == STORAGE_SYSTEM_DETAILS:
        return storage_system_detail_response_generation_instructions
    elif intent == TENANT_ALERTS:
        return tenant_alert_response_generation_instructions
    elif intent == STORAGE_SYSTEM_ALERTS:
        return storage_system_alert_response_generation_instructions
    elif intent == TENANT_NOTIFICATIONS:
        return tenant_notification_response_generation_instructions
    elif intent == STORAGE_SYSTEM_NOTIFICATIONS:
        return storage_system_notification_response_generation_instructions
    else:
        return ""


def preprocess_api_response(document, intent, current_state):
    """
    This method parses the documents and pre-process api response before passing the api response to the llm:
    Different preprocessing needs to be done for different apis
    Storage-list:
        1. Convert bytes to GiB
        2. Convert epoch timestamp to human-readable timestamp
    :param document:
    :return: document with converted values
    """
    if document:
        updated_doc = {}
        if intent == STORAGE_SYSTEM_METRIC:
            for key in document:
                if key == DATA:
                    updated_doc[DATA] = _process_metric_response(document[DATA])
                else:
                    updated_doc[key] = document[key]
            return updated_doc
        elif intent == STORAGE_SYSTEM_VOLUME:
            return document
        else:
            return _convert_capacity_and_timestamp(document, intent, current_state)
    else:
        return document


def _process_metric_response(data):
    """
    Process data section of the api response before sending to the llm
    :param data:
    :return: Updated data section
    """
    updated_data = []
    for item in data:
        new_item = {}
        for key in item:
            value = item[key]
            # convert bytes to gib and update key to reflect capacity is in GiB
            if key == "naturalKey":
                pass
            elif (
                key == "used_capacity"
                or key == "available_capacity"
                or key == "usable_capacity"
            ):
                new_item[key] = bytes_to_gib(value)
            # no change to the key value
            else:
                new_item[key] = value
        updated_data.append(new_item)
    return updated_data


def _convert_capacity_and_timestamp(document, intent, current_state):
    """
    This method parses the documents containing storage list and does following conversions:
        1. Convert bytes to GiB
        2. Convert epoch timestamp to human-readable timestamp
    :param document:
    :return: original document with updated values
    """
    updated_doc = {}
    for key in document:
        if key in TIMESTAMP_FIELDS:
            updated_doc[key] = epoch_to_human_readable(document[key])
        elif key == DATA:
            updated_doc[key] = _process_data_section(document[DATA], intent, current_state)
        else:
            updated_doc[key] = document[key]
    return updated_doc


def _process_data_section(data, intent, current_state):
    """
    Process data section of the api response before sending to the llm
    :param data:
    :return: Updated data section
    """
    updated_data = []
    for item in data:
        new_item = {}
        if intent in (STORAGE_SYSTEM_ALERTS, STORAGE_SYSTEM_NOTIFICATIONS):
            if STORAGE_SYSTEM_ID in current_state:
                new_item[STORAGE_SYSTEM_ID] = current_state[STORAGE_SYSTEM_ID]
        for key in item:
            value = item[key]
            # convert bytes to gib and update key to reflect capacity is in GiB
            if key.endswith("_bytes"):
                updated_key = key.replace("_bytes", "_gib")
                new_item[updated_key] = bytes_to_gib(value)
            # change epoch time from milliseconds to human-readable format
            elif key in TIMESTAMP_FIELDS:
                new_item[key] = epoch_to_human_readable(item[key])
            elif key == "details":
                new_item[key] = _process_details_section(item["details"])
            elif key == "detailsList":
                new_item[key] = _process_details_section(item["detailsList"])
            # no change to the key value
            else:
                new_item[key] = value
        updated_data.append(new_item)
    return updated_data


def _process_details_section(details):
    """
    Process details section of the api response before sending to the llm
    :param details:
    :return:
    """
    updated_details = {}
    for key in details:
        # change epoch time from milliseconds to human-readable format
        if key in TIMESTAMP_FIELDS:
            updated_details[key] = epoch_to_human_readable(details[key])
        # no change to the key value
        else:
            updated_details[key] = details[key]
    return updated_details
