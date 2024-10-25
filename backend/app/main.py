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
import os
import uuid
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api import APIController
from backend.app.chat import ChatController
from backend.encryption_module.Encryption import EncryptionService
from backend.constants.constants import *
from backend.conversation_history.conversation_history import ConversationHistory
from backend.conversation_history.conversation_history_model import (
    RenameConversationHistoryRequest,
    DeleteConversationsRequest,
)
from backend.external_apis import REGISTERED_APIS
from backend.llm.HostedLlm import HostedLlm
from backend.logging_module.Logging import Logging
from backend.login_module.user_login import UserLoginModule
from backend.login_module.user_login_model import (
    UserLoginRequest,
    LogoutRequest,
)
from backend.models.chatbot import (
    RunChatbotModel,
    ExecuteActionModel,
    PreviousActionModel,
    MorningCupOfCoffeeModel,
)
from backend.previous_actions_module.DatabaseOperations import (
    IntentsAndEntitiesDatabaseOperations,
)
from backend.previous_actions_module.DbInitialisation import (
    PreviousActionsDatabaseInitialisation,
)
from backend.previous_actions_module.ExecuteAction import ActionExecutor
from backend.previous_actions_module.LatestIntents import (
    get_latest_unique_intents_and_entities,
)
from backend.utils.Helpers import Helpers
from backend.utils.Helpers import (
    check_and_update_incomplete_intent,
)
from backend.utils.ResponseGenerationHelpers import preprocess_api_response

logger = None
hosted_llmObj = None
helper = None
apiController = None
chatController = None
login_module = None
conversation_history = None
global_states = {}
incomplete_intent = {}
consecutive_exception_count = {}
incomplete_intent_count = {}
encryption_module = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        global logger, hosted_llmObj, helper, apiController, chatController, login_module, conversation_history, encryption_module

        logger = Logging("si_chatbot")
        hosted_llmObj = HostedLlm()
        helper = Helpers(REGISTERED_APIS)
        apiController = APIController(BASE_URL)
        chatController = ChatController(apiController)
        encryption_module = EncryptionService()
   
        login_module = UserLoginModule()
        # Initialize the previous actions database
        PreviousActionsDatabaseInitialisation.initialize_intent_entity_database()
        conversation_history = ConversationHistory()
        logger.info("si-chatbot-be app initialization completed successfully")
        yield

    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

    finally:
        logger.info("si-chatbot-be app closed")


app = FastAPI(lifespan=lifespan)

# Adding middleware *before* the app starts
origins = [
    os.getenv("ORIGIN"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # List of allowed methods
    allow_headers=["*"],  # List of allowed headers
)


@app.post("/chatbot/run_chatbot")
def run_chatbot(request: RunChatbotModel):
    """
    This endpoint is responsible for servicing user queries
    :param request: {"userQuery": "", "api_key": "", "tenant_id":}
    :return:
    """
    global global_states, incomplete_intent, consecutive_exception_count, incomplete_intent_count
    # get necessary parameters from user request
    question = request.userQuery
    tenant_id = request.tenant_id
    encrypted_api_key = request.api_key
    username = request.username
    conversation_id = request.conversation_id or str(uuid.uuid4())
    intent = None
    try:
        api_key = encryption_module.decrypt_value(encrypted_api_key)
        # Retrieve or initialize the state for the given conversation_id and username
        state_key = (conversation_id, username)

        current_state = conversation_history.get_current_state(
            conversation_id, username, tenant_id
        )
        logger.info(f"Current state {current_state} loaded for user {username}")
        if current_state:
            global_states[state_key] = current_state

        # Delete incomplete intent if a new chat thread is started
        if state_key not in global_states:
            global_states[state_key] = {}
            if username in incomplete_intent:
                del incomplete_intent[username]
                if username in incomplete_intent_count:
                    del incomplete_intent_count[username]
                logger.info(
                    f"New conversation thread detected. Deleted incomplete intent for user {username}"
                )
            if username in consecutive_exception_count:
                del consecutive_exception_count[username]
                logger.info(
                    f"New conversation thread detected. Deleted consecutive exception count for user {username}"
                )

        # call the llm chain to detect intent
        intent = hosted_llmObj.get_intent_of_utterance(question)
        logger.info(f"Detected intent {intent} for user query {question}")
        if intent in (GREETINGS, THANKING):
            # generate response to these common intents using llm for better ux
            llm_response = hosted_llmObj.common_intents_response_generator(intent,question)
            logger.info(f"Generated common intent response {llm_response} using llm for user query {question}")
            augmented_response = helper.augment_response(
                intent, llm_response, conversation_id, None, None, True
            )
            current_conversation_thread = (
                conversation_history.create_conversation_thread(
                    conversation_id, str(question), augmented_response, tenant_id
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
        elif intent == MORNING_CUP_OF_COFFEE_ROUTINE:
            augmented_response = helper.augment_response(
                intent, None, conversation_id, None, None, None
            )
            current_conversation_thread = (
                conversation_history.create_conversation_thread(
                    conversation_id, question, augmented_response, tenant_id
                )
            )
            conversation_history.store_conversation_history(
                current_conversation_thread,
                current_state,
                conversation_id,
                username,
                tenant_id,
            )
            if augmented_response is not None:
                IntentsAndEntitiesDatabaseOperations.insert_intent_and_entities(
                    intent, augmented_response, username, question, tenant_id
                )
            return augmented_response
        elif intent == CHATBOT_CAPABILITIES or intent == UNKNOWN:
            augmented_response = helper.augment_response(
                intent, None, conversation_id, None, None, None
            )
            current_conversation_thread = (
                conversation_history.create_conversation_thread(
                    conversation_id, str(question), augmented_response, tenant_id
                )
            )
            conversation_history.store_conversation_history(
                current_conversation_thread,
                current_state,
                conversation_id,
                username,
                tenant_id,
            )
            if intent == CHATBOT_CAPABILITIES and augmented_response is not None:
                IntentsAndEntitiesDatabaseOperations.insert_intent_and_entities(
                    intent, augmented_response, username, question, tenant_id
                )
            return augmented_response

        # check if there is any incomplete intent or if the intent is not servicable
        if username not in incomplete_intent and intent not in helper.get_api_list():
            # Construct a dictionary representing the error response
            error_response = {STATUS: ERROR, MESSAGE: UNKNOWN_INTENT, IDENTIFIER: TEXT}
            raise HTTPException(status_code=501, detail=error_response)

        # Call the helper function to check and update incomplete intents
        intent = check_and_update_incomplete_intent(
            username, intent, incomplete_intent, incomplete_intent_count, logger
        )
        # call the llm chain to detect entities
        entity_dict = hosted_llmObj.extract_entities_from_utterance(question)
        logger.info(
            f"Extracted entities {entity_dict} from user query {question} for user {username}"
        )
        entity_dict[TENANT_ID] = tenant_id
        # user can enter storage system name in place of uuid
        # fetch corresponding uuid for the system_name in the scenario where uuid is absent
        # in either scenario, we will remove the system_name from entity_dict
        if SYSTEM_NAME in entity_dict:
            logger.info(
                f"For user query {question}, user entered system name instead of system id"
            )
            mapped_storage_system_id = helper.get_storage_system_id(
                entity_dict[SYSTEM_NAME].lower(),
                tenant_id,
                api_key=api_key,
                chat_controller=chatController,
                logger=logger,
            )
            # if a valid new storage system id is found, update the entity_dict
            if mapped_storage_system_id != entity_dict[SYSTEM_NAME]:
                entity_dict[STORAGE_SYSTEM_ID] = mapped_storage_system_id
                del entity_dict[SYSTEM_NAME]
            else:
                del entity_dict[SYSTEM_NAME]
                # an exception is raised if the system uuid is not found for the tenant
                system_not_found_response = {
                    STATUS: BAD_REQUEST,
                    MESSAGE: INAVLID_SYSTEM_NAME,
                    IDENTIFIER: MARKDOWN,
                }
                raise HTTPException(status_code=400, detail=system_not_found_response)
        logger.info(
            f"Updated entities for user {username} and query {question} are {entity_dict}"
        )

        # Update the state with the new entities
        global_states[state_key] = chatController.update_states(
            global_states[state_key], entity_dict, logger
        )
        current_state = global_states[state_key]
        augmented_response = None
        error_response = None
        # invoke the api based on intent and entities
        documents = chatController.invoke_API(
            intent, global_states[state_key], api_key, logger
        )
        logger.info(f"Documents fetched are: {documents}")
        documents = preprocess_api_response(documents, intent, current_state)
        logger.info(f"Sending pre-processed documents for RAG -----")

        if documents:
            response, is_response_generated = (
                hosted_llmObj.extract_answers_from_documents(
                    question, intent, documents[DATA]
                )
                if intent in RESPONSE_GENERATION_INTENTS and DATA in documents
                else (documents[DATA], False)
            )
            response = {DATA: response}
        else:
            response = {DATA: documents}
            is_response_generated = False
        logger.info(f"Response from RAG is : {response}")
        augmented_response = helper.augment_response(
            intent,
            response,
            conversation_id,
            tenant_id,
            (
                current_state[STORAGE_SYSTEM_ID]
                if STORAGE_SYSTEM_ID in current_state
                else None
            ),
            is_response_generated,
        )
        logger.info(f"Augmented Response is : {augmented_response}")
        if intent == CHATBOT_CAPABILITIES and (
            augmented_response[MESSAGE] is None or len(augmented_response[MESSAGE]) == 0
        ):
            # Check if data key is present and has a None value
            error_response = {
                STATUS: NO_CONTENT,
                MESSAGE: "No data available for the given request.",
                IDENTIFIER: TEXT,
                DATA: [],
            }
            raise HTTPException(status_code=204, detail=error_response)
        elif intent != CHATBOT_CAPABILITIES and (
            augmented_response[DATA] is None or len(augmented_response[DATA]) == 0
        ):
            augmented_response[DATA] = "No data found for your request. The resource may not be available on your tenant, or no response was received."
            augmented_response[IDENTIFIER] = MARKDOWN
        current_conversation_thread = conversation_history.create_conversation_thread(
            conversation_id, str(question), augmented_response, tenant_id
        )
        conversation_history.store_conversation_history(
            current_conversation_thread,
            current_state,
            conversation_id,
            username,
            tenant_id,
        )

        if (
            error_response is None
            and intent in helper.get_api_list()
            and augmented_response is not None
        ):
            # Append missing entities from current_state to userQuery based on the intent
            updated_question = (
                IntentsAndEntitiesDatabaseOperations.append_missing_entities_to_query(
                    question, current_state, intent
                )
            )
            IntentsAndEntitiesDatabaseOperations.insert_intent_and_entities(
                intent, current_state, username, updated_question, tenant_id
            )

        # if incomplete intent was present and if the control comes here, that means intent was serviced properly,
        # remove it from the list
        # Reset incomplete intent count on successful completion
        if username in incomplete_intent:
            del incomplete_intent[username]
            if username in incomplete_intent_count:
                del incomplete_intent_count[username]
            logger.info(f"Completed intent {intent} for user {username}")
        # delete the key to reset consecutive exception count on a successful response
        if username in consecutive_exception_count:
            del consecutive_exception_count[username]
            logger.info("Reset the consecutive exception count")
    except KeyError:
        # Handle case where "data" key is missing
        error_response = {
            STATUS: INTERNAL_SERVER_ERROR,
            MESSAGE: MISSING_DATA_KEY,
            IDENTIFIER: TEXT,
        }
        raise HTTPException(status_code=500, detail=error_response)
    except HTTPException as ex:
        if (
            ex
            and ex.detail
            and ex.detail[MESSAGE]
            and INCOMPLETE_INTENT_CHECK_STR in ex.detail[MESSAGE]
        ):
            incomplete_intent[username] = intent
            logger.info(f"Added incomplete intent {intent} for user {username}")

            # **Store conversation history when "To proceed, I need the" is present**
            if (
                "To proceed, I need the"
                in ex.detail[MESSAGE]
            ):
                logger.info(
                    f"Incomplete entities detected for user {username}, storing chat history."
                )

                # Get the correct response message from the exception
                response_message = ex.detail[MESSAGE]

                # Create and store the conversation thread for incomplete entities
                augmented_response = helper.augment_response(
                    intent,
                    {MESSAGE: response_message},
                    conversation_id,
                    tenant_id,
                    (
                        entity_dict[STORAGE_SYSTEM_ID]
                        if STORAGE_SYSTEM_ID in entity_dict
                        else None
                    ),
                    True,  # `is_response_generated` is True because the response is complete
                )
                augmented_response[USER_QUERY] = request.userQuery
                augmented_response[IDENTIFIER] = MARKDOWN
                current_conversation_thread = (
                    conversation_history.create_conversation_thread(
                        conversation_id,
                        str(request.userQuery),
                        augmented_response,
                        tenant_id,
                    )
                )
                conversation_history.store_conversation_history(
                    current_conversation_thread,
                    current_state,
                    conversation_id,
                    username,
                    tenant_id,
                )

        logger.error(f"An error occurred: {ex}", ex)
        # track consecutive exceptions
        if username not in consecutive_exception_count:
            consecutive_exception_count[username] = {
                COUNT: 0,
                LAST_EXCEPTION_MESSAGE: None,
            }

        last_exception_message = consecutive_exception_count[username][
            LAST_EXCEPTION_MESSAGE
        ]
        if last_exception_message == ex.detail[MESSAGE]:
            consecutive_exception_count[username][COUNT] += 1
        else:
            consecutive_exception_count[username] = {
                COUNT: 1,
                LAST_EXCEPTION_MESSAGE: ex.detail[MESSAGE],
            }

        # graceful exit if the same exception occurs consecutively
        if consecutive_exception_count[username][COUNT] >= 2:
            logger.error(
                f"Consecutive same exception detected for user {username}, graceful exit.",
                ex,
            )
            # Gracefully exit: clear state, reset incomplete intent, and respond with an apology
            if state_key in global_states:
                del global_states[state_key]
            if username in incomplete_intent:
                del incomplete_intent[username]
            graceful_exit_response = {
                STATUS: BAD_REQUEST,
                MESSAGE: GRACEFUL_EXIT_MESSAGE,
                IDENTIFIER: MARKDOWN,
            }
            # delete after graceful exit
            del consecutive_exception_count[username]
            raise HTTPException(status_code=400, detail=graceful_exit_response)

        # Raise the original exception
        raise ex
    return augmented_response


@app.post("/chatbot/previous_actions")
def previous_actions(
    request: PreviousActionModel
):
    """
    This endpoint returns the latest 5 unique intents along with their entities
    from the 'intents_and_entities' table.
    Args:
        request: The HTTP request object.
    Returns:
        JSON response containing the latest 5 unique intents and entities.
    """
    try:
        # get necessary parameters from user request
        username = request.username
        conversation_id = request.conversation_id or str(uuid.uuid4())
        tenant_id = request.tenant_id

        previous_actions_response = get_latest_unique_intents_and_entities(
            INTENTS_AND_ENTITIES_FOR_PA,
            username,
            conversation_id,
            global_states,
            conversation_history,
            tenant_id,
        )
        previous_actions_data = json.loads(previous_actions_response)
        if previous_actions_data.get(STATUS) == "error":
            error_response = {
                STATUS: ERROR,
                MESSAGE: previous_actions_data.get(MESSAGE),
                IDENTIFIER: TEXT,
            }
            raise HTTPException(status_code=500, detail=error_response)
    except HTTPException as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise ex
    except Exception as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise HTTPException(status_code=500, detail=str(ex))

    return previous_actions_data


@app.post("/chatbot/login")
def login(user_data: UserLoginRequest):
    try:
        decrypted_key = encryption_module.decrypt_value(user_data.api_key)
        user_data_response, error_response, status_code = (
            login_module.login_user(
                user_data.username, user_data.tenant_id, decrypted_key
            )
        )
        message = f"User '{user_data.username}' logged in successfully!"
        return {
            MESSAGE: message,
            USER_DATA: user_data_response,
        }
    except HTTPException as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise ex
    except Exception as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/chatbot/logout")
def logout(request: LogoutRequest):
    try:
        username = request.username
        success_response = {
            MESSAGE: f"User '{username}' logged out!",
            STATUS: SUCCESS_STATUS,
        }
        return success_response
    except HTTPException as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise ex
    except Exception as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/chatbot/get_conversation_history")
def get_conversation_history(
    conversation_id: str,
    username: str,
    tenant_id: str,
):
    """
    Endpoint to delete conversations based on the provided conversation IDs and username.

    Args:
        request (DeleteConversationsRequest): A request object containing the conversation IDs and username.

    Returns:
        dict: A success message indicating the number of conversations deleted.

    Raises:
        HTTPException:
            - 400: If no conversations were deleted or an error occurred during deletion.
            - 500: For any other unexpected errors.
    """
    try:
        conversation_history_list = conversation_history.get_conversation_history(
            conversation_id, username, tenant_id
        )
        return conversation_history_list
    except HTTPException as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise ex
    except Exception as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise HTTPException(status_code=500, detail=str(ex))


@app.put("/chatbot/rename_conversation_title")
def rename_conversation_title(
    user_request: RenameConversationHistoryRequest,
):
    """
    Renames the title of a conversation in the conversation history.

    Parameters:
    - user_request: RenameConversationHistoryRequest
        The request body containing the username, conversation_id, and new_title.

    Returns:
    - JSON response containing the status and message of the operation if successful.

    Raises:
    - HTTPException: If there is an error during the operation.
    """
    try:
        username = user_request.username
        tenant_id = user_request.tenant_id

        conversation_id = user_request.conversation_id
        new_title = user_request.new_title
        response, error_response, STATUS_CODE = (
            conversation_history.update_conversation_title(
                conversation_id, username, new_title, tenant_id
            )
        )
        if response is not None:
            return response
        else:
            raise HTTPException(
                status_code=STATUS_CODE,
                detail=error_response or "Failed to rename conversation title.",
            )
    except HTTPException as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise ex
    except Exception as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise HTTPException(status_code=500, detail=str(ex))


@app.get("/chatbot/get_user_conversation_list")
def get_user_conversation_list(
    username: str, tenant_id: str
):
    """
    Retrieves the list of conversations for a given username.

    Parameters:
    - username: str
        The username of the user whose conversation list is to be retrieved.

    Returns:
    - JSON response containing the list of conversations if successful.

    Raises:
    - HTTPException: If there is an error during the operation.
    """
    try:
        conversation_list, error_response, STATUS_CODE = (
            conversation_history.get_user_conversations(username, tenant_id)
        )
        print(conversation_list)
        if conversation_list is not None:
            return conversation_list
        else:
            raise HTTPException(
                status_code=STATUS_CODE,
                detail=error_response or "Failed to get conversation list.",
            )
    except Exception as ex:
        logger.error(f"An error occured: {ex}", ex)
        raise HTTPException(status_code=500, detail=str(ex))


@app.delete("/chatbot/delete_conversations")
def delete_conversations(
    request: DeleteConversationsRequest
):
    """
    Endpoint to delete conversations based on the provided conversation IDs and username.

    Args:
        request (DeleteConversationsRequest): A request object containing the conversation IDs and username.

    Returns:
        dict: A success message indicating the number of conversations deleted.

    Raises:
        HTTPException:
            - 400: If no conversations were deleted or an error occurred during deletion.
            - 500: For any other unexpected errors.
    """
    try:
        tenant_id = request.tenant_id

        deleted_count, error_response = conversation_history.delete_conversations(
            request.conversation_ids, request.username, tenant_id
        )
        if deleted_count is not None and deleted_count > 0:
            return {MESSAGE: f"{deleted_count} conversations deleted successfully."}
        else:
            raise HTTPException(
                status_code=400,
                detail=error_response
                or "Failed to delete conversations or no matching conversations found.",
            )
    except HTTPException as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise ex
    except Exception as ex:
        logger.error(f"An error occurred: {ex}", ex)
        raise HTTPException(status_code=500, detail=str(ex))


@app.post("/chatbot/execute_action")
def execute_action(
    request: ExecuteActionModel
):
    """
    This endpoint will call the API based on the option selected in the previous actions.
    Args:
        request: {"action": "", "tenant_id": "", "username": "", "conversation_id": "", "api_key": "", "userQuery": ""}
    Returns:
        str: The response from the API call.
    """
    global global_states
    tenant_id = request.tenant_id
    decrypted_api_key = request.api_key
    intent = request.action
    username = request.username
    conversation_id = request.conversation_id or str(uuid.uuid4())
    userQuery = request.userQuery

    try:
        api_key = encryption_module.decrypt_value(decrypted_api_key)
        action_executor = ActionExecutor()
        augmented_response = action_executor.execute_action(
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
        )
        return augmented_response

    except Exception as ex:
        if ex.status_code == 204:
            logger.info(f"No data available for the given request: {ex.detail}")
            error_response = {
                STATUS: NO_CONTENT,
                MESSAGE: "No data available for the given request.",
                IDENTIFIER: MARKDOWN,
                DATA: [],
            }
            raise HTTPException(status_code=500, detail=error_response)
        else:
            logger.error(f"An error occurred: {ex}", ex)
            error_response = {
                STATUS: ERROR,
                MESSAGE: "Oops! Something went wrong on our side. Please try again in a moment.",
                IDENTIFIER: MARKDOWN,
            }
            raise HTTPException(status_code=500, detail=error_response)


@app.post("/chatbot/morning_cup_of_coffee")
def morning_cup_of_coffee(
    request: MorningCupOfCoffeeModel
):
    try:
        global global_states
        username = request.username
        tenant_id = request.tenant_id
        decrypted_api_key = request.api_key
        conversation_id = request.conversation_id or str(uuid.uuid4())

        response_data = []
        api_key = encryption_module.decrypt_value(decrypted_api_key)
        # Iterating over REGISTERED_APIS to find the required APIs by their class names.
        for api in REGISTERED_APIS:
            parameters = {TENANT_ID: tenant_id}
            if api.__name__ == STORAGE_LIST_INFO:
                storage_data_response = api.call(
                    BASE_URL, parameters, api_key, STORAGE_LIST, logger=logger
                )
                error_storage_data = [
                    entry
                    for entry in storage_data_response[DATA]
                    if entry[CONDITION] == ERROR
                ]
                description = (
                    STORAGE_LIST_DESC
                    if error_storage_data
                    else STORAGE_LIST_NO_DATA_DESC
                )
                response_data.append(
                    {
                        INTENT: STORAGE_LIST,
                        DATA: error_storage_data,
                        IDENTIFIER: GRID,
                        DESCRIPTION: description,
                    }
                )
            elif (
                api.__name__ == TENANT_ALERTS_INFO
                or api.__name__ == TENANT_NOTIFICATIONS_INFO
            ):
                parameters.update({SEVERITY: CRITICAL, DURATION: OCCURRENCE})

                if api.__name__ == TENANT_ALERTS_INFO:
                    alert_data = api.call(
                        BASE_URL, parameters, api_key, TENANT_ALERTS, logger=logger
                    )
                    description = (
                        TENANT_ALERTS_DESC
                        if alert_data[DATA]
                        else TENANT_ALERTS_NO_DATA_DESC
                    )
                    response_data.append(
                        {
                            INTENT: TENANT_ALERTS,
                            DATA: alert_data,
                            IDENTIFIER: GRID,
                            DESCRIPTION: description,
                        }
                    )
                elif api.__name__ == TENANT_NOTIFICATIONS_INFO:
                    notification_data = api.call(
                        BASE_URL,
                        parameters,
                        api_key,
                        TENANT_NOTIFICATIONS,
                        logger=logger,
                    )
                    description = (
                        TENANT_NOTIFICATIONS_DESC
                        if notification_data[DATA]
                        else TENANT_NOTIFICATIONS_NO_DATA_DESC
                    )
                    response_data.append(
                        {
                            INTENT: TENANT_NOTIFICATIONS,
                            DATA: notification_data,
                            IDENTIFIER: GRID,
                            DESCRIPTION: description,
                        }
                    )

        state_key = (conversation_id, username)
        current_state = global_states.get(state_key)
        current_conversation_thread = conversation_history.create_conversation_thread(
            conversation_id, str(MORNING_CUP_OF_COFFEE), response_data, tenant_id
        )
        current_conversation_thread[ROUTINE] = MORNING_CUP_OF_COFFEE_ROUTINE
        conversation_history.store_conversation_history(
            current_conversation_thread,
            current_state,
            conversation_id,
            username,
            tenant_id,
        )
        augmented_response = {
            CONVERSATION_ID: conversation_id,
            DATA: response_data,
            ROUTINE: MORNING_CUP_OF_COFFEE_ROUTINE,
        }
        return augmented_response
    except Exception as ex:
        logger.error(f"An error occurred: {ex}", ex)
        error_response = {
            STATUS: INTERNAL_SERVER_ERROR,
            MESSAGE: MISSING_PARAMETER_MORNINGCUP_ROUTINE,
            IDENTIFIER: TEXT,
        }
        raise HTTPException(status_code=500, detail=error_response)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
