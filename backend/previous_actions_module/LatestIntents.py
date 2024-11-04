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


def get_latest_unique_intents_and_entities(
    db_path, username, conversation_id, global_states, conversation_history, tenant_id, limit=5
):
    """
    Retrieves the latest five intents and their associated entities from the database.

    For intents like 'CHATBOT_CAPABILITIES' and 'MORNING_CUP_OF_COFFEE_ROUTINE', 
    the 'entities' field is explicitly set to null in the returned data.

    Args:
        db_path (str): The path to the SQLite database file.
        username (str): The username of the user initiating the query.
        conversation_id (str): The conversation identifier.
        global_states (dict): A dictionary containing global states.
        conversation_history (ConversationHistory): An object managing the conversation history.
        tenant_id (str): The user's Configured tenantID associated with the intent.
        limit (int, optional): The maximum number of unique intents to retrieve. Defaults to 5.

    Returns:
        str: A JSON string containing the latest unique intents and their associated entities, 
             with entities set to null for specific intents, or an error message if an exception occurs.

    Raises:
        Exception: If an error occurs during the database query, an error message is returned as a JSON string.
    """
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            query = """
            SELECT intent, entities, userQuery
            FROM intents_and_entities 
            WHERE username = ?
            AND tenantId = ?
            ORDER BY id DESC 
            LIMIT ?
            """
            cursor.execute(
                query,
                (
                    username,
                    tenant_id,
                    limit,
                ),
            )
            results = cursor.fetchall()
            # Handle intents like CHATBOT_CAPABILITIES and MORNING_CUP_OF_COFFEE by setting entities as null
            previous_actions = []
            for intent, entities, userQuery in results:
                if intent in (CHATBOT_CAPABILITIES, MORNING_CUP_OF_COFFEE_ROUTINE):
                    entities_data = None  # Explicitly set entities as null for these intents
                else:
                    entities_data = json.loads(entities) if entities else None  # Handle other intents as usual

                previous_actions.append({INTENT: intent, ENTITIES: entities_data, USER_QUERY: userQuery})
            json_response = {
                MESSAGE: RESPONSE,
                PREVIOUS_ACTIONS: previous_actions,
                IDENTIFIER: BUTTONS,
            }
            state_key = (conversation_id, username)
            question_str = f"Previous actions"
            current_state = global_states.get(state_key)
            current_conversation_thread = (
                conversation_history.create_conversation_thread(
                    conversation_id, str(question_str), json_response, tenant_id
                )
            )
            current_conversation_thread[ROUTINE] = GET_PREVIOUS_ACTIONS_ROUTINE
            conversation_history.store_conversation_history(
                current_conversation_thread, current_state, conversation_id, username, tenant_id
            )
            json_response[CONVERSATION_ID] = conversation_id
            return json.dumps(json_response)
    except Exception as e:
        error_response = {STATUS: ERROR, MESSAGE: str(e), IDENTIFIER: TEXT}
        return json.dumps(error_response)
