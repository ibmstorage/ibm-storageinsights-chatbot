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
from backend.prompt.prompts import response_generation_template


class ResponseGenerationPromptManager:
    def __init__(self):
        """
        Initializes the ResponseGenerationPromptManager with a prompt template.
        """
        self.prompt = PromptTemplate(
            template=response_generation_template,
            input_variables=["question", "documents", "intent_specific_instructions"],
        )

    def get_response_generation_prompt(self):
        """
        Returns the prompt template.

        Returns:
            PromptTemplate: The prompt template initialized with the given intent.
        """
        return self.prompt
