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

from langchain_core.prompts import PromptTemplate
from backend.prompt import prompts

class IntentDetectionPromptManager:
    def __init__(self):
        """
        Initializes the IntentDetectionPromptManager with a prompt template.

        Args:
            intent (str): The template string for intent detection.
        """
        self.prompt = PromptTemplate(
            template=prompts.intent_template,
            input_variables=["system_message","question"]
        )

    def get_intent_prompt(self):
        """
        Returns the prompt template.

        Returns:
            PromptTemplate: The prompt template initialized with the given intent.
        """
        return self.prompt