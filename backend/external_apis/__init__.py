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

from backend.external_apis.StorageSystemDetails import StorageSystemDetails
from backend.external_apis.TenantNotifications import TenantNotifications
from backend.external_apis.VolumeByStorageSystem import VolumeByStorageSystem
from backend.external_apis.NotificationsByStorageSystem import (
    NotificationByStorageSystem,
)
from backend.external_apis.TenantAlerts import TenantAlerts
from backend.external_apis.StorageList import StorageList
from backend.external_apis.MetricsByStorageSystem import MetricsByStorageSystem
from backend.external_apis.AlertByStorageSystem import AlertByStorageSystem
from backend.external_apis.ChatbotCapabilities import ChatbotCapabilities

# do not change the order of this list, new APIs should be appended at the end
REGISTERED_APIS = [
    StorageList,
    TenantAlerts,
    TenantNotifications,
    StorageSystemDetails,
    VolumeByStorageSystem,
    NotificationByStorageSystem,
    MetricsByStorageSystem,
    AlertByStorageSystem,
    ChatbotCapabilities,
]
