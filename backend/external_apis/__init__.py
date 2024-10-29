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
