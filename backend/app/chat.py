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

from backend.logging_module.Logging import Logging
class ChatController:
    def __init__(self, api_controller):
        self.api_controller = api_controller

    def update_states(self, states, parameters, logger: Logging):
        for parameter_name, new_value in parameters.items():
            old_value = states.get(parameter_name, "None")
            states[parameter_name] = new_value
            logger.info("Updating %s: %s -> %s" % (parameter_name, old_value, new_value))
        return states

    def invoke_API(self, action, states, api_key, logger):
        result = ""
        print(self, action)
        if action != "unknown":
            result = self.api_controller.call(action, states, api_key, logger)

        return result
