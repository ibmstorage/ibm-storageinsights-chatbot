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

from backend.constants.constants import EPSILON_SUMMARY, MESSAGE, STATUS
from backend.external_apis.Template import API


class ChatbotCapabilities(API):
    name = "chatbot-capabilities"
    description = "Lists out the capabilities that the chatbot has to the user"

    @classmethod
    def _invoke_and_validate(cls, base_url, parameters, api_key, logger):
        return {STATUS: 200, MESSAGE: EPSILON_SUMMARY}
