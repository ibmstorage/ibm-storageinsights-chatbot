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

export const getConversationList = async (
  username: string,
  tenantId: string,
) => {
  const queryParams = {
    username: username,
    tenant_id: tenantId,
  };
  try {
    const response = await axiosAPI.get(`get_user_conversation_list`, {
      params: queryParams,
    });

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      return response?.error;
    }
  } catch (error) {
    return error;
  }
};

export const getConversationHistory = async (
  conversationID: string,
  username: string,
  tenantId: string,
) => {
  const queryParams = {
    username: username,
    conversation_id: conversationID,
    tenant_id: tenantId,
  };
  try {
    const response = await axiosAPI.get(`get_conversation_history`, {
      params: queryParams,
    });

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      return response?.error;
    }
  } catch (error) {
    return error;
  }
};

export const renameConversationTitle = async (payload: any) => {
  try {
    const response = await axiosAPI.put(`rename_conversation_title`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      return response?.error;
    }
  } catch (error) {
    return error;
  }
};

export const deleteConversationHistory = async (payload: any) => {
  try {
    const response = await axiosAPI.delete(`delete_conversations`, {
      headers: {
        'Content-Type': 'application/json',
      },
      data: payload,
    });

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      return response?.error || new Error('Unknown error');
    }
  } catch (error) {
    // Ensure only relevant error information is returned
    return (
      error.response?.data ||
      error.message ||
      new Error('An unknown error occurred')
    );
  }
};
