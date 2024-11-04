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

import sqlite3
import json
from backend.constants.constants import *


class IntentsAndEntitiesDatabaseOperations:

    @staticmethod
    def insert_intent_and_entities(intent, entity_dict, username, question, tenant_id):
        """
        Inserts an intent and its associated entities into the database.

        For specific intents like 'CHATBOT_CAPABILITIES' and 'MORNING_CUP_OF_COFFEE_ROUTINE',
        the entities will be set to None.

        Args:
            intent (str): The intent to be inserted into the database.
            entity_dict (dict): A dictionary containing the entities associated with the intent.
                                Will be set to None for specific intents.
            username (str): The username of the user initiating the action.
            question (str): The user's question associated with the intent.
            tenant_id (str): The user's Configured tenantID associated with the intent.

        Returns:
            str: A JSON string indicating the success or failure of the operation.

        Raises:
            Exception: If an error occurs during the database insertion, an error message is returned as a JSON string.
        """
        try:
            # Set entities_json to None for CHATBOT_CAPABILITIES intent
            if intent in (CHATBOT_CAPABILITIES, MORNING_CUP_OF_COFFEE_ROUTINE):
                entities_json = None
            else:
                # Convert dictionary to JSON string
                entities_json = json.dumps(entity_dict)
            with sqlite3.connect(INTENTS_AND_ENTITIES_FOR_PA) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """INSERT INTO intents_and_entities (username, intent, entities, userQuery, tenantId)
                                  VALUES (?, ?, ?, ?, ?)""",
                    (username, intent, entities_json, question, tenant_id),
                )
                connection.commit()
                success_message = json.dumps(
                    {
                        STATUS_CODE: 200,
                        STATUS: SUCCESS_STATUS,
                        MESSAGE: "Data inserted successfully",
                        IDENTIFIER: TEXT,
                    }
                )
                print(success_message)
                return success_message
        except Exception as e:
            error_message = json.dumps(
                {STATUS_CODE: 400, STATUS: ERROR, MESSAGE: str(e)}
            )
            return error_message

    @staticmethod
    def get_entities_by_intent(intent, username, tenant_id, userQuery):
        """
        Retrieves the entities associated with a given intent, username, tenant_id, and userQuery from the database.

        For intents like 'CHATBOT_CAPABILITIES' and 'MORNING_CUP_OF_COFFEE_ROUTINE', the
        entities column is stored as None and will not be included in the result.

        Args:
            intent (str): The intent for which the associated entities and question are to be retrieved.
            username (str): The username of the user initiating the action.
            tenant_id (str): The user's Configured tenantID associated with the intent.
            userQuery (str): The specific user query made, used to filter and retrieve the correct entities.

        Returns:
            dict or None: A dictionary containing the 'question' if found.
                        For intents where entities are None, only the question is returned.
                        Returns None if no data is found for the intent.

        Raises:
            RuntimeError: If an error occurs during the database query, an exception with an error message is raised.
        """
        try:
            with sqlite3.connect(INTENTS_AND_ENTITIES_FOR_PA) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """SELECT entities FROM intents_and_entities
                                  WHERE intent = ? AND username = ? AND tenantId = ? AND userQuery = ?""",
                    (intent, username, tenant_id, userQuery),
                )
                result = cursor.fetchone()
                if result and result[0]:  # Ensure result and entities are not None
                    entities_json = result[0]  # Get entities
                    return_value = json.loads(entities_json) if entities_json else None
                    return return_value
                else:
                    return None  # Return None if no entities found for the intent
        except Exception as e:
            raise RuntimeError(f"Error fetching entities from database: {str(e)}")

    # Helper function to format and append missing entities to the userQuery based on the intent
    def append_missing_entities_to_query(question, current_state, intent):
        """
        Format and append missing entities to the user query based on the detected intent.

        This function checks if specific entities such as 'storage_system_id', 'types',
        'severity', and 'duration' are present in the 'current_state' but not explicitly mentioned
        in the user's query ('question'). If any entity is missing, it appends the entity
        information in a readable format at the end of the query.

        Args:
            question (str): The user's original query.
            current_state (dict): The state information containing entities for the current
                                conversation, including possible values such as
                                'storage_system_id', 'types', 'severity', and 'duration'.
            intent (str): The detected intent for the current query, used to determine
                        which entities need to be checked and appended.

        Returns:
            str: The formatted user query with missing entities appended, if applicable.

        Example:
            Original query: "show me volumes for above system"
            After appending: "show me volumes for above system (system ID eaa288e0-e385-11ee-b2e1-cfddfe51829e)"

        Supported intents and entity checks:
            - STORAGE_SYSTEM_DETAILS, STORAGE_SYSTEM_VOLUME: Checks for 'storage_system_id'.
            - STORAGE_SYSTEM_METRIC: Checks for 'storage_system_id', 'types', and 'duration'.
            - STORAGE_SYSTEM_ALERTS, STORAGE_SYSTEM_NOTIFICATIONS: Checks for 'storage_system_id',
            'severity', and 'duration'.
        """
        # Entities to check for based on the intent
        additions = []
        updated_question = question
        if intent in (STORAGE_SYSTEM_DETAILS, STORAGE_SYSTEM_VOLUME):
            storage_system_id = current_state.get(STORAGE_SYSTEM_ID)
            if (
                storage_system_id
                and str(storage_system_id).lower() not in question.lower()
            ):
                additions.append(f"system ID : {storage_system_id}")

        elif intent == STORAGE_SYSTEM_METRIC:
            storage_system_id = current_state.get(STORAGE_SYSTEM_ID)
            types = current_state.get(TYPES)
            duration = current_state.get(DURATION)

            if (
                storage_system_id
                and str(storage_system_id).lower() not in question.lower()
            ):
                additions.append(f"system ID : {storage_system_id}")
            if types and str(types).lower() not in question.lower():
                additions.append(f"metric type : {types}")
            if duration and str(duration).lower() not in question.lower():
                additions.append(f"duration : {duration}")

        elif intent in (STORAGE_SYSTEM_ALERTS, STORAGE_SYSTEM_NOTIFICATIONS):
            storage_system_id = current_state.get(STORAGE_SYSTEM_ID)
            severity = current_state.get(SEVERITY)
            duration = current_state.get(DURATION)

            if (
                storage_system_id
                and str(storage_system_id).lower() not in question.lower()
            ):
                additions.append(f"system ID : {storage_system_id}")
            if severity and str(severity).lower() not in question.lower():
                additions.append(f"severity : {severity}")
            if duration and str(duration).lower() not in question.lower():
                additions.append(f"duration : {duration}")

        # If we have any additions, we can insert them into the userQuery
        if additions:
            updated_question = f"{question} ({', '.join(additions)})"

        return updated_question
