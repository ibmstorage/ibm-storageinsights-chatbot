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

from backend.external_apis import REGISTERED_APIS


class APIController:
    """
    This class will call appropriate api based on user intent.
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.apis = {api.name: api for api in REGISTERED_APIS}
        # self.parameter_names = set.union(*[set(api.parameters.keys()) for api in self.apis.values()])
        self.parameter_names = set()
        for api in self.apis.values():
            if api.parameters:
                self.parameter_names.update(api.parameters.keys())

    def call(self, action, parameters, api_key, logger):
        return self.apis[action].call(self.base_url, parameters, api_key, action, logger)
