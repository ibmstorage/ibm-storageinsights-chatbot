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

import json
import sqlite3
from datetime import datetime

from backend.constants.constants import *


class ConversationHistory:
    def __init__(self, db_name=CONVERSATION_HISTORY_DB):
        try:
            with sqlite3.connect(db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                CREATE TABLE IF NOT EXISTS conversation (
                    conversation_id TEXT PRIMARY KEY,
                    username TEXT,
                    conversation_title TEXT,
                    conversation_content TEXT,
                    recent_timestamp TEXT,
                    current_state TEXT,
                    tenant_id TEXT
                )
                """
                )
                conn.commit()
        except Exception as e:
            print("failed to create table")
            raise e

    def create_conversation_thread(self, conversation_id, user_message, response_data,tenant_id):
        """
        Creates a dictionary representing a conversation thread.

        Parameters:
        - conversation_id: str
            The ID of the conversation.
        - user_message: str
            The message from the user.
        - response_data: any
            The response data corresponding to the user message.

        Returns:
        - dict: A dictionary representing the conversation thread, including the conversation ID,
                user message, response data, and a timestamp of when the thread was created.
        """
        current_timestamp = datetime.now().isoformat()
        conversation_dict = {
            "conversation_id": conversation_id,
            "Message": user_message,
            "Response": {"responseData": response_data},
            "timestamp": current_timestamp,
            "tenant_id":tenant_id
        }
        return conversation_dict

    def get_conversation_history(self, conversation_id, username, tenant_id):
        """
        Retrieves the conversation history for a given conversation ID and username.

        Parameters:
        - conversation_id: str
            The ID of the conversation whose history is to be retrieved.
        - username: str
            The username of the user requesting the conversation history.

        Returns:
        - dict: The most recent conversation state as a dictionary if found.
        - None: If no conversation history is found for the given conversation ID and username.

        Raises:
        - Exception: If there is an error during the database query.
        """
        try:
            with sqlite3.connect(CONVERSATION_HISTORY_DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT conversation_content 
                FROM conversation 
                WHERE conversation_id = ? AND username = ? AND tenant_id = ?
                ORDER BY conversation_id DESC
                """,
                    (conversation_id, username,tenant_id),
                )
                result = cursor.fetchone()
            if result:
                # Return the last (most recent) conversation state
                return json.loads(result[0])
            else:
                return None  # No conversation history found for given conversation_id and username
        except Exception as e:
            print(f"An error occurred: {e}")
            raise e

    def store_conversation_history(
        self, current_conversation_dict, current_state, conversation_id, username, tenant_id
    ):
        """
        Stores or updates the conversation history for a given conversation ID and username.

        Parameters:
        - current_conversation_dict: dict
            The current conversation message dictionary to be added to the conversation history.
        - current_state: dict
            The current state of the conversation.
        - conversation_id: str
            The ID of the conversation to be stored or updated.
        - username: str
            The username of the user whose conversation history is being stored or updated.

        Returns:
        - None

        Raises:
        - sqlite3.Error: If there is an error during the database operation.
        """
        recent_timestamp = datetime.now().isoformat()
        current_state_str = json.dumps(current_state)
        previous_conversation_history = self.get_conversation_history(
                conversation_id, username, tenant_id
            )
        user_question = current_conversation_dict["Message"]
        if not previous_conversation_history:
            merged_conversation_history = [current_conversation_dict]
        else:
            merged_conversation_history = self.append_conversation(
                previous_conversation_history, current_conversation_dict
            )

        merged_conversation_str = json.dumps(merged_conversation_history)
        initial_conversation_title = user_question
        try:
            with sqlite3.connect(CONVERSATION_HISTORY_DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                UPDATE conversation
                SET conversation_content = ?, recent_timestamp = ?, current_state = ?
                WHERE conversation_id = ? AND username = ? AND tenant_id = ?
                """,
                    (
                        merged_conversation_str,
                        recent_timestamp,
                        current_state_str,
                        conversation_id,
                        username,
                        tenant_id
                ),
                )
                if cursor.rowcount == 0:  # If no rows were updated, insert a new row
                    cursor.execute(
                        """
                    INSERT INTO conversation (conversation_id, username, conversation_title, conversation_content, recent_timestamp, current_state, tenant_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            conversation_id,
                            username,
                            initial_conversation_title,
                            merged_conversation_str,
                            recent_timestamp,
                            current_state_str,
                            tenant_id
                    ),
                    )
                    conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def append_conversation(self, prev_conversation, current_conversation):
        """
        Appends the current conversation to the previous conversation history.

        Parameters:
        - prev_conversation: list
            The previous conversation history, represented as a list of conversation dictionaries.
        - current_conversation: dict
            The current conversation message dictionary to be appended.

        Returns:
        - list: The updated conversation history with the current conversation appended.
        """
        prev_conversation.append(current_conversation)
        return prev_conversation

    def get_user_conversations(self, username, tenant_id):
        """
        Retrieves the list of conversations for a given user.

        Parameters:
        - username (str): The username for which to retrieve conversations.

        Returns:
        - tuple: (conversation_list, None, 200) if the retrieval was successful, where conversation_list is a list of dictionaries containing conversation details.
        - tuple: (None, error_response, 500) if an error occurred, where error_response is a dictionary containing error details.

        Raises:
        - sqlite3.Error: Prints the exception message if an error occurs during the database operation.
        """
        try:
            with sqlite3.connect(CONVERSATION_HISTORY_DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT conversation_id, conversation_title, recent_timestamp
                FROM conversation 
                WHERE username = ? AND tenant_id = ?
                """,
                    (username,tenant_id),
                )
                results = cursor.fetchall()
                conversation_list = []
                for row in results:
                    conversation_list.append(
                        {
                            "conversation_id": row[0],
                            "conversation_title": row[1],
                            "recent_timestamp": row[2],
                        }
                    )
                return conversation_list, None, 200
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            error_response = {
                STATUS: ERROR,
                MESSAGE: ERROR_GETTING_CONVERSATION_HISTORY,
                IDENTIFIER: TEXT,
            }
            return None, error_response, 500

    def update_conversation_title(self, conversation_id, username, new_title, tenant_id):
        """
        Updates the title of a conversation for a given user.

        Parameters:
        - conversation_id (int): The ID of the conversation to be updated.
        - username (str): The username of the user who owns the conversation.
        - new_title (str): The new title for the conversation.

        Returns:
        - tuple: (rowcount, None, 200) if the update was successful, where rowcount is the number of rows updated.
        - tuple: (None, error_response, 500) if an error occurred, where error_response is a dictionary containing error details.

        Raises:
        - Exception: Prints the exception message if an error occurs during the database operation.
        """
        try:
            with sqlite3.connect(CONVERSATION_HISTORY_DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                UPDATE conversation
                SET conversation_title = ?
                WHERE conversation_id = ? AND username = ? AND tenant_id = ?
                """,
                    (new_title, conversation_id, username, tenant_id),
                )
                conn.commit()
                return cursor.rowcount, None, 200  # Returns the number of rows updated
        except Exception as e:
            print(f"An error occurred: {e}")
            error_response = {
                STATUS: ERROR,
                MESSAGE: RENAME_UNSUCCESSFUL,
                IDENTIFIER: TEXT,
            }
            return None, error_response, 500

    def delete_conversations(self, conversation_ids, username, tenant_id):
        """
        Deletes conversations from the database based on the provided conversation IDs, username, and tenant ID.

        Args:
            conversation_ids (list): A list of conversation IDs to be deleted.
            username (str): The username associated with the conversations to be deleted.
            tenant_id (str): The tenant ID associated with the conversations to be deleted.

        Returns:
            tuple:
                - int: The number of rows deleted from the database.
                - dict or None: An error response dictionary if an error occurs, otherwise None.

        Raises:
            sqlite3.Error: Prints the exception message if an error occurs during the database operation.
        """
        try:
            with sqlite3.connect(CONVERSATION_HISTORY_DB) as conn:
                cursor = conn.cursor()
                placeholders = ",".join("?" for _ in conversation_ids)
                query = f"""
                DELETE FROM conversation
                WHERE conversation_id IN ({placeholders}) AND username = ? AND tenant_id = ?
                """
                cursor.execute(query, (*conversation_ids, username, tenant_id))
                conn.commit()
                return cursor.rowcount, None  # Returns the number of rows deleted
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            error_response = {
                "status": "error",
                "message": "Delete unsuccessful",
                "identifier": "text",
            }
            return None, error_response


    def get_current_state(self, conversation_id, username, tenant_id):
        """
        Retrieve the current state of a specific conversation for a given user.

        Args:
            conversation_id (str): The ID of the conversation.
            username (str): The username associated with the conversation.

        Returns:
            dict or None: The current state of the conversation if found, otherwise None.

        Raises:
            sqlite3.Error: If there is an issue with the database query.
        """
        try:
            with sqlite3.connect(CONVERSATION_HISTORY_DB) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                SELECT current_state 
                FROM conversation 
                WHERE conversation_id = ? AND username = ? AND tenant_id = ?
                """,
                    (conversation_id, username,tenant_id),
                )
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                else:
                    return None  # No current state found for the given conversation_id and username

        except sqlite3.Error as e:
            print(f"An error occurred while retrieving the current state: {e}")
            return None
