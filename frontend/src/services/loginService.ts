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

import axiosAPI, { axiosAPIRequestConfig } from './axiosInstance';
import en from 'src/locals/en.json';

export const login = async (payload) => {
  try {
    const response = await axiosAPI.post(`login`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
      skipAuth: true,
    } as axiosAPIRequestConfig);

    if (response.status === 200 || response.status === 201) {
      return response.data;
    } else {
      return response?.error;
    }
  } catch (error) {
    console.error(en.loginFiledLog, error);
    return error;
  }
};
