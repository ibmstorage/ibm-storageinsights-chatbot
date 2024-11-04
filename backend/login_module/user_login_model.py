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

from pydantic import BaseModel


class UserLoginRequest(BaseModel):
    """
    Pydantic model representing the request body for user login.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    username: str
    tenant_id: str
    api_key: str


class UserLoginDataResponse(BaseModel):
    """
    Pydantic model representing the response body containing user data.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user.
    """

    username: str
    tenant_id: int


class UserLoginResponse(BaseModel):
    """
    Pydantic model representing the response body for user login.

    Attributes:
        message (str): A message indicating the result of the login attempt.
        user_data (UserLoginDataResponse): The data of the logged-in user.
    """

    message: str
    user_data: UserLoginDataResponse


class LogoutRequest(BaseModel):
    username: str
