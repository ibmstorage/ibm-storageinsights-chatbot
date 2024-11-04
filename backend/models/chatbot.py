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

from typing import Optional

from pydantic import BaseModel


class RunChatbotModel(BaseModel):
    """
    Pydantic model representing the request body for running user query.

    Attributes:
        "userQuery" (str): Query user has asked
        "tenant_id" (str): Configured tenant id
        "username" (str): Configured username
        "api_key" (str): Configured api key
        "conversation_id" (Optional[str]): Current conversation id
    """
    userQuery: str
    tenant_id: str
    api_key: str
    username: str
    conversation_id: Optional[str] = None


class ExecuteActionModel(BaseModel):
    """
    Pydantic model representing the request body for execute action.

    Attributes:
        "tenant_id" (str): Configured tenant id.
        "username" (str): Configured username.
        "conversation_id" (Optional[str]): Current conversation id
        "api_key" (str): Configured api key
        "action" (str): Action to execute
        "userQuery" (str): The specific query made by the user, used to fetch entities for the action.
    """
    tenant_id: str
    username: str
    conversation_id: Optional[str] = None
    api_key: str
    action: str
    userQuery: str


class MorningCupOfCoffeeModel(BaseModel):
    """
    Pydantic model representing the request body for morning cup of coffee routine.

    Attributes:
        "tenant_id" (str): Configured tenant id.
        "username" (str): Configured username.
        "conversation_id" (Optional[str]): Current conversation id
        "api_key" (str): Configured api key
    """
    tenant_id: str
    username: str
    conversation_id: Optional[str] = None
    api_key: str


class PreviousActionModel(BaseModel):
    """
    Pydantic model representing the request body for morning cup of coffee routine.

    Attributes:
        "username" (str): Configured username.
        "tenant_id" (str): Configured tenant id.
        "conversation_id" (Optional[str]): Current conversation id
    """
    username: str
    tenant_id: str
    conversation_id: Optional[str] = None
    tenant_id: str
