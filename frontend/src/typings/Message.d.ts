/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

export interface Message {
  text: string; // Text content of the bot message
  sender: string; // Bot identifier, e.g., "BOT"
  identifier?: string; // Optional identifier for the message
  data?: any; // Can be any type, depends on the response data structure
  intent?: string; // Optional intent of the message
  id?: number; // Unique identifier, generated using Date.now()
  loading?: boolean; // Loading state of the message
  link?: any; // Optional link associated with the message
}
