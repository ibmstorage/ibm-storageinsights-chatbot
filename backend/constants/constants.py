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

# external apis constants
STORAGE_LIST = "storage-list"
STORAGE_SYSTEM_DETAILS = "storage-system-details"
TENANT_NOTIFICATIONS = "tenant-notifications"
STORAGE_SYSTEM_VOLUME = "storage-system-volume"
TENANT_LIST = "Tenant-List"
USED_USABLE_CAPACITY = "used-usable-capacity"
TENANT_ALERTS = "tenant-alerts"
STORAGE_SYSTEM_METRIC = "storage-system-metric"
STORAGE_SYSTEM_NOTIFICATIONS = "storage-system-notification"
STORAGE_SYSTEM_ALERTS = "storage-system-alert"
CHATBOT_CAPABILITIES = "chatbot-capabilities"
GREETINGS = "greetings"
THANKING = "thanking"
UNKNOWN = "unknown"
METADATA = "metadata"
SYSTEM_ID_ASSERTION = "system-id-assertion"
METRIC_TYPE_ASSERTION = "metric-type-assertion"

# user request constants
SESSION_ID = "session_id"
USER_QUERY = "userQuery"
TENANT_ID = "tenant_id"
API_KEY = "api_key"
PREVIOUS_API_KEY = "previous-api-key"
NEW_API_KEY = "new-api-key"
ACTION = "action"
ENTITIES = "entities"
RESPONSE = "Below, you'll find a curated list of some of the actions you've recently undertaken! Check them out:"

# user response constants
INTENT = "intent"
IDENTIFIER = "identifier"
GRID = "grid"
PROPERTIES = "properties"
CHART = "chart"
TEXT = "text"
MARKDOWN = "markdown"
MESSAGE = "message"
STATUS = "status"
DESCRIPTION = "description"
PREVIOUS_ACTIONS = "previous_actions"
BUTTONS = "buttons"
USER_DATA = "user_data"
LINK = "link"

# hosted llm parameter
INTENT_DETECTION_STOP_SEQUENCE = ["]"]
ENTITY_EXTRACTION_STOP_SEQUENCE = ["}", "\n\n"]
GREEDY = "greedy"
FIFTEEN = 15
HUNDRED = 100
ONE = 1
WATSONX_APIKEY = "WATSONX_APIKEY"
GRANITE_34B_CODE_INSTRUCT = "ibm/granite-34b-code-instruct"
LLAMA_3_405B_INSTRUCT = "meta-llama/llama-3-405b-instruct"
WATSONX_HOSTED_SERVICE = "WATSONX_HOSTED_SERVICE"
PROJECT_ID = "PROJECT_ID"
SECRET_KEY = "SECRET_KEY"

# morning cup of coffee routine descriptions and constants
STORAGE_LIST_DESC = "Here are the storage systems with Error condition on your tenant"
TENANT_ALERTS_DESC = (
    "Here are the critical alerts identified within the last 24-hour period."
)
TENANT_NOTIFICATIONS_DESC = (
    "Here are the critical notifications for your tenant from the last 24 hours."
)
STORAGE_LIST_NO_DATA_DESC = "These are the storage systems that have an Error condition"
TENANT_ALERTS_NO_DATA_DESC = "There were no alerts generated during the last 24 hours."
TENANT_NOTIFICATIONS_NO_DATA_DESC = (
    "There were no notifications generated during the last 24 hours."
)
DATA = "data"
SEVERITY = "severity"
CONDITION = "condition"
ERROR = "error"
CRITICAL = "critical"
DURATION = "duration"
OCCURRENCE = "1d"
STORAGE_LIST_INFO = "StorageList"
TENANT_ALERTS_INFO = "TenantAlerts"
TENANT_NOTIFICATIONS_INFO = "TenantNotifications"

# execute action
NO_ENTITIES = "No entities found for the specified intent"

# chatbot capabilities
EPSILON_SUMMARY = """
Hello! I'm your GenAI assistant dedicated to simplifying storage observability. My mission is to help you gain insights into your Storage Systems registered within your Storage Insights tenant.\n\n

### Capabilities\n\n

I currently use a pre-configured set of Storage Insights APIs to assist you with the following:\n\n
- **Tenant Alerts and Notifications**: Retrieve alerts and notifications related to your tenant.\n\n
- **Storage Systems**: Access details, metrics, alerts, volumes and notifications for your registered storage systems.\n\n
- **Here are the specific APIs I currently support**:\n\n
  1. Storage system alerts\n
  2. Storage system metrics\n
  3. Storage system notifications\n
  4. Storage system list\n
  5. Tenant alerts\n
  6. Tenant notifications\n
  7. Storage system volumes\n
  8. Storage system details\n\n

### Limitations\n\n

- My responses are limited to the APIs I currently have access to.\n\n
- I am restricted to answering queries related to storage observability and cannot assist with inquiries beyond this scope.\n\n

### Future Enhancements\n\n

For smoother conversations, I try my best to retain the context of previous queries. In future versions, I will have access to more data sources and enhanced conversational abilities.\n"""


# graceful exit message
GRACEFUL_EXIT_MESSAGE = """
Apologies, it seems I'm currently unable to fully process your request.\n\n

This may be due to a missing parameter, an error in identifying the correct intent, or switching intents without completing the previous one. Please clarify your request, or if you're unsure about my capabilities, simply type:\n\n

**`"show me your capabilities"`**\n\n

I'm here to assist you in the best possible way!
"""

COUNT = "count"
LAST_EXCEPTION_MESSAGE = "last_exception_message"
# Thank you message
MORNING_CUP_OF_COFFEE_ROUTINE_RESPONSE_MESSAGE = (
    "Getting you morning essential routine details"
)

# Thank you message
THANKING_RESPONSE_MESSAGE = "You're welcome! Glad I could assist. If you have any more questions or need anything else, feel free to ask."
# Error messages
MISSING_PARAMETER = (
    "Please provide a valid query (either of tenantID or api key is missing)."
)
MISSING_QUERY = "It looks like you didn't enter anything. How can I assist you today?"
UNKNOWN_INTENT = """
Oops! I'm unable to understand your query. My current capability allows fetching data with a limited subset of Storage Insights REST APIs. If you're unsure about my capabilities, simply type:\n\n

**`"show me your capabilities"`**\n\n

Feel free to ask or try rephrasing your query. I'm ready whenever you are!
"""
NO_DATA = "Data retrieval failed. Please try again later."
MISSING_DATA_KEY = "That's a great question! Unfortunately, the data you requested seems unavailable at the moment. Would you like me to try searching for something related?"
MISSING_PARAMETER_MORNINGCUP_ROUTINE = "Please provide valid parameters (either of tenantID or api key or Username is missing)."

# Error status
RESOURCE_NOT_FOUND = "HTTP 404 Not Found"
NO_CONTENT = "No Content"
INTERNAL_SERVER_ERROR = "Internal Server Error"
BAD_REQUEST = "Bad Request"
VALIDATION_ERROR = "Validation Error"
# register user
USERNAME_EXISTS_MESSAGE = (
    "Username already exists. Please log in if you already have an account."
)
EMAIL_EXISTS_MESSAGE = "An account with this email already exists. Please log in if you already have an account."
REGISTRATION_FAILED_MESSAGE = "Failed to register user."
STATUS_CODE = "status_code"
RENAME_UNSUCCESSFUL = "There was a issue while changing the title. Please try again"
ERROR_GETTING_CONVERSATION_HISTORY = (
    "There was a issue while getting the conversation history"
)
ERROR_GETTING_CONVERSATION_LIST = (
    "There was a issue while getting the conversation list"
)
# API Management
UPDATE_API_MESSAGE = "API key updated successfully"
RECORD_NOT_FOUND = (
    "Record not found. No such API exists with the provided tenantID and username."
)
INVALID_REQUEST = "Invalid request data or database error"
NOT_FOUND = "Not Found"
SUCCESS = "success"
API_KEY_ID = "api_key_id"
EXISTING_ROLE_MESSAGE = (
    "A user with the same tenant ID, username and role already exists"
)
API_KEY_ADDED_MESSAGE = "API key added successfully"
DATABASE_ERROR = "Unexpected database error"
API_KEY_DELETED_MESSAGE = "API key deleted successfully"
UNAUTHORIZED = "Unauthorized"
API_DOES_NOT_MATCH = "Provided API key does not match the stored one"
NO_API_KEY_FOUND = "No API keys found for the given username"
MISSING_USERNAME = "Missing required key (USERNAME) in request body."
API_KEYS = "api_keys"
ENCRYPTION_KEY_FILE = "/app/database/encryption_key.txt"
API_KEY_DETAILS = "api_key_details"
INVALID_API_KEY = (
    "Either tenant id or api key is not correct, please check tenant id or api key"
)
ERROR_ADDING_API_KEY = "There seems to be a problem adding the API key. The API key format is likely invalid. Please ensure it follows the correct format and try again."
ERROR_EDITING_API_KEY = "There seems to be a problem editing the API key. Please ensure all fields are filled correctly, including username, tenant ID, and new API key."
ERROR_DELETING_API_KEY = "There seems to be a problem deleting the API key. The API key format is likely invalid. Please ensure it follows the correct format and try again."
DATABASE_ERROR_MESSAGE = "We're encountering a database issue at the moment. Please try again later, or contact support if the issue persists."
INAVLID_SYSTEM_NAME = """
**System Not Found**\n\n
The storage system you mentioned is not present for the specified tenant. Please double-check the system name or ID and try asking your question again.
"""

USERNAME = "username"
ROLE = "user-role"

# login user
INVALID_CREDENTIALS_MESSAGE = (
    "Login failed. Please enter a valid API key for your tenant and try again.",
)
LOGIN_COUNT = "login_count"
USER_LOGOUT_FAILED = "failed to logout user"
USER_NOT_LOGGED_IN = "User not logged in"
FIRST_NAME = "first_name"
EMAIL = "email"
IS_NEWUSER = "is_NewUser"

# security qustions
USERNAME_DOES_NOT_EXISTS_MESSAGE = (
    "Username does not exist. Please provide valid username."
)
WRONG_SECURITY_ANSWERS = (
    "Wrong answers entered. Please provide the answers used while registration"
)
SUCCESS_STATUS = "SUCCESS"
SECURITY_QUESTION_1 = "security_question_1"
SECURITY_QUESTION_2 = "security_question_2"

# update password
UPDATE_PASSWORD_FAILED_MESSAGE = "Failed to update password"

# chat history
CONVERSATION_ID = "conversation_id"
ROUTINE = "routine"
MORNING_CUP_OF_COFFEE_ROUTINE = "morning-cup-of-coffee"
MORNING_CUP_OF_COFFEE = "morning cup of coffee"
EXECUTE_PREVIOUS_ACTIONS_ROUTINE = "execute-pervious-actions"
GET_PREVIOUS_ACTIONS_ROUTINE = "get-pervious-actions"
# Intent and entity extraction
STORAGE_SYSTEM_ID = "storage_system_id"
SYSTEM_NAME = "system_name"
TYPES = "types"

# LLM results
LABEL = "label"
ENTITY_GROUP = "entity_group"
UUID = "UUID"
DUR = "DUR"
SEV = "SEV"
SERIAL = "SERIAL"
METRIC = "METRIC"
WORD = "word"
DAYS_VARIATION = ("days", "day")
HOURS_VARIATION = ("hours", "hour", "hrs", "hr")
MINUTES_VARIATION = ("minutes", "min", "mins")
INFORMATIONAL_ACK_VARIATIONS = (
    "informational-acknowledge",
    "informational acknowledge",
    "information acknowledge",
    "info acknowledged",
)
SEVERITY_VARIATIONS = (
    "info acknowledged",
    "critical acknowledged",
    "warning acknowledged",
)
WARNING_ACK_VARIATIONS = ("warning acknowledged", "warning-acknowledged")
CRITICAL_ACK_VARIATIONS = ("critical acknowledged", "critical-acknowledged")

# Regex pattern
VALID_DURATION_PATTERN = r"\b\d+[dDhHmM]\b"
VALID_UUID_REGEX = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"

# External API parameter possible values
VALID_SEVERITIES = [
    "warning",
    "critical",
    "info",
    "error",
    "info_acknowledged",
    "warning_acknowledged",
    "critical_acknowledged",
]
VALID_METRIC_TYPE = [
    "volume_overall_read_io_rate",
    "volume_overall_write_io_rate",
    "volume_overall_total_io_rate",
    "volume_unmapped_volumes_io_rate",
    "volume_overall_read_cache_hit_percentage",
    "volume_overall_write_cache_hit_percentage",
    "volume_overall_total_cache_hit_percentage",
    "volume_read_data_rate",
    "volume_write_data_rate",
    "volume_total_data_rate",
    "volume_unmapped_volumes_data_rate",
    "volume_read_transfer_size",
    "volume_write_transfer_size",
    "volume_total_transfer_size",
    "volume_write-cache_delay_percentage",
    "volume_read_response_time",
    "volume_write_response_time",
    "volume_total_response_time",
    "volumes_unmapped_response_time",
    "volume_host_time_percentage",
    "volume_utilization",
    "disk_read_io_rate",
    "disk_write_io_rate",
    "total_disk_io_rate",
    "disk_read_data_rate",
    "disk_write_data_rate",
    "disk_total_data_rate",
    "disk_read_response_time",
    "disk_write_response_time",
    "disk_total_response_time",
    "port_send_io_rate",
    "port_receive_io_rate",
    "total_port_io_rate",
    "port_send_data_rate",
    "port_receive_data_rate",
    "port_total_data_rate",
    "port_send_response_time",
    "port_receive_response_time",
    "port_total_response_time",
    "ip_replication_transfer_send_size",
    "ip_replication_transfer_receive_size",
    "ip_replication_transfer_total_size",
    "ip_replication_latency",
    "ip_replication_to_remote_node_send_data_rate",
    "ip_replication_to_remote_node_receive_data_rate",
    "ip_replication_to_remote_node_re_send_data_rate",
    "ip_replication_compressed_send_data_rate",
    "ip_replication_compressed_receive_data_rate",
    "physical_node_send_data_rate",
    "physical_node_receive_data_rate",
    "physical_node_total_data_rate",
    "node_logical_send_data_rate",
    "node_logical_receive_data_rate",
    "node_logical_total_data_rate",
    "cpu_utilization",
    "gc_moved_size",
    "node_read_cache_fullness",
    "node_write_cache_fullness",
    "max_node_read_cache_fullness",
    "max_node_write_cache_fullness",
    "filesystem_and_node_read_io",
    "filesystem_and_node_write_io",
    "filesystem_and_node_total_io",
    "filesystem_and_node_bytes_read",
    "filesystem_and_node_bytes_write",
    "filesystem_and_node_bytes_total",
    "filesystem_read_response_time",
    "filesystem_write_response_time",
    "filesystem_total_response_time",
    "filesystem_read_transfer_size",
    "filesystem_write_transfer_size",
    "filesystem_total_transfer_size",
    "available_capacity",
    "used_capacity",
    "usable_capacity",
]

# HTTP headers
X_API_TOKEN = "x-api-token"
ACCEPT = "Accept"
APPLICATION_JSON = "application/json"
X_API_KEY = "x-api-key"
X_INTEGRATION = "x-integration"
X_INTEGRATION_VERSION = "x-integration-version"
STORAGE_INSIGHTS_CHATBOT = "si-chatbot"
VERSION = "v1"

# Miscellaneous
BASE_URL = "https://insights.ibm.com/restapi/v1/"
INCOMPLETE_INTENT_CHECK_STR = "To proceed, I need the"
SI_BASE_URL = "https://insights.ibm.com/gui/"

# Intent description
intentDescMap = {
    TENANT_NOTIFICATIONS: "I understand you are looking for tenant notifications",
    STORAGE_SYSTEM_NOTIFICATIONS: "I understand you are looking for the notifications belonging to a storage system",
    STORAGE_SYSTEM_VOLUME: "I understand you are looking for the volumes associated with a particular storage system",
    TENANT_ALERTS: "I got that you are looking for the the alerts that your tenant is having",
    STORAGE_SYSTEM_DETAILS: "I got that you are looking for the system's details",
    STORAGE_SYSTEM_ALERTS: "I understand you are looking for the alerts associated with a storage system",
    STORAGE_LIST: "I understand you are looking for the list of storage systems belonging to your tenant",
    TENANT_LIST: "I understand you are looking for the list of tenants that you have",
    STORAGE_SYSTEM_METRIC: "I understand you are looking for the metrics information on your storage system",
    CHATBOT_CAPABILITIES: "I understand that you want to know what are my capabilities",
}

INTERNAL_SERVER_ERROR_MORNINGCUP_OF_COFFEE = (
    "Oops!Something went wrong from our end.Please try again later"
)

# Database table names
USER_DATA_DB = "/app/database/user_data.db"
API_KEY_DATABASE = "/app/database/api_key_database.db"
INTENTS_AND_ENTITIES_FOR_PA = "/app/database/previous_actions.db"
CONVERSATION_HISTORY_DB = "/app/database/conversation_history.db"

# log constants
CONTAINER_MOUNT_POINT = "/app/logging/"
LOG_FORMATTER = (
    "%(levelname)s - %(asctime)s - %(threadName)s (%(thread)d) - %(message)s"
)

# API response keys
TIMESTAMP_FIELDS = (
    "last_successful_probe",
    "last_successful_monitor",
    "occurenceTime",
    "startTimestamp",
    "endTimestamp",
    "occurrenceTimeInMs",
    "timeStamp",
    "time",
)
RESPONSE_GENERATION_INTENTS = (
    STORAGE_LIST,
    TENANT_NOTIFICATIONS,
    TENANT_ALERTS,
    STORAGE_SYSTEM_NOTIFICATIONS,
    STORAGE_SYSTEM_ALERTS,
    STORAGE_SYSTEM_DETAILS,
)
