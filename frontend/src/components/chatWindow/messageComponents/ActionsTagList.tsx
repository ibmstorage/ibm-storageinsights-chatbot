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
import { Tag } from 'carbon-components-react';
import commonStyles from './Common.module.scss';
import { Message } from 'src/typings/Message';

interface ActionsTagListProps {
  message: Message;
  onActionClick: (actionId: string) => any;
}

const ActionsTagList: React.FC<ActionsTagListProps> = ({ message, onActionClick }) => {
  const previousActionList = message?.data;
  return (
    <div>
      <div className={`${commonStyles.bot} ${commonStyles.chatMessage}`}>
        {message.text}
      </div>
      {previousActionList && (
        <div className={commonStyles.tagListContainer}>
          {previousActionList.map((action) => (
            <Tag
              className={commonStyles.actionButton}
              key={action.intent}
              size="md"
              title={action?.userQuery}
              onClick={() => onActionClick(action)}>
              {action?.userQuery}
            </Tag>
          ))}
        </div>
      )}
    </div>
  );
};

export default ActionsTagList;
