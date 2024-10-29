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

from backend.utils.Helpers import Helpers
from backend.external_apis import REGISTERED_APIS
from backend.constants.PromptConstants import *
from backend.constants.constants import SYSTEM_ID_ASSERTION, METRIC_TYPE_ASSERTION

helper = Helpers(REGISTERED_APIS)
# Method to dynamically fetch API list
intent_list = helper.get_api_list()
intent_list.append(SYSTEM_ID_ASSERTION)
intent_list.append(METRIC_TYPE_ASSERTION)
# Converting the list to a formatted string
formatted_intent_list = ", ".join(intent_list)

# Granite system message
system_message = """You are Granite Chat, an AI language model developed by IBM. You are a cautious assistant. You carefully follow instructions. You are helpful and harmless and you follow ethical guidelines and promote positive behavior."""
querius_system_message = "Hello! I'm Querius, your GenAI assistant dedicated to simplifying storage observability. My mission is to help you gain insights into your Storage Systems registered within your Storage Insights tenant."

intent_template = f"""
<|system|>
{{system_message}}
<|user|>
Assign a label to the given sentence. The label must be one of the following: [{formatted_intent_list}]
If the input is an introductory salutation like "hi", "hello", "good morning", "good evening" or similar, then assign [greetings]. If the input is a goodbye message or a thanking remark, assign [thanking]. If the input asks which storage system needs attention, focus, or review, assign [morning-cup-of-coffee]. If the input does not fit into any of these labels, you should assign [unknown]. Assign only one label to the sentence.
Your response should only include the answer. Do not prepend or append anything else. Do not provide any further explanation.
Note: The terms 'systems' and 'devices' are synonymous and should be treated as referring to the same entity. For any query related to hardware failure, ensure the intent is mapped to [tenant-notifications]. If the input sentence only includes a storage system UUID (formatted as a UUID), the label should be [system-id-assertion]. If the input sentence only includes a metric type (e.g., "port_send_io_rate", "ip_replication_latency") or any metric-related term without other detailed information, assign the label [metric-type-assertion]. If the input sentence seems related to documentation, such as questions about "how to" or "what to do," then assign the label [unknown]. Also, Questions regarding opening or closing of tickets should be mapped to [unknown].

For all other cases, carefully assess the content of the sentence to determine the correct label from the provided list.

Here are some examples, complete the last one:
sentence:
Enumerate the storage systems available to the tenant.
label:
[storage-list]

sentence:
get me all the storage systems managed by this tenant
label:
[storage-list]

sentence:
show me the storage systems in error or disconnected state
label:
[storage-list]

sentence:
show me the alerts for the tenant for the past 20 days?
label:
[tenant-alerts] 

sentence:
What are the info notifications for my tenant in 10d?
label:
[tenant-notifications]

sentence:
Retrieve details of the storage system 32606980-7983-11ee-b7a5-af40c0807045
label:
[storage-system-details]

sentence:
Can you tell me about any information notifications for svc2a in the last 10 days?
label:
[storage-system-notification]

sentence:
How many pools and disks are currently in use across my storage systems?
label:
[storage-list]

sentence:
list down the storage systems for the tenant
label:
[storage-list]

sentence:
Is the percentage of mapped capacity less than 25% for any of the storage systems?
label:
[storage-list]

sentence:
What are the severity info notifications for system 93be4120-7983-11ee-9bbe-a32462b6c5c5 for this tenant in last 10d?
label:
[storage-system-notification]

sentence:
What are the severity info alerts for system ca4c4d00-7a04-11ee-9bbe-a32462b6c5c5 in 10d?
label:
[storage-system-alert]

sentence:
Hey, good morning!
label:
[greetings]

sentence:
good evening
label:
[greetings]

sentence:
Sure, the system ID is 12fae123-456b-789c-0d12-3e45f67a89bc
label:
[system-id-assertion]

sentence:
89bcf123-d456-78e9-a0f1-23b4c567890a
label:
[system-id-assertion]

sentence:
Umm, storage d67a1b23-e01f-4c58-8b34-a4312456a789
label:
[system-id-assertion]

sentence:
Show me the alerts for storage system 4c7dcde0-e386-11ee-b2e1-cfddfe51829e with a severity of warning
label:
[storage-system-alert]

sentence:
what are the volumes for the system ca4c4d00-7a04-11ee-9bbe-a32462b6c5c5 which belongs to my tenant?
label:
[storage-system-volume]

sentence:
what is the health status or data collection status of system flash7200
label:
[storage-system-details]

sentence:
what is the performance metrics with type volume_overall_read_io_rate data for the storage system with b2351490-e386-11ee-b679-61f24598a983 for this tenant for the last 18 hours
label:
[storage-system-metric]

sentence:
show me volume utilization for system e92dcfb0-2b01-11ef-807f-8fd7eb980b28
label:
[storage-system-metric]

sentence:
what are your capabilities?
label:
[chatbot-capabilities]

sentence:
What can you assist me with?
label:
[chatbot-capabilities]

sentence:
Can you provide me with the list of volumes for 44d144f0-9c23-11ec-b909-0242ac120002?
label:
[storage-system-volume]

sentence:
I need to check the available volumes for my tenant on 72b81230-9a25-4a7d-817f-7a002cb3f283
label:
[storage-system-volume]

sentence:
Show me the volume details for 5b49d360-7b4f-11eb-9439-0242ac130002 linked to my account
label:
[storage-system-volume]

sentence:
Can you check the data collection status for system flash9000?
label:
[storage-system-details]

sentence:
Tell me the overall health and performance of APM00145042834
label:
[storage-system-details]

sentence:
when was the last successful probe for system a7ece550-02d3-11ef-ba9c-f1cd529d5b67
label:
[storage-system-details]

sentence:
I want to know about the current health status of a storage system?
label:
[storage-system-details]

sentence:
Retrieve volume read response time metric for f4a6b5a0-7a06-11eb-9439-0242ac130002 for the past month
label:
[storage-system-metric]

sentence:
Can you give me the volume_write_transfer_size for system 73c145e0-9a25-4a7d-817f-7a002cb3f283 over the last 10 days?
label:
[storage-system-metric]

sentence:
I need the volume overall total cache hit percentage for a system
label:
[storage-system-metric]

sentence:
The storage system UUID is 9bc0a1f2-3d45-6789-b012-34567c8d90ab
label:
[system-id-assertion]

sentence:
It’s 1abc234d-567e-890f-a123-45678bc9d012
label:
[system-id-assertion]

sentence:
i do not know the storage system
label:
[system-id-assertion]

sentence:
usable capacity
label:
[metric-type-assertion]

sentence:
CPU utilization
label:
[metric-type-assertion]

sentence:
port receive response time
label:
[metric-type-assertion]

sentence:
Which storage system needs my attention?
label:
[morning-cup-of-coffee]

sentence: 
do I need to worry about any systems in my fleet?
label:
[morning-cup-of-coffee]

sentence:
Anything to worry about my block storage systems?
label:
[morning-cup-of-coffee]

sentence:
Which storage system in my fleet should be prioritised?
label:
[morning-cup-of-coffee]

sentence:
Should I have coffee or tea today ?
label:
[unknown]

sentence:
where is my coffee ?
label:
[unknown]

sentence:
Which of my storage systems have less than 10% available capacity?
label:
[storage-list]

sentence:
Show me the systems with a condition marked as error or warning
label:
[storage-list]

sentence:
List all storage systems where the available capacity is over 90%
label:
[storage-list]

sentence:
Give me the systems that have unmapped capacity greater than 50%
label:
[storage-list]

sentence:
What are the systems that have the probe status as failed or device unreachable?
label:
[storage-list]

sentence:
Can you show me the systems with more than 50 volumes?
label:
[storage-list]

sentence:
Which systems have overprovisioned capacity greater than 7 TB?
label:
[storage-list]

sentence:
Do any systems have capacity issues today?
label:
[storage-list]

sentence:
List all storage systems where the remote relationships count is higher than 0
label:
[storage-list]

sentence:
Show me the systems with a snapshot provisioned capacity over 500 GB
label:
[storage-list]

sentence:
Which storage systems have a data reduction savings percentage of 0?
label:
[storage-list]

setence:
show me systems which are all healthy
label:
[storage-list]

sentence:
are there any devices for which i need to change the credentials
label:
[storage-list]

sentence:
display all the systems which are enabled for ransomware threat detection
label:
[storage-list]

sentence:
show warranty expired storage systems
label:
[unknown]

sentence:
When do I have to increase my storage capacity?
label:
[unknown]

sentence:
type is filesystem write transfer size
label:
[metric-type-assertion]

sentence:
okay, metric is volume overall read cache hit percentage
label:
[metric-type-assertion]

sentence:
Its disk read response time
label:
[metric-type-assertion]

sentence:
What is the available system capacity and used capacity percent for storage system tpcv5k4?
label:
[storage-system-details]

sentence:
Can you provide the status and IP address of the storage system 6565f4a0-1675-11ef-9ec0-6976616010e2?
label:
[storage-system-details]

sentence:
How many volumes and pools are currently managed by the storage system with serial number 000000C020427C18?
label:
[storage-system-details]

sentence:
What are the compression savings and provisioned capacity percent for storage system 9b9adce0-02d2-11ef-ba9c-f1cd529d5b67?
label:
[storage-system-details]

sentence:
What is the current probe status and last successful probe time for system 059f59a0-1687-11ef-9ec0-6976616010e2
label:
[storage-system-details]

sentence:
How much available volume capacity and unmapped capacity is there in my storage system?
label:
[storage-system-details]

sentence:
What is the current drive compression ratio and total provisioned capacity for my storage system
label:
[storage-system-details]

sentence:
What are the disk and IP port counts for my storage system?
label:
[storage-system-details]

sentence:
Have there been any critical alerts been detected on this tenant?
label:
[tenant-alerts]

sentence:
Are there any policy violations detected in my tenant's storage systems?
label:
[tenant-alerts]

sentence:
Which resources have generated the most alerts in the tenant recently?
label:
[tenant-alerts]

sentence:
Are there any info-level alerts about datastores in my tenant?
label:
[tenant-alerts]

sentence:
have any of my systems reported ransomware attack?
label:
[tenant-alerts]

sentence:
Is there any report of a ransomware attack?
label:
[tenant-alerts]

sentence:
any ransomware attack
label:
[tenant-alerts]

sentence:
Show me all alerts with multiple violations for my tenant's resources
label:
[tenant-alerts]

sentence:
Can you show me all the alerts regarding removed datastores?
label:
[tenant-alerts]

sentence:
Are there any general alerts triggered by VMware policies in my tenant?
label:
[tenant-alerts]

sentence:
Do I have any tenant-wide alerts for multiple violations on storage systems?
label:
[tenant-alerts]

sentence:
Are there systems flagged with a ransomware threat alert?
label:
[tenant-alerts]

sentence:
What recent critical alerts have been triggered by my datastores?
label:
[tenant-alerts]

sentence:
Are there any new info-level alerts for removed paths across my tenant?
label:
[tenant-alerts]

sentence:
Can you show me critical alerts for probe status errors on my Unity storage system?
label:
[storage-system-alert]

sentence:
What are the latest alerts for policy violations on my storage system?
label:
[storage-system-alert]

sentence:
Has any critical alert been detected on my system?
label:
[storage-system-alert]

sentence:
Do I have any critical alerts for my Dell EMC Unity system?
label:
[storage-system-alert]

sentence:
What alerts are related to removed HBAs in my system a7ece550-02d3-11ef-ba9c-f1cd529d5b67?
label:
[storage-system-alert]

sentence:
Have there been any alerts for my storage system related to policy compliance errors?
label:
[storage-system-alert]

sentence:
What alerts have been triggered by errors in 84767d70-1674-11ef-bdaa-49bc6e244688 probes?
label:
[storage-system-alert]

sentence:
Are there any alerts related to general category issues on my storage system
label:
[storage-system-alert]

sentence:
which systems are eligible ransomware alerts?
label:
[unknown]

sentence:
Which are the system with expired warranty
label:
[unknown]

sentence:
Which systems are eligible to receive ransomware alerts?
label:
[unknown]

sentence:
What issues have been detected with the probe status on system c4b6dab0-1674-11ef-bdaa-49bc6e244688 ?
label:
[storage-system-alert]

sentence:
show me critical alerts
label:
[tenant-alerts]

sentence:
Are there any alerts associated with degraded volumes?
label:
[tenant-alerts]

sentence:
Do any degraded volumes have alerts
label:
[tenant-alerts]

sentence:
Is there any system with Ransomware threat alert? 
label:
[tenant-alerts]

sentence:
Can you tell me the number of remote relationships and the condition of my storage system?
label:
[storage-system-details]

sentence:
which of my systems are healthy?
label:
[storage-list]

sentence:
Is there any system which is out of sync ?
label:
[storage-list]

sentence:
are there any system running out of capacity today?
label:
[storage-list]

sentence:
Which are the systems that will be running out of capacity soon?
label:
[storage-list]

sentence:
show me systems with firmware version greater than 7.8
label:
[storage-list]

sentence:
Do i have to change credentials for any of the system?
label:
[storage-list]

sentence:
Show me the system with top concern ..
label:
[storage-list]

sentence:
show me top 3 systems with power utilization
label:
[unknown]

sentence:
Can you display the systems by power consumption?
label:
[unknown]

sentence:
Give me top 5 systems with highest temperature
label:
[unknown]

sentence:
Which are the systems with the highest temperature?
label:
[unknown]

sentence:
How to configure call home for e92dcfb0-2b01-11ef-807f-8fd7eb980b28
label:
[unknown]

sentence:
Have there been any unacknowledged tickets opened in the last 24 hours?
label:
[tenant-notifications]

sentence:
Which tickets are marked as info severity for my storage systems?
label:
[tenant-notifications]

sentence:
Are any tickets for the SAN Volume Controller pending acknowledgment?
label:
[tenant-notifications]

sentence:
Can you show me the details of ticket TS017190771?
label:
[unknown]

sentence:
Is there any system with disk errors?
label:
[tenant-notifications]

sentence:
check if there is a system with disk errors
label:
[tenant-notifications]

sentence:
What is the latest ticket reported for my storage systems?
label:
[unknown]

sentence:
Which storage systems have expired warranties?
label:
[unknown]

sentence:
what tickets are closed
label:
[unknown]

sentence:
what open tickets i have
label:
[unknown]

sentence:
When was the last successful Call Home event for the storage system 0413c050-1676-11ef-8775-f5d2d6b10a60
label:
[storage-system-notification]

sentence:
Has the event on 10-07-2024 for device UKStand4-FS5045 for system uuid 04d5c910-167c-11ef-bdaa-49bc6e244688 been acknowledged?
label:
[storage-system-notification]

sentence:
Does system 059f59a0-1687-11ef-9ec0-6976616010e2 have reported events with the info_acknowledged severity?
label:
[storage-system-notification]

sentence:
can you tell me about the events of a storage system
label:
[storage-system-notification]

sentence:
which are all the important notifications for my system 060ce930-f0cf-11ee-8dc2-35cfb00490ae?
label:
[storage-system-notification]

sentence:
which are my closed tickets
label:
[unknown]

sentence:
Has a ransomware attack been detected on any system?
label:
[tenant-alerts]

sentence:
Do any of the systems have ransomware threat alerts? 
label:
[tenant-alerts]

sentence:
How many alerts are unacknowledged
label:
[tenant-alerts]

sentence:
I want to get the warning severity alerts for my storage
label:
[storage-system-alert]

sentence:
What are the systems have acknowledged Call Home events?
label:
[tenant-notifications]

sentence:
tell me about the storage systems have reported events with the info_acknowledged severity?
label:
[tenant-notifications]

sentence:
How many events were recorded for storage systems in the last month?
label:
[tenant-notifications]

sentence:
{{question}}
label:"""

entity_template = """
<|system|>
{system_message}
<|user|>
For each sentence, perform named entity recognition (NER) and tag the entities according to the following categories:

- storage_system_id : A unique system ID. This entity will always represent a unique identifier which must be a 32-character hexadecimal string in the format `8-4-4-4-12` (e.g., `123e4567-e89b-12d3-a456-426614174000`). Do not tag any other alphanumeric strings as `storage_system_id`.
- system_name: The name of a storage system. This entity represents a descriptive or user-defined name for a storage system, distinct from the storage_system_id. It may contain a mix of letters, numbers, hyphens, underscores, or spaces. Examples include: Names with prefixes and alphanumeric combinations: "2107.75AHG91", "SVC-svc4", "tpcflash9100".  Simple alphanumeric names: "GDLSVT10", "XIV_D 7811012", "V9000-tpcv9k1", "tpccluster1", "v7000-storea", "FLYER 7825410" and others of similar type. System names do not follow the 8-4-4-4-12 hexadecimal format and are more descriptive in nature. Ensure that these names do not get confused with storage_system_id.
- severity : The severity level can only be one of the following - critical, critical_acknowledged, warning, warning_acknowledged, info, info_acknowledged.
- duration : The duration, which ends with 'd/D' for days, 'h/H' for hours, or 'm/M' for minutes.
- types :The metric types, which must be in the format of lowercase words separated by underscores. Examples include used_capacity, usable_capacity, available_capacity, cpu_utilization, volume_utilization, volume_overall_read_io_rate, volume_overall_write_io_rate, volume_read_data_rate, volume_write_data_rate, gc_moved_size ,etc.

Response Instructions:
Your response must consist only of the detected entities and their corresponding tags within a dictionary structure. If you cannot confidently detect any of the four entities, you must return an empty dictionary `{{}}`. Ensure the `storage_system_id` is an ID following a structured pattern of `8-4-4-4-12`. If it does not meet this criterion, do not tag it as `storage_system_id`. 
Under no circumstances should you generate any text or outputs other than the dictionary. If no entities are detected, the only valid output is `{{}}`. Do not reuse, infer, or generate any tags based on the provided examples. Only respond based on the current input sentence. Examples provided are strictly for instructional purposes and should not be referenced in your response. 

Here are some examples, complete the last one:

Input Sentence:
what are the info notifications for my tenant for the past 20 days
Tags:
{{"severity":"info", "duration":"20d"}}

Input Sentence:
Provide details about device 98765432-1234-5678-abcd-123456789abc associated with this tenant
Tags:
{{"storage_system_id":"98765432-1234-5678-abcd-123456789abc"}}

Input Sentence:
show me the volumes for system e8958560-e386-11ee-b2e1-cfddfe51829e
Tags:
{{"storage_system_id":"e8958560-e386-11ee-b2e1-cfddfe51829e"}}

Input Sentence:
show me alerts on this tenant for last 15 days
Tags: 
{{"duration":"15d"}}

Input Sentence:
fetch the critical alerts for storage system e8958560-e386-11ee-b2e1-cfd123e51829e for last 10 hours
Tags:
{{"storage_system_id":"e8958560-e386-11ee-b2e1-cfd123e51829e", "severity":"critical", "duration":"10h"}}

Input Sentence:
what is the performance metrics with type volume overall read io rate data for the system b2351490-e386-11ee-b679-61f24598a983 for the tenant for the last 10d
Tags:
{{"storage_system_id":"b2351490-e386-11ee-b679-61f24598a983", "types":"volume_overall_read_io_rate", "duration":"10d"}}

Input Sentence:
what is the ip replication compressed receive data rate for 059f59a0-1687-11ef-9ec0-6976616010e2 for the tenant for the last twelve days
Tags:
{{"storage_system_id":"059f59a0-1687-11ef-9ec0-6976616010e2", "types":"ip_replication_compressed_receive_data_rate", "duration":"12d"}}

Input Sentence:
show me used capacity graph for system svc3c
Tags:
{{"types":"used_capacity", "system_name":"svc3c"}}

Input Sentence:
i need help with 2 things, can you tell me about the informational alert details of system uuid e92dcfb0-2b01-11ef-807f-8fd7eb980b28 and secondly tell me if there are any ransomware alerts on this tenant that are concerning?
Tags:
{{"storage_system_id":"e92dcfb0-2b01-11ef-807f-8fd7eb980b28", "severity":"info"}}

Input Sentence:
are there any systems in error condition?
Tags:
{{}}

Input Sentence:
For my DS8800 device, what is the ip replication total transfer size and how many info acknowledged alerts there are over the past 9 hours?
Tags:
{{"system_name":"DS8800", "types":"ip_replication_total_transfer_size", "severity": "info_acknowledged", "duration": "9h"}}

Input Sentence:
are there any alerts on this tenant
Tags:
{{}}

Input Sentence:
are their any warning acknowledged notifications for my tenant
Tags:
{{"severity":"warning_acknowledged"}}

Input Sentence:
give me all systems on this tenant
Tags:
{{}}

Input Sentence:
get me critical acknowledged notification if any for the past couple of hours
Tags:
{{"severity":"critical_acknowledged", "duration":"2h"}}

Input Sentence:
is my ip replication latency greater than 5 ms?
Tags:
{{"types":"ip_replication_latency"}}

Input Sentence:
give me details of all devices associated with this tenant
Tags:
{{}}

Input Sentence:
give me details about the metric ip replication latency for the past three hours on system tpcflash5200-2 and also if any warning acknowledged notifications have been received
Tags:
{{"types": "ip_replication_latency", "duration": "3h", "system_name":"tpcflash5200-2 ", "severity":"warning_acknowledged"}}

Input Sentence:
give me details of any of the systems associated with this tenant
Tags:
{{}}

Input Sentence:
when was the port send io rate the lowest in past couple of hours
Tags:
{{"types":"port_send_io_rate", "duration":"2h"}}

Input Sentence:
what is the volume unmapped volumes data rate for my system ?
Tags:
{{"types":"volume_unmapped_volumes_data_rate"}}

Input Sentence:
is my ip replication latency greater than 5 ms?
Tags:
{{"types":"ip_replication_latency"}}

Input Sentence:
does v7000-storea have any volume-related details in the past 22 hours
Tags:
{{"system_name":"v7000-storea", "duration":"22h"}}

Input Sentence:
get me the disk read data rate for 069c5840-167c-11ef-8c9a-bd1292ca37cd
Tags:
{{"types":"disk_read_data_rate", "storage_system_id": "069c5840-167c-11ef-8c9a-bd1292ca37cd"}}

Input Sentence:
07688d90-6099-11ef-859d-47e83a51569d
Tags:
{{"storage_system_id": "07688d90-6099-11ef-859d-47e83a51569d"}}

Input Sentence:
show me usable capacity for e545b430-1675-11ef-bdaa-49bc6e244688
Tags:
{{"types":"usable_capacity", "storage_system_id": "e545b430-1675-11ef-bdaa-49bc6e244688"}}

Input Sentence:
give me the warning alerts in past one hour for SVC-perfsvc1 which has id 51ad7e60-c75b-11ee-a416-b3b5584372fa
Tags:
{{"severity":"warning", "duration": "1h", "system_name":"SVC-perfsvc1", "storage_system_id": "51ad7e60-c75b-11ee-a416-b3b5584372fa"}}

Input Sentence:
give me all systems on this tenant
Tags:
{{}}

Input Sentence:
list me the alerts on tpcflash900b
Tags:
{{"system_name":"tpcflash900b"}}

Input Sentence:
Does a7ece550-02d3-11ef-ba9c-f1cd529d5b67  have any volume related details in the past 10 days
Tags:
{{"storage_system_id": "a7ece550-02d3-11ef-ba9c-f1cd529d5b67", "duration": "10d"}}

Input Sentence:
{question}
Tags:"""

common_intents_template = f"""
<|system|>
{querius_system_message}

### Capabilities
I currently use a pre-configured set of Storage Insights APIs to assist you with the following:
- **Tenant Alerts and Notifications**: Retrieve alerts and notifications related to your tenant.
- **Storage Systems**: Access details, metrics, alerts, volumes, and notifications for your registered storage systems.

### Limitations
- My responses are limited to the APIs I currently have access to.
- I am restricted to answering queries related to storage observability and cannot assist with inquiries beyond this scope.

*Instructions*:

#### Response Guidelines:

1. **Respond Only to Greetings or Thanking Messages**: For any user input, respond only if it contains a greeting or a thanking message. Do not handle other intents, and do not provide responses outside of greetings and thanking.
2. **Friendly and Jovial Tone**: For greetings or thanking intents, generate a friendly and positive response in a jovial tone based on the user input.
3. **No Mention of Documentation**: Do not provide or reference any documentation, links, or instructions related to external documents.
4. **User Input Independence**: Treat each user input and response independently. Do not refer to previous interactions.
5. **Prohibited Responses**: Never respond with phrases like:
   - "Let me fetch that for you."
   - "I will retrieve the information."
   - Any statement suggesting actions beyond responding to greetings or thanking messages
6. **Direct and Relevant Responses**: Keep responses concise and focused on the input.
7. **No Assumptions or Hallucinations**: Never generate responses or actions based on fabricated information or assumptions.

### Examples:

<|user|>
Intent: greetings
User Input: Hello there!
<|assistant|>
Hey! How can I help with your storage systems today?

<|user|>
Intent: greetings
User Input: Good morning!
<|assistant|>
Good morning! Ready to dive into your storage systems? Let me know how I can assist!

<|user|>
Intent: greetings
User Input: Hey Querius!
<|assistant|>
Hey! How can I make your storage observability easier today?

<|user|>  
Intent: greetings  
User Input: hii...What are your constraints?
<|assistant|>
Sure thing! My current capabilities allow me to interact with storage insights APIs to gather data such as alerts, notifications, system details, metrics, etc. However, please note that I don't possess the ability to perform external tasks or access resources outside of these APIs.

<|user|>
Intent: thanking
User Input: Thanks a lot!
<|assistant|>
You’re very welcome! I’m here if you need any more help with your storage systems!

<|user|>  
Intent: thanking  
User Input: I appreciate your help.  
<|assistant|>  
Glad I could help! Don’t hesitate to ask if you need more assistance.

<|user|>
Intent: thanking
User Input: gotta goooo
<|assistant|>
Bye! Don't hesitate to reach out if you need help with anything else.

<|user|>
Intent: greetings
User Input: What's up, Querius?
<|assistant|>
Not much, just here to help! How can I assist you with your storage systems today?

<|user|>
Intent: greetings
User Input: good evening! what are your limitations?
<|assistant|>
Good evening! My focus is on assisting with storage observability-related queries using the APIs I have access to. I’m unable to help with tasks or questions outside of this scope.

<|user|>
Intent: greetings
User Input: Hiii buddy
<|assistant|>
Hey there! How can I assist you with your storage systems today?

<|user|>
Intent: thanking
User Input: thanks, you've been great
<|assistant|>
It’s my pleasure! Don’t hesitate to reach out if you need more assistance!

<|user|>
Intent: thanking
User Input: see you soon
<|assistant|>
Take care! Don't hesitate to reach out if you have any questions or concerns about your storage systems.

<|user|>
Intent: greetings
User Input: hows it going mate
<|assistant|>
It's going well! How can I assist you with your storage systems today?

<|user|>
Intent: greetings
User Input: heyy good morning, what can you do for me today?
<|assistant|>
Heyy! I'm here to assist with your storage observability needs. How can I help you with your storage systems today?

<|user|>
Intent: {{intent}}
User Input: {{question}}
<|assistant|>"""

response_generation_template = f"""{BEGIN_OF_TEXT}{START_HEADER_ID}{SYSTEM}{END_HEADER_ID} You are an AI language model 
designed to function as a specialized Retrieval Augmented Generation (RAG) assistant. You are not good at mathematical 
calculations such as counting, addition, subtraction, multiplication, or division. If the user asks for any form of 
calculation, politely inform them that you cannot perform math operations accurately. Generate responses in proper 
sentences as a human would. When generating responses, prioritize correctness, i.e., ensure that your response is 
correct given the context and user query, and that it is grounded in the context. Furthermore, make sure that the 
response is supported by the given tenant or context.If the tenant is empty, respond with a contextually appropriate 
statement indicating that there is no data available to answer the question.Refrain from adding anything else to your 
response when the tenant is empty. Always make sure that your response is relevant to the question.
For example, if the user query is 'are there any systems in error state' and if the tenant is empty, your response 
should say that the tenant is not managing any storage systems. For example, if the user asks for alerts of a tenant and
the tenant is empty, your response should say that there are no alerts present taking into consideration the context
of user query.

If an explanation is needed, first provide the explanation or reasoning, and then give the final answer.

You are a markdown expert, generate responses using markdown formatting, H3 (###), and lower-level headings, but avoid 
using H1 (#) and H2 (##). Include other markdown elements like bold, italics, lists, links, and code blocks as needed. 
For important notes or references, use block quotes (>) to draw attention to the text. Examine the question and decide 
whether you should answer in a tabular format or not. Replace the word 'document' in your response with 'tenant'.
Think step by step but do not provide steps in the answer.
{{intent_specific_instructions}}
[Document] {{documents}} [End] {END_OF_TURN}{START_HEADER_ID}{USER}{END_HEADER_ID}{{question}}{END_OF_TURN}
{START_HEADER_ID}{ASSISTANT}{END_HEADER_ID}"""

storage_list_response_generation_instructions = """Below document gives list of storage systems, you should only 
answer questions about storage systems from given document. If you are asked about alerts or notifications for the 
tenant or a storage system, the answer is not present in the below document. Your response should always contain 
storage system id and storage system name in addition to whatever fields you choose to add.Replace pm_status with 
Performance monitor status in your response. If a user asks a question like "Which systems are nearing 100 percent 
capacity," use the used_capacity_percent field to generate the response. Only include systems where 
used_capacity_percent is strictly greater than 80%. Do not include any systems with used_capacity_percent 
less than or equal to 80% under any circumstance. If no systems meet the criteria, respond with 
'No systems are nearing 100 percent capacity.'. If a user asks question like 'how many systems is my tenant managing', 
first provide the details and then provide correct count. When you are asked questions that need comparison like 
'show me systems which are running out of capacity?', think step by step, provide detailed data first and then filter the data"""

storage_system_detail_response_generation_instructions = """Below document gives details of storage systems, 
you should only answer questions about a particular storage system from given document. If you are asked about alerts 
or notifications for the tenant or a storage system, the answer is not present in the below document. If you are 
asked about any storage system other than the one mentioned in the document, the answer is not present in the below 
document.Your response should always contain storage system id and storage system name in addition to whatever fields 
you choose to add.Replace pm_status with Performance monitor status in your response"""

tenant_alert_response_generation_instructions = """Below document provides details about alerts that were received on 
a tenant. You should answer questions only about alerts for a tenant or for a storage system. Your answer should 
always include following fields: alert id, parent resource name, alert name, severity, occurrence time, source of the 
alert, creator of the alert in addition to whatever fields you choose to add. If you are asked about notifications, 
details about a system, below document does not provide that answer."""

storage_system_alert_response_generation_instructions = """Below document provides details about alerts that were 
received for a storage system. Answer to the user query is present in the document. You should answer questions only 
about alerts for a storage system. Your answer should always include following fields: alert id, parent resource 
name, alert name, severity, occurrence time, source of the alert, creator of the alert in addition to whatever fields 
you choose to add. If you are asked about notifications, details about a system, below document does not provide that 
answer."""

storage_system_notification_response_generation_instructions = """Below document provides details about notifications 
that were received for a storage system. Answer to the user query is present in the document. You should answer 
questions only about notifications for a storage system. Your answer should always include following fields: 
notification id, parent resource name, severity, occurrence time in addition to whatever fields you choose to add. If 
you are asked about alerts, details about a system, below document does not provide that answer."""

tenant_notification_response_generation_instructions = """Below document provides details about notifications that 
were received for the tenant. You should answer questions only about notifications for a tenant or for a storage 
system. Your answer should always include following fields: event, id, time, device name, serial number, 
more information, whether the event is acknowledged or not in addition to whatever fields you choose to add. If you 
are asked about alerts, details about a system, below document does not provide that answer."""
