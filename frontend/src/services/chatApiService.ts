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

import axiosAPI from './axiosInstance';
import {
  getSelectedAPIEntries,
  getAuthCredentialByKey,
} from 'src/utils/CommonUtil';
import { encryptValue } from './encryptionService';

const constructPayload = (conversation_id: string) => {
  let tenantId = getAuthCredentialByKey('tenantID');
  let apiKey = getAuthCredentialByKey('xApiKey');
  let encryptedKey = encryptValue(apiKey);

  const payload = {
    tenant_id: tenantId,
    api_key: encryptedKey,
    username: getAuthCredentialByKey('userID'),
    conversation_id: conversation_id,
  };

  return payload;
};

//POST API service function to run user queries
export const runUserQuery = async (userQuery: any, conversation_id: string) => {
  try {
    const payload = constructPayload(conversation_id);
    payload.userQuery = userQuery;

    const response = await axiosAPI.post(`run_chatbot`, payload);

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      console.error('Failed to fetch the response');
    }
  } catch (error) {
    console.error('Error:', error);
    return error;
  }
};

//POST API service to fetch morning cup of coffee info
export const fetchMorningCupOfCoffee = async (conversation_id = '') => {
  try {
    const apiEntries = getSelectedAPIEntries();
    const payload = constructPayload(conversation_id);

    const response = await axiosAPI.post(`morning_cup_of_coffee`, payload);

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      console.error('Failed to fetch the response');
      return response?.error;
    }
  } catch (error) {
    console.error('Error:', error);
    return error;
  }
};

//POST API service to fetch Previous actions list
export const fetchPreviousActionsList = async (conversation_id?: string) => {
  try {
    let tenantId = getAuthCredentialByKey('tenantID');
    const payload = {
      username: getAuthCredentialByKey('userID'),
      tenant_id: tenantId,
      conversation_id: conversation_id ?? '',
    };
    const response = await axiosAPI.post(`previous_actions`, payload);

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      console.error('Failed to fetch the response');
      return response?.error;
    }
  } catch (error) {
    console.error('Error:', error);
    return error;
  }
};

//POST API service function to fetch Previous actions data
export const fetchPreviousActionsData = async (
  actionData: any,
  conversation_id: string,
) => {
  try {
    const apiEntries = getSelectedAPIEntries();
    const conversationID = conversation_id ?? '';
    const payload = constructPayload(conversationID);
    const actionPayload = {
      ...payload,
      action: actionData.intent,
      entities: actionData.entity,
      userQuery: actionData.userQuery,
    };
    const response = await axiosAPI.post(`execute_action`, actionPayload);

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      console.error('Failed to fetch the response');
      return response?.error;
    }
  } catch (error) {
    console.error('Error:', error);
    return error;
  }
};
