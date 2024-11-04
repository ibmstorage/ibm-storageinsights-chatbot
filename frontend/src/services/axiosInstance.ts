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

import axios, { InternalAxiosRequestConfig } from 'axios';

const isProduction = process.env.NODE_ENV === 'production';

const baseURL = isProduction 
    ? process.env.REACT_APP_BACKEND_BASE_URL + '/chatbot/'
    : '/chatbot/';

const axiosAPI = axios.create({
  baseURL,
});

axiosAPI.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

axiosAPI.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default axiosAPI;
