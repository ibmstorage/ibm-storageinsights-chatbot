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

import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import en from 'src/locals/en.json';
import { dataIdentifier } from 'src/utils/Constants';
import { Message } from 'src/typings/Message';
import MaskedLink from './MaskedLink';
import commonStyles from './Common.module.scss';

const TextSummary: React.FC<{ message: Message }> = ({ message }) => {
  const text =
    message?.identifier === dataIdentifier.markdown
      ? message?.data
      : message?.text;
  return (
    <div
      className={`${commonStyles['markdown-content']} ${commonStyles.chatMessage}`}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        children={text} />
      <div>
        {message?.link && (
          <p className={commonStyles.moreDetails}>
            {en.moreDetails}
            <MaskedLink
              text={en.IbmStorageInsights}
              url={message?.link} />
          </p>
        )}
      </div>
    </div>
  );
};

export default TextSummary;
