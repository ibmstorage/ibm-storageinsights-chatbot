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

import axiosAPI, {
  axiosAPIRequestConfig,
  skipAuthConfig,
} from './axiosInstance';

export const fetchSecurityQuestions = async (username) => {
  try {
    const response = await axiosAPI.get(
      `security_questions/?username=${username}`,
      skipAuthConfig,
    );
    if (response.status === 200) {
      return response.data;
    } else {
      return {
        error: response.statusText || 'Failed to fetch security questions',
      };
    }
  } catch (error) {
    return { error: error.message || 'An unknown error occurred' };
  }
};

export const validateSecurityAnswers = async (payload) => {
  try {
    const response = await axiosAPI.post(`validate_security_answers`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
      skipAuth: true,
    } as axiosAPIRequestConfig);

    if (response.status === 200 && response.data.status === 'SUCCESS') {
      return { success: true };
    } else {
      return { success: false };
    }
  } catch (error) {
    throw new Error('Error validating security answers');
  }
};

export const updatePasswordService = async (payload) => {
  try {
    const response = await axiosAPI.post(`update_password`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
      skipAuth: true,
    } as axiosAPIRequestConfig);

    if (response.status === 200 && response.data.status === 'SUCCESS') {
      return { success: true };
    } else {
      return { success: false };
    }
  } catch (error) {
    throw new Error('An unknown error occurred');
  }
};
