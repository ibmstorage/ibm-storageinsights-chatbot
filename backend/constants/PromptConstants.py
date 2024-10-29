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

# llama prompt special tokens
BEGIN_OF_TEXT = "<|begin_of_text|>"
START_HEADER_ID = "<|start_header_id|>"
END_HEADER_ID = "<|end_header_id|>"
END_OF_TURN = "<|eot_id|>"

# LLM roles
SYSTEM = "system"
USER = "user"
ASSISTANT = "assistant"

# Context length
LLAMA_INPUT_CONTEXT_LENGTH = 128000  # 125k context size instead of 128k to accommodate output tokens
