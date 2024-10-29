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

import re
import json
import datetime

from fastapi import HTTPException

from backend.constants.constants import *


def check_and_update_incomplete_intent(
    username, intent, incomplete_intent, incomplete_intent_count, logger
):
    """
    Method to handle checking and updation of incomplete intents.
    :param username: username
    :param intent: new intent detected
    :param incomplete_intent: dictionary to keep track of most recent incomplete intent
    :param incomplete_intent_count: dictionary to keep count of number of incomplete intents
    """
    # Check if there is an incomplete intent for the user
    # load the previous incomplete intent
    if username in incomplete_intent:
        previous_intent = incomplete_intent[username]
        logger.info(f"Incomplete intent {previous_intent} found for user {username}")

        if (
            intent == previous_intent
            or intent == SYSTEM_ID_ASSERTION
            or intent == METRIC_TYPE_ASSERTION
        ):
            intent = previous_intent
            logger.info(
                f"Intent: {intent} | Proceeding with the same intent as before or received "
                f"system-id/metric-type assertion."
            )
        else:
            # If user provided a new intent, check if we have reached the threshold of intent changes
            if username not in incomplete_intent_count:
                incomplete_intent_count[username] = 1
                logger.info(
                    f"Incomplete Intent Count = {incomplete_intent_count[username]} for intent {intent}"
                )
            else:
                incomplete_intent_count[username] += 1
                logger.info(
                    f"Incomplete Intent Count = {incomplete_intent_count[username]} for intent {intent}"
                )

            # Threshold to avoid multiple incomplete intents
            if incomplete_intent_count[username] >= 3:  # Threshold of 3 retries
                # Graceful exit: Clear the incomplete intent, reset counter, and return a message
                logger.info(
                    f"Threshold Breached | Incomplete Intent Count = {incomplete_intent_count[username]} | "
                    f"Gracefully Exiting"
                )
                del incomplete_intent[username]
                del incomplete_intent_count[username]
                graceful_exit_clarification = {
                    STATUS: BAD_REQUEST,
                    MESSAGE: GRACEFUL_EXIT_MESSAGE,
                    IDENTIFIER: MARKDOWN,
                }
                raise HTTPException(status_code=400, detail=graceful_exit_clarification)
            else:
                # If not yet reached the threshold, store the new incomplete intent
                incomplete_intent[username] = intent
                logger.info(
                    f"New incomplete intent {intent} stored for user {username}"
                )
    return intent


def generate_error_response(status_code, error_msg, identifier) -> dict:
    """
    Method to generate proper error response from given details
    :param status_code: status code to be sent to UI
    :param error_msg: error message to be sent to UI
    :param identifier: identifier to send to UI, can be text, grid, chart,..
    :return: dictionary with all the error information to be sent to UI
    """
    response = {}
    if status_code:
        response[STATUS] = status_code
    if error_msg:
        if error_msg == RESOURCE_NOT_FOUND:
            error_msg = (
                "Requested resource was not found on the selected tenant, plz check the resource ID or "
                "tenant ID or the parameters that you entered"
            )
        response[MESSAGE] = error_msg
    if identifier:
        response[IDENTIFIER] = identifier
    return response


def is_valid_uuid(uuid_string):
    uuid_regex = re.compile(VALID_UUID_REGEX, re.IGNORECASE)
    return bool(uuid_regex.match(uuid_string))


def bytes_to_gib(bytes_value):
    gib_value = bytes_value / (1024**3)
    return round(gib_value, 2)


def epoch_to_human_readable(epoch_ms):
    # Convert milliseconds to seconds
    epoch_seconds = epoch_ms / 1000.0
    # Convert epoch time to datetime
    human_readable_time = datetime.datetime.fromtimestamp(epoch_seconds)
    # Format the datetime object to a readable string
    formatted_time = human_readable_time.strftime("%b %d, %Y, %H:%M:%S")
    return formatted_time


def get_intent_link(intent, tenant_id, system_uuid):
    """
    This method will generate a Storage insights link depending on the intent
    :param intent: intent of user query
    :param tenant_id: configured tenant id
    :param system_uuid: mentioned system uuid
    :return: URL pointing to a page in Storage Insights
    """
    if intent in (TENANT_ALERTS, STORAGE_SYSTEM_ALERTS) and tenant_id:
        return f"{SI_BASE_URL}{tenant_id}#alerts"
    elif intent in (TENANT_NOTIFICATIONS, STORAGE_SYSTEM_NOTIFICATIONS) and tenant_id:
        return f"{SI_BASE_URL}{tenant_id}#notifications"
    elif intent == STORAGE_LIST and tenant_id:
        return f"{SI_BASE_URL}{tenant_id}#storageSystems?tab=0"
    elif intent == STORAGE_SYSTEM_DETAILS and tenant_id and system_uuid:
        return f"{SI_BASE_URL}{tenant_id}#storageDetail?l3={system_uuid}"
    elif intent == STORAGE_SYSTEM_VOLUME and tenant_id and system_uuid:
        return f"{SI_BASE_URL}{tenant_id}#storageDetail?l3={system_uuid}&link=volumes"
    elif intent == STORAGE_SYSTEM_METRIC and tenant_id:
        return f"{SI_BASE_URL}{tenant_id}#storageSystems?tab=2"
    else:
        return None


class Helpers:

    def __init__(self, registered_apis=None):
        self.registered_apis = registered_apis
        self.storage_name_to_id = {}

    def get_api_list(self):
        """
        This method returns the supported apis as a list
        :return:
        """
        apis = {api.name: api for api in self.registered_apis}
        apisList = list(apis.keys())
        return apisList

    def get_api_parameters(self, intent):
        """
        This method returns the parameters required to service a particular intent
        :param intent:
        :return: parameters to invoke the api
        """
        for api in self.registered_apis:
            if api.name == intent and api.parameters is not None:
                return list(api.parameters.keys())
        return None

    def get_param_dict(self, entities):
        """
        This method will convert the llm response string in a proper dict with key value pairs
        :param entities:
        :return:
        """
        pairs = entities[1:-1].split(", ")
        entity_dict = {}
        # Creating a dictionary using dictionary comprehension
        for pair in pairs:
            splits = pair.split(",")
            for item in splits:
                temp = item.split(":")
                if len(temp) == 2:
                    if len(temp[1]) > 0:
                        entity_dict[temp[0]] = temp[1]

        return entity_dict

    def augment_response(
        self,
        intent,
        response,
        conversation_id,
        tenant_id,
        system_uuid,
        is_response_generated,
    ):
        """
        This method augments the response with extra parameters which are used by UI to render the output
        :param is_response_generated: whether a response is generated by a llm or not
        :param system_uuid: storage system id
        :param tenant_id: configured tenant id
        :param intent: intent of the user query
        :param response: API respones from external APIs
        :param conversation_id: current conversation id
        :return: augmented response
        """
        # Ensure response is initialized as a dictionary if it's None
        if response is None:
            response = {}
        try:
            if intent is None or response is None:
                raise ValueError("Intent/response parameters cannot be None.")
            # check if response generation can be done for this intent and if response generation was successfully done.
            # In case the api response is too big to fit in the context window of the llm, response generation will not
            # be done and data will be shown directly as a table
            elif intent in RESPONSE_GENERATION_INTENTS and is_response_generated:
                response.update({INTENT: intent, IDENTIFIER: MARKDOWN})
            elif intent in (
                STORAGE_SYSTEM_VOLUME,
                STORAGE_SYSTEM_ALERTS,
                STORAGE_SYSTEM_NOTIFICATIONS,
                TENANT_ALERTS,
                TENANT_NOTIFICATIONS,
                STORAGE_LIST,
            ):
                response.update({f"{INTENT}": f"{intent}", f"{IDENTIFIER}": f"{GRID}"})
            elif intent == STORAGE_SYSTEM_DETAILS:
                response.update(
                    {f"{INTENT}": f"{intent}", f"{IDENTIFIER}": f"{PROPERTIES}"}
                )
            elif intent == STORAGE_SYSTEM_METRIC:
                response.update({f"{INTENT}": f"{intent}", f"{IDENTIFIER}": f"{CHART}"})
            elif intent == CHATBOT_CAPABILITIES:
                response.update(
                    {
                        f"{INTENT}": f"{intent}",
                        f"{IDENTIFIER}": f"{MARKDOWN}",
                        f"{DATA}": f"{EPSILON_SUMMARY}",
                    }
                )
            elif intent in (GREETINGS, THANKING) and is_response_generated:
                response.update({IDENTIFIER: MARKDOWN})
            elif intent == MORNING_CUP_OF_COFFEE_ROUTINE:
                response.update(
                    {
                        f"{INTENT}": f"{intent}",
                        f"{IDENTIFIER}": f"{TEXT}",
                        f"{MESSAGE}": f"{MORNING_CUP_OF_COFFEE_ROUTINE_RESPONSE_MESSAGE}",
                    }
                )
            elif intent == UNKNOWN:
                response.update(
                    {
                        f"{INTENT}": f"{intent}",
                        f"{IDENTIFIER}": f"{MARKDOWN}",
                        f"{DATA}": f"{UNKNOWN_INTENT}",
                    }
                )
            else:
                # Handle the case where intent is None (unexpected scenario)
                raise ValueError("Unsupported intent: {intent}.")
            link = get_intent_link(intent, tenant_id, system_uuid)
            response.update({CONVERSATION_ID: conversation_id, LINK: link})
            return response
        except ValueError as ve:
            # Construct JSON error response
            error_response = {
                STATUS: ERROR,
                DESCRIPTION: VALIDATION_ERROR,
                MESSAGE: ve.__str__(),
                DATA: None,
                CONVERSATION_ID: conversation_id,
            }
            return error_response
        except Exception as e:
            # Construct JSON error response for unexpected exceptions
            error_message = f"An unexpected error occurred: {str(e)}"
            error_response = {
                STATUS: ERROR,
                DESCRIPTION: INTERNAL_SERVER_ERROR,
                MESSAGE: error_message,
                DATA: None,
                CONVERSATION_ID: conversation_id,
            }
            return error_response

    def filter_entities_from_result(self, result: dict, user_question: str) -> dict:
        """
        Method to parse the LLM output and validate the entities in the dictionary, based on the user question.
        After creating the dictionary, checks if the entity is mentioned in the user question, and removes it if not.

        :param result: LLM output as a dictionary.
            ex. result = {"storage_system_id": "DS8000", "types":"ip_replication_total_transfer_size",
            "severity": "info_acknowledged", "duration": "9h"}
        :param user_question: The original user question.
        :return: Validated dictionary containing only the verified entities based on the user question.
        """
        # Initialize the dictionary to hold validated entities
        entity_dict = {}
        user_question = user_question.lower()

        for key, value in result.items():
            if key == STORAGE_SYSTEM_ID:
                valid_value = self._validate_system_uuid(value)
            elif key == SYSTEM_NAME:
                valid_value = value
            elif key == SEVERITY:
                valid_value = self._validate_severity(value)
            elif key == DURATION:
                valid_value = self._validate_duration(value)
            elif key == TYPES:
                valid_value = self._validate_types(value)
            else:
                # Skip any unexpected keys
                continue

            # If the value is valid, add it to the entity_dict
            if valid_value:
                entity_dict[key] = valid_value

        # After creating the dictionary, check if each entity is mentioned in the user question
        return self._remove_unmentioned_entities(entity_dict, user_question)

    def _validate_duration(self, value: str) -> str | None:
        """
        Validate the duration.
        :param value: The duration.
        :return: The valid duration or None if invalid.
        """
        value = value.lower().strip()
        if re.search(VALID_DURATION_PATTERN, value):
            return value
        elif any(sub in value for sub in DAYS_VARIATION):
            return value.replace(" ", "").replace("days", "d").replace("day", "d")
        elif any(sub in value for sub in HOURS_VARIATION):
            value = (
                value.replace(" ", "")
                .replace("hours", "h")
                .replace("hour", "h")
                .replace("hrs", "h")
                .replace("hr", "h")
            )
            return value
        elif any(sub in value for sub in MINUTES_VARIATION):
            value = (
                value.replace(" ", "")
                .replace("minutes", "m")
                .replace("mins", "m")
                .replace("min", "m")
            )
            return value
        return None

    def _validate_severity(self, value: str) -> str | None:
        """
        Validate the severity level.
        :param value: The severity level.
        :return: The valid severity level or None if invalid.
        """
        value = value.lower()
        if value in VALID_SEVERITIES:
            return value
        elif any(sub in value for sub in INFORMATIONAL_ACK_VARIATIONS):
            return VALID_SEVERITIES[4]
        elif any(sub in value for sub in WARNING_ACK_VARIATIONS):
            return VALID_SEVERITIES[5]
        elif any(sub in value for sub in CRITICAL_ACK_VARIATIONS):
            return VALID_SEVERITIES[6]
        return None

    def _validate_types(self, value: str) -> str | None:
        """
        Validate the metric types.
        :param value: The metric type.
        :return: The valid metric type or None if invalid.
        """
        value = value.lower().strip()
        value = re.sub(r"\s+", "_", value)
        value = value.replace("-", "_")
        if value in VALID_METRIC_TYPE:
            return value
        return None

    def _validate_system_uuid(self, value: str) -> str | None:
        """
        Validate the system uuid.
        :param value: system uuid alphanumeric string.
        :return: The valid system uuid or None if invalid.
        """
        if is_valid_uuid(value):
            return value
        return None

    def _contains_duration(self, question: str) -> bool:
        """
        Check if the user question contains any valid duration mention using the _validate_duration method.
        :param value: The original user question.
        :return: Boolean True if duration is valid else False.
        """
        for word in question.split():
            if self._validate_duration(word):
                return True
        return False

    def _remove_unmentioned_entities(
        self, entity_dict: dict, user_question: str
    ) -> dict:
        """
        Remove entities from the dictionary if they are not mentioned in the user question.
        :param entity_dict: The dictionary of validated entities.
        :param user_question: The original user question.
        :return: The filtered dictionary with only entities mentioned in the user question.
        """
        user_question = user_question.lower().strip()
        keys_to_remove = []

        # Check if each entity is mentioned as a substring in the user question
        for key, value in entity_dict.items():
            if key == STORAGE_SYSTEM_ID:
                if value not in user_question:
                    keys_to_remove.append(key)

            elif key == SYSTEM_NAME:
                if value.lower() not in user_question:
                    keys_to_remove.append(key)

            elif key == SEVERITY:
                severity_parts = value.split("_") if "_" in value else [value]
                valid_severity_found = any(
                    part in user_question for part in severity_parts
                )
                if not valid_severity_found:
                    keys_to_remove.append(key)

            elif key == DURATION:
                if not self._contains_duration(user_question):
                    keys_to_remove.append(key)

            elif key == TYPES:
                type_substrings = value.split("_")
                valid_types_found = any(sub in user_question for sub in type_substrings)
                if not valid_types_found:
                    keys_to_remove.append(key)

        # Remove the keys that were not found in the user question
        for key in keys_to_remove:
            del entity_dict[key]

        return entity_dict

    def get_storage_system_id(
        self, system_name, tenant_id, api_key, chat_controller, logger
    ) -> str:
        """
        Given a storage system name, this method will return the corresponding storage system id
        :param system_name: name of the storage system user entered
        :param tenant_id:
        :param api_key:
        :param chat_controller:
        :return: storage system uuid corresponding to storage system name
        """
        name_to_id = {}

        # if storage list is not available, call the external api to fetch storage list
        if tenant_id not in self.storage_name_to_id:
            logger.info(f"Fetching storage list for tenant {tenant_id}")
            response = chat_controller.invoke_API(
                STORAGE_LIST, {TENANT_ID: tenant_id}, api_key, logger
            )
            self.__create_name_to_id_map(response[DATA], tenant_id)

        # load the storage list for this tenant
        if tenant_id in self.storage_name_to_id:
            name_to_id = self.storage_name_to_id[tenant_id]
            logger.info(f"Loaded name to id map {name_to_id} for tenant {tenant_id}")

        if system_name in name_to_id:
            system_id = name_to_id[system_name]
            logger.info(
                f"System id {system_id} found corresponding to name {system_name}"
            )
            return system_id
        else:
            return system_name

    def parse_output(self, output: str) -> str:
        """
        This method parses the given llm response to remove specific unwanted characters.
        This method removes: Newline characters, Square brackets, Commas, Full stops, Leading and trailing whitespace.
        :param output: The raw output string generated by llm.
        :return: The cleaned string with unwanted characters removed.
        """
        # Remove newline characters
        output = output.replace("\n", "")

        # Remove square brackets, commas, and full stops
        output = re.sub(r"[\[\],.]", "", output)

        # Remove any leading or trailing whitespace
        output = output.strip()

        return output

    def LLMOutputToDict(self, string: str) -> dict | None:
        """
        This method converts llm string response to a dictionary.
        :param string: The input string to be converted.
        :return: A dictionary representation of the string, or None if conversion fails.
        """
        string = string.strip()

        if not string:
            print("Error: Received an empty string.")
            return None

        try:
            result = json.loads(string.replace("'", '"'))
            if isinstance(result, dict):
                keys_to_remove = [
                    key for key, value in result.items() if isinstance(value, list)
                ]
                for key in keys_to_remove:
                    del result[key]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

        return result

    def __create_name_to_id_map(self, data, tenant_id) -> None:
        """
        Given storage list data, this method will create a storage system name to storage system id mapping for a
        given tenant
        :param data:
        :param tenant_id:
        :return:
        """
        if METADATA in data:
            return

        name_to_id = {}
        for system in data:
            system_name = system["name"].lower()
            name_to_id[system_name] = system[STORAGE_SYSTEM_ID]

        self.storage_name_to_id[tenant_id] = name_to_id
