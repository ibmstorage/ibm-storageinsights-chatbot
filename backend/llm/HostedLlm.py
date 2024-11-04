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
from typing import Any

from fastapi import HTTPException
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from langchain_ibm import WatsonxLLM

from backend.constants.PromptConstants import LLAMA_INPUT_CONTEXT_LENGTH
from backend.constants.constants import *
from backend.prompt import prompts
from backend.prompt.CommonIntentsPromptManager import CommonIntentsPromptManager
from backend.prompt.EntityDetectionPromptManager import EntityDetectionPromptManager
from backend.prompt.IntentDetectionPromptManager import IntentDetectionPromptManager
from backend.prompt.ResponseGenerationPromptManager import (
    ResponseGenerationPromptManager,
)
from backend.utils.Helpers import Helpers
from backend.utils.ResponseGenerationHelpers import get_instructions_for_intent

intent_detection_parameters = {
    GenTextParamsMetaNames.DECODING_METHOD: GREEDY,
    GenTextParamsMetaNames.MAX_NEW_TOKENS: FIFTEEN,
    GenTextParamsMetaNames.STOP_SEQUENCES: INTENT_DETECTION_STOP_SEQUENCE,
    GenTextParamsMetaNames.MIN_NEW_TOKENS: ONE,
    GenTextParamsMetaNames.REPETITION_PENALTY: ONE,
    GenTextParamsMetaNames.RANDOM_SEED: 42,
}

entity_extraction_parameters = {
    GenTextParamsMetaNames.DECODING_METHOD: GREEDY,
    GenTextParamsMetaNames.MAX_NEW_TOKENS: HUNDRED,
    GenTextParamsMetaNames.STOP_SEQUENCES: ENTITY_EXTRACTION_STOP_SEQUENCE,
    GenTextParamsMetaNames.MIN_NEW_TOKENS: ONE,
    GenTextParamsMetaNames.REPETITION_PENALTY: ONE,
    GenTextParamsMetaNames.RANDOM_SEED: 42,
}

common_user_intents_parameters = {
    GenTextParamsMetaNames.DECODING_METHOD: GREEDY,
    GenTextParamsMetaNames.MAX_NEW_TOKENS: 100,
    GenTextParamsMetaNames.MIN_NEW_TOKENS: ONE,
    GenTextParamsMetaNames.STOP_SEQUENCES: ["\n\n"],
    GenTextParamsMetaNames.REPETITION_PENALTY: 1.2,
    GenTextParamsMetaNames.RANDOM_SEED: 5,
}

response_generation_parameters = {
    GenTextParamsMetaNames.DECODING_METHOD: GREEDY,
    GenTextParamsMetaNames.MAX_NEW_TOKENS: 4096,
    GenTextParamsMetaNames.MIN_NEW_TOKENS: 0,
    GenTextParamsMetaNames.STOP_SEQUENCES: [],
    GenTextParamsMetaNames.REPETITION_PENALTY: 1,
    GenTextParamsMetaNames.TEMPERATURE: 0.0,
    GenTextParamsMetaNames.RANDOM_SEED: 5,
}


class HostedLlm:

    def __init__(self):
        """
        Constructor to load the intent detection and entity extraction models
        using IBM Watsonx hosted service.
        """
        # Initialize Granite for Intent Detection
        self.llm = WatsonxLLM(
            model_id=GRANITE_34B_CODE_INSTRUCT,
            url=os.getenv(WATSONX_HOSTED_SERVICE),
            project_id=os.getenv(PROJECT_ID),
            params=intent_detection_parameters,  # Initial parameters for intent detection
        )
        # Initialize Granite for Entity Detection
        self.entity_llm = WatsonxLLM(
            model_id=GRANITE_34B_CODE_INSTRUCT,
            url=os.getenv(WATSONX_HOSTED_SERVICE),
            project_id=os.getenv(PROJECT_ID),
            params=entity_extraction_parameters,  # Initial parameters for entity detection
        )
        self.common_response_handler_llm = WatsonxLLM(
            model_id=GRANITE_34B_CODE_INSTRUCT,
            url=os.getenv(WATSONX_HOSTED_SERVICE),
            project_id=os.getenv(PROJECT_ID),
            params=common_user_intents_parameters,
        )
        self.response_llm = WatsonxLLM(
            model_id=LLAMA_3_405B_INSTRUCT,
            url=os.getenv(WATSONX_HOSTED_SERVICE),
            project_id=os.getenv(PROJECT_ID),
            params=response_generation_parameters,
        )
        self.response_llm_tokenizer = ModelInference(
            model_id=LLAMA_3_405B_INSTRUCT,
            credentials=Credentials(
                api_key=os.getenv(WATSONX_APIKEY), url=os.getenv(WATSONX_HOSTED_SERVICE)
            ),
            project_id=os.getenv(PROJECT_ID),
        )
        self.helper = Helpers()
        # Initialize the IntentDetectionPromptManager and EntityDetectionPromptManager
        self.prompt_manager = IntentDetectionPromptManager()
        self.entity_manager = EntityDetectionPromptManager()
        self.common_intents_manager = CommonIntentsPromptManager()
        self.response_generation_manager = ResponseGenerationPromptManager()

    def set_parameters(self, parameters):
        """
        Method to update the LLM parameters dynamically.
        :param parameters: A dictionary of parameters to be set.
        """
        self.llm.params = parameters
        
    def handle_token_quota_error(self, ex):
        """
        Handles the token quota error and raises an HTTPException with a user-friendly message.
        :param ex: The original exception caught during the LLM invocation.
        """
        # Check if the exception has a response
        if hasattr(ex, 'response') and ex.response is not None:
            status_code = ex.response.status_code
            
            try:
                error_data = ex.response.json()
            except ValueError:
                print("Error parsing JSON response. Defaulting error_data to empty.")
                error_data = {}  # If JSON parsing fails, use an empty dict

        # Check for specific error code and status code
        if status_code == 403 and error_data["errors"][0]["code"] == "token_quota_reached":
            message = (
                f"You've used all your free tokens for this month's Watsonx API. "
                f"Tokens will refresh next month. To continue using the service without interruption, you can upgrade your plan or purchase additional tokens. "
                f"For additional information, visit: https://cloud.ibm.com/apidocs/watsonx-ai"
            )
            raise HTTPException(
                status_code=403,
                detail={
                    STATUS: "Forbidden",
                    MESSAGE: message,
                    IDENTIFIER: MARKDOWN
                },
            )
            
        error_response = {
            STATUS: NO_CONTENT,
            MESSAGE: f"Apologies, I'm currently unable to generate a response due to an issue. Please try again "
            f"later.",
            IDENTIFIER: TEXT,
            DATA: [],
        }
        raise HTTPException(status_code=503, detail=error_response)

    def get_intent_of_utterance(self, user_utterance) -> str | None:
        """
        Method to detect intent from the given user utterance using Watsonx.
        :param user_utterance: The input string from the user.
        :return: Intent of the user utterance.
        """
        try:
            if not user_utterance:
                return UNKNOWN

            # Get the intent detection prompt template and format it
            prompt_template = self.prompt_manager.get_intent_prompt()
            input_prompt = prompt_template.format(
                system_message=prompts.system_message, question=user_utterance
            )

            # Call the hosted LLM to get intent classification
            response = self.llm.invoke(input_prompt)

            # Parse and return the intent from the response
            if response:
                return self.helper.parse_output(response)
            else:
                return UNKNOWN
        except Exception as ex:
            print(f"Error encountered while trying to detecting intents. {str(ex)}")
            self.handle_token_quota_error(ex)

    def extract_entities_from_utterance(self, user_utterance) -> dict:
        """
        Method to extract entities from user utterance using Watsonx.
        :param user_utterance: The input string from the user.
        :return: dict containing all the entities in the user utterance or an empty dict if result is None.
        """
        try:
            entities = {}

            if user_utterance:

                # Get the entity detection prompt template and format it
                prompt_template = self.entity_manager.get_entity_detection_prompt()
                input_prompt = prompt_template.format(
                    system_message=prompts.system_message, question=user_utterance
                )

                # Call the hosted LLM to extract entities
                response = self.entity_llm.invoke(input_prompt)

                # Convert the response string into a dictionary
                result = self.helper.LLMOutputToDict(response)

                # Check if the result is None or dictionary is empty
                if not result:
                    return {}

                # Create the entities dictionary from the result
                entities = self.helper.filter_entities_from_result(result, user_utterance)

            return entities
        except Exception as ex:
            print(f"Error encountered while trying to extracting entities. {str(ex)}")
            self.handle_token_quota_error(ex)
        
    def common_intents_response_generator(self,intent_detected, user_utterance) -> dict:
        """
        Method to handle response generation of common intents like thanking, greetings using llm.
        :param intent_detected: The intent detected.
        :param user_utterance: The input string from the user.
        :return: dict containing the response based on user intent or an empty dict if no valid response is generated.
        """
        try:
            # Initialize response dictionary
            final_response = {}
            if user_utterance:
                prompt = self.common_intents_manager.get_common_intent_handler_prompt()
                input_prompt = prompt.format(
                    intent=intent_detected,
                    question=user_utterance
                )
                # Call the LLM to generate response for general user intent
                response = self.common_response_handler_llm.invoke(input_prompt)
                if response:
                    response = response.strip()
                    # Update the response with the specific format
                    final_response.update(
                        {
                            f"{INTENT}": f"{intent_detected}",
                            f"{DATA}": f"{response}",
                        }
                    )
                else:
                    final_response.update(
                        {
                            f"{INTENT}": f"{intent_detected}",
                            f"{DATA}": f"{EPSILON_SUMMARY}",
                        }
                    )
            return final_response
        except Exception as ex:
            print(f"Error encountered while trying to generate common intents message using llm. {str(ex)}")
            self.handle_token_quota_error(ex)

    def extract_answers_from_documents(
        self, question, intent, documents
    ) -> tuple[Any, bool] | tuple[str, bool]:
        """
        Method to pass the api response, prompt and user query to the llm and extract proper answer
        :param question: user query
        :param intent: intent for which the document were fetched
        :param documents: api response for the identified intent
        :return: String containing the answer to the user query
        """
        try:
            prompt_template = (
                self.response_generation_manager.get_response_generation_prompt()
            )
            instructions = get_instructions_for_intent(intent)
            input_prompt = prompt_template.format(
                question=question,
                documents=documents,
                intent_specific_instructions=instructions,
            )
            # calculate the number of tokens in input prompt, if the tokens are more than size of context window,
            # do not pass the input prompt to the llm and return the documents directly to be shown as table.
            tokenized_response = self.response_llm_tokenizer.tokenize(
                prompt=input_prompt, return_tokens=True
            )
            if tokenized_response["result"]["token_count"] > LLAMA_INPUT_CONTEXT_LENGTH:
                return documents, False
            response = self.response_llm.invoke(input_prompt)
            return response.strip(), True
        except Exception as ex:
            print(f"Error encountered while trying to generate response. {str(ex)}")
            self.handle_token_quota_error(ex)
