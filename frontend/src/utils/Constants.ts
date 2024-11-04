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

export const maxAPIkeyLength = 1;
export const BOT = 'bot';
export const USER = 'user';
export const GIB = 'GIB';
export const exportTableFilename = 'SI_table_data';

export const dataIdentifier = {
  grid: 'grid',
  grids: 'grids',
  chart: 'chart',
  properties: 'properties',
  buttons: 'buttons',
  markdown: 'markdown',
};

export const beColumnList = {
  lastDataCollection: 'last_data_collection',
  occurenceTime: 'occurenceTime',
  time: 'time',
  condition: 'condition',
};

export const columnListMap: any = {
  'tenant-notifications': [
    'device_name',
    'event',
    'severity',
    'time',
    'more_information',
  ],
  'storage-system-notification': [
    'device_name',
    'event',
    'severity',
    'time',
    'more_information',
  ],
  'storage-system-volume': [
    'name',
    'volume_id',
    'storage_system',
    'status_label',
    'last_data_collection',
    'capacity_bytes',
    'pool_name',
    'raid_level',
    'used_capacity_bytes',
  ],
  'tenant-alerts': [
    'name',
    'category',
    'condition',
    'occurenceTime',
    'parentResource',
    'severity',
    'source',
    'violation',
  ],
  'storage-system-details': [
    'name',
    'condition',
    'vendor',
    'type',
    'model',
    'firmware',
    'ip_address',
  ],
  'storage-list': [
    'name',
    'condition',
    'vendor',
    'type',
    'model',
    'firmware',
    'ip_address',
    'storage_system_id',
  ],
  'storage-system-alert': [
    'name',
    'category',
    'condition',
    'occurenceTime',
    'parentResource',
    'severity',
    'source',
    'violation',
  ],
};

export const intentDescMap: any = {
  'tenant-notifications':
    "I'm unable to give you a precise answer due to the large amount of data, but here's a detailed response for you.",
  'storage-system-notification':
    "I'm unable to give you a precise answer due to the large amount of data, but here's a detailed response for you.",
  'storage-system-volume':
    'All set! I found the storage volumes you requested. Dive in and explore!',
  'tenant-alerts': "I'm unable to give you a precise answer due to the large amount of data, but here's a detailed response for you.",
  'storage-system-details':
    'Just like you asked, I pulled up the information on your storage system.',
  'storage-system-alert': "I'm unable to give you a precise answer due to the large amount of data, but here's a detailed response for you.",
  'storage-list': "I'm unable to give you a precise answer due to the large amount of data, but here's a detailed response for you.",
  'storage-system-metric':
    'Just like you asked, I pulled up the metrics information on your storage system.',
  'chatbot-capabilities':
    'Epsilon simplifies tenant management by conveniently organizing all your tenants and their notifications. It offers comprehensive access to alerts, metrics, storage volumes, and notifications for your storage systems. Additionally, it provides detailed insights into each storage system in your inventory and assists with capacity-related inquiries, ensuring seamless management.',
};

export const intentActionsMap = {
  'used-usable-capacity': 'Used Usable Capacity',
  'storage-system-alert': 'Storage System Alert',
  'storage-system-volume': 'Storage System Volume',
  'tenant-alerts': 'Tenant Alerts',
  'storage-system-details': 'Storage System Details',
  'storage-system-metric': 'Storage System Metrics',
  'storage-system-notification': 'Storage System Notification',
  'storage-list': 'Storage List',
  'tenant-notifications': 'Tenant notifications',
  'chatbot-capabilities': 'Chatbot Capabilities',
  'morning-cup-of-coffee': 'Morning cup of coffee',
};

export const intentEmptyDataMap = {
  'tenant-notifications': 'No data received from Storage Insights for this.',
  'storage-system-notification':
    'No data received from Storage Insights for this.',
  'storage-system-volume': 'No data received from Storage Insights for this.',
  'tenant-alerts': 'No data received from Storage Insights for this.',
  'storage-system-details': 'No data received from Storage Insights for this.',
  'storage-system-alert': 'No data received from Storage Insights for this.',
  'storage-list': 'No data received from Storage Insights for this.',
  'tenant-list': 'No data received from Storage Insights for this.',
  'storage-system-metric': 'No data received from Storage Insights for this.',
};

export const conditionMapping = {
  info: 'Informational',
  warning: 'Warning',
  critical: 'Critical',
  info_acknowledged: 'Informational - Acknowledged',
  warning_acknowledged: 'Warning - Acknowledged',
  critical_acknowledged: 'Critical - Acknowledged',
  error: 'Error',
  normal: 'Normal',
  unconfigured: 'Unconfigured',
  unknown: 'Unknown',
  Unreachable: 'Device Unreachable',
  unreachable_acknowledged: 'Unreachable - Acknowledge',
};

// login form
export const LOGIN_NOTIFICATION_TIMEOUT = 5000;
export const LOGIN_SUCCESS_NOTIFICATION_TIMEOUT = 3000;

// settings panel
export const NOTIFICATIONS_TIMEOUT = 12_000;

// forgot password notification
export const NOTIFICATIONS_TIMER = 2000;
export const ICON_SIZE = 20;
export const FORGOT_PASSWORD = 'ForgotPassword';
export const UPDATE_SECURITYQUESTIONS = 'UpdateSecurityQuestions';
export const UPDATE_PASSWORD = 'UpdatePassword';

// logout
export const SUCCESS_STATUS = 'SUCCESS';

// carbon dark theme
export const DARK_THEME_CONSTANT = 'g100';

// routine
export const MORNING_CUP_OF_COFFEE_ROUTINE = 'morning-cup-of-coffee';
export const EXECUTE_PERVIOUS_ACTIONS_ROUTINE = 'execute-pervious-actions';
export const GET_PERVIOUS_ACTIONS_ROUTINE = 'get-pervious-actions';

// status code
export const UNAUTHORIZED_STATUS_CODE = 401;
export const ERR_BAD_RESPONSE = 'ERR_BAD_RESPONSE';
export const ERR_BAD_REQUEST = 'ERR_BAD_REQUEST';

// Help Documentation Link
export const IBM_DOCS_STORAGE_INSIGHTS_URL =
  'https://www.ibm.com/docs/en/storage-insights?topic=overview-storage-insights';
