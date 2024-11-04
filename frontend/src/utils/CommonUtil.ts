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

import { ITenantAPIKey } from "src/typings/TenantAPIKey";
import { ITenantConfigRequest } from "src/typings/Requestpayload";
import {
  GIB,
  beColumnList,
  conditionMapping,
  dataIdentifier,
} from "./Constants";

/**
 * Formats a timestamp into a human-readable date and time string.
 * @param {number} timestamp - The timestamp to format (in milliseconds).
 * @returns {string} The formatted date and time string in the "MMM DD, YYYY HH:mm:ss" format (e.g., "Apr 15, 2024 14:30:00").
 */
export const formatDataTimestamp = (timestamp: number) => {
  const date = new Date(timestamp);
  const dateOptions = {
    year: "numeric",
    month: "short",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  };
  const formattedDate = date.toLocaleDateString("en-US", dateOptions);
  return `${formattedDate}`;
};

/**
 * Converts bytes to Gibibytes (GiB).
 * @param {number} bytes - The size in bytes to convert to Gibibytes.
 * @returns {string} The size converted to Gibibytes with two decimal places.
 */
export const convertBytesToGiB = (bytes) => {
  const gibibyte = 1024 ** 3;
  const gibibytes = bytes / gibibyte;
  return gibibytes.toFixed(2);
};

/**
 * Formats table headers for display, adding human-readable labels and units where applicable.
 * @param {string[]} headerData - Array of header keys to be formatted.
 * @returns {Object[]} An array of objects with formatted headers, including keys and human-readable labels.
 */
export const formatTableHeaders = (headerData: any) => {
  const formattedHeaders = headerData?.map((key) => ({
    key,
    header: key.endsWith("_bytes")
      ? key.charAt(0).toUpperCase() +
        key.slice(1).replace(/_/g, " ") +
        ` (${GIB})`
      : key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, " "),
  }));
  return formattedHeaders;
};

/**
 * Formats table rows based on the provided message data and formatted header data.
 * @param {Object} message - The message object containing data to be formatted into rows.
 * @param {Object[]} formattedHeaderData - An array of objects with formatted header information.
 * @returns {Object[]} An array of objects representing formatted table rows.
 */
export const formatTableRows = (message, formattedHeaderData) => {
  const formattedRows = message.data.map((item, index) => {
    const row = {};
    formattedHeaderData.forEach((header) => {
      if (header.key.endsWith("_bytes")) {
        const bytes = item[header.key];
        const gibibytes = convertBytesToGiB(bytes);
        row[header.key] = gibibytes;
      } else if (
        header.key === beColumnList.lastDataCollection ||
        header.key === beColumnList.occurenceTime ||
        header.key === beColumnList.time
      ) {
        const formattedTime = formatDataTimestamp(item[header.key]);
        row[header.key] = formattedTime;
      } else if (header.key === beColumnList.condition) {
        row[header.key] =
          conditionMapping[item[header.key]] || item[header.key];
      } else {
        row[header.key] = item[header.key];
      }
    });
    row["id"] = index;
    return row;
  });
  return formattedRows;
};

/**
 * Formats a timestamp into a human-readable date and time string.
 *
 * @param {string} timestamp - The timestamp string to format.
 * @returns {string} - The formatted date and time string in 'dd Month yyyy, HH:MM:SS' format.
 */
export const formatTimestamp = (timestamp: string): string => {
  const date = new Date(timestamp);

  const options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "long",
    day: "2-digit",
  };

  const formattedDate = date.toLocaleDateString("en-GB", options);
  const formattedTime = date.toLocaleTimeString("en-GB", { hour12: false });

  return `${formattedDate}, ${formattedTime}`;
};

export const getSelectedAPIEntries = () => {
  const savedAPIEntries = localStorage.getItem("selectedAPIEntries");
  return savedAPIEntries ? JSON.parse(savedAPIEntries) : [];
};

export const getAuthCredentialByKey = (key: string) => {
  const authCredentials = localStorage.getItem("authCredentials");

  if (authCredentials) {
    const parsedCredentials = JSON.parse(atob(authCredentials));
    return parsedCredentials[key] || "";
  }

  return "";
};

export const getConfigPayload = (
  tenantAPIKeyEntry: ITenantAPIKey
): ITenantConfigRequest => {
  const { tenantId, tenantName, apiKey, newAPIKey, isCurrent, apiKeyId } =
    tenantAPIKeyEntry;

  const configPayload: ITenantConfigRequest = {
    tenant_id: tenantId,
    username: getAuthCredentialByKey("userID"),
    ...(tenantName && { tenant_name: tenantName }),
    ...(apiKeyId && { api_key_id: apiKeyId }),
    ...(apiKey && { api_key: apiKey }),
    ...(newAPIKey && {
      new_api_key: newAPIKey,
    }),
    ...(isCurrent && { is_current: isCurrent === "true" ? 1 : 0 }),
  };

  return configPayload;
};

export function convertObjectToQueryParams(parameters: any) {
  const queryParameters = Object.entries(parameters)
    .map(([key, value]) =>
      Array.isArray(value)
        ? value
            .map(
              (object) =>
                `${encodeURIComponent(key)}=${encodeURIComponent(
                  JSON.stringify(object)
                )}`
            )
            .join("&")
        : `${encodeURIComponent(key)}=${encodeURIComponent(value as string)}`
    )
    .join("&");
  return queryParameters;
}

export function storeSelectedAPIEntry(
  tenantConfigData: ITenantConfigRequest[]
) {
  const currentTenant = tenantConfigData?.find(
    (tenantConfig: any) => tenantConfig.is_current
  );
  if (currentTenant) {
    const formattedTenantData = {
      apiKey: currentTenant.api_key,
      id: currentTenant?.api_key_id,
      isSelected: currentTenant?.is_current,
      tenantId: currentTenant.tenant_id,
      tenantName: currentTenant.tenant_name,
    };

    localStorage.setItem(
      "selectedAPIEntries",
      JSON.stringify([formattedTenantData])
    );
  }
}

export function botMarkdownMessage(responseData: any) {
  const textContent =
    responseData?.identifier === dataIdentifier.markdown
      ? responseData?.data && responseData?.data !== ""
        ? responseData?.data
        : responseData?.message
      : responseData?.data;

  return textContent;
}
