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
from backend.constants.constants import *
from backend.utils.ResponseGenerationHelpers import preprocess_api_response
from backend.llm.HostedLlm import HostedLlm
from backend.previous_actions_module.DatabaseOperations import (
    IntentsAndEntitiesDatabaseOperations,
)


class ActionExecutor:

    def execute_action(
        self,
        intent,
        tenant_id,
        api_key,
        username,
        userQuery,
        conversation_id,
        chatController,
        helper,
        global_states,
        conversation_history,
        logger,
    ):
        """
        Executes an action based on the given intent, interacting with various components to handle the process.

        For intents like 'CHATBOT_CAPABILITIES' and 'MORNING_CUP_OF_COFFEE_ROUTINE',
        the 'entities' column is set to None and only the 'question' is used in the process.

        Args:
            intent (str): The intent to be executed.
            tenant_id (str): The tenant identifier.
            api_key (str): The API key for authorization.
            username (str): The username of the user initiating the action.
            userQuery (str): The specific query made by the user, used to retrieve the correct entities from the database.
            conversation_id (str): The conversation identifier.
            chatController (ChatController): The controller used to invoke the API.
            helper (Helper): A helper object for augmenting the response.
            global_states (dict): A dictionary containing global states.
            conversation_history (ConversationHistory): An object managing the conversation history.

        Returns:
            dict: An augmented response with additional conversation details.

        Raises:
            HTTPException: If no entities or question are found for the given intent, raises a 404 error with details.
        """
        # Fetch entities from database based on intent
        entity_dict = IntentsAndEntitiesDatabaseOperations.get_entities_by_intent(
            intent, username, tenant_id, userQuery
        )
        state_key = (conversation_id, username)
        current_state = global_states.get(state_key)
        # Handle specific intents where entities are set to None
        if intent in {CHATBOT_CAPABILITIES, MORNING_CUP_OF_COFFEE_ROUTINE}:
            augmented_response = helper.augment_response(
                intent, None, conversation_id, None, None, None
            )

            current_conversation_thread = (
                conversation_history.create_conversation_thread(
                    conversation_id, userQuery, augmented_response, tenant_id
                )
            )

            conversation_history.store_conversation_history(
                current_conversation_thread,
                current_state,
                conversation_id,
                username,
                tenant_id,
            )
            return augmented_response

        if not entity_dict:
            raise HTTPException(
                status_code=404,
                detail={STATUS: ERROR, MESSAGE: NO_ENTITIES, IDENTIFIER: TEXT},
            )

        entity_dict[TENANT_ID] = tenant_id

        documents = chatController.invoke_API(intent, entity_dict, api_key, logger)
       # Null check for documents
        if not documents or not isinstance(documents, dict) or DATA not in documents:
            error_response = {
                STATUS: NO_CONTENT,
                MESSAGE: "No data available for the given request.",
                IDENTIFIER: MARKDOWN,
                DATA: [],
            }
            raise HTTPException(status_code=204, detail=error_response)
        documents = preprocess_api_response(documents, intent, entity_dict)
        hosted_llmObj = HostedLlm()
        question = userQuery
        response, is_response_generated = (
            hosted_llmObj.extract_answers_from_documents(
                question, intent, documents[DATA]
            )
            if intent in RESPONSE_GENERATION_INTENTS and DATA in documents
            else (documents[DATA], False)
        )
        response = {DATA: response}
        augmented_response = helper.augment_response(
            intent,
            response,
            conversation_id,
            tenant_id,
            (
                entity_dict[STORAGE_SYSTEM_ID]
                if STORAGE_SYSTEM_ID in entity_dict
                else None
            ),
            is_response_generated,
        )
        augmented_response[USER_QUERY] = userQuery

        # Handle conversation history
        question_str = f"{userQuery}"
        current_conversation_thread = conversation_history.create_conversation_thread(
            conversation_id, str(question_str), augmented_response, tenant_id
        )
        current_conversation_thread[ROUTINE] = EXECUTE_PREVIOUS_ACTIONS_ROUTINE
        conversation_history.store_conversation_history(
            current_conversation_thread,
            current_state,
            conversation_id,
            username,
            tenant_id,
        )

        augmented_response[CONVERSATION_ID] = conversation_id
        augmented_response[ROUTINE] = EXECUTE_PREVIOUS_ACTIONS_ROUTINE

        return augmented_response
