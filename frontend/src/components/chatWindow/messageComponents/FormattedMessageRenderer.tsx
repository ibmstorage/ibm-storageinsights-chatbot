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
import { MachineLearning, UserAvatarFilled } from '@carbon/icons-react';
import { BOT, USER, dataIdentifier } from 'src/utils/Constants';
import commonStyles from './Common.module.scss';
import MessageWithDatatable from './MessageWithDatatable';
import ActionsTagList from './ActionsTagList';
import chatbotLogo from '../../../assets/Chatbot_Logo.png';
import UserFeedback from '../userFeedback/UserFeedback';
import MessageWithChart from './MessageWithChart';
import TextSummary from './TextSummary';
import { Message } from 'src/typings/Message';
import WaitingMessage from 'src/components/chatUtils/WaitingMessage';

const senderInfo: any = {
  user: {
    title: 'User',
    icon: (
      <UserAvatarFilled
        size="1.8rem"
        fill="#F8FF73"
      />
    ),
  },
  bot: { title: 'Bot', icon: <MachineLearning size="1.8rem" /> },
};

interface FormattedMessageRendererProps {
  message: Message;
  handleActionClicked: (action: string) => any;
}

const FormattedMessageRenderer: React.FC<FormattedMessageRendererProps> = ({
  message,
  handleActionClicked,
}) => {
  return (
    <div id="botResponseContainer">
      <div className={commonStyles['sender-info']}>
        {message.sender === BOT ? (
          <div>
            <img
              src={chatbotLogo}
              alt="Chatbot Logo"
              className={commonStyles.botLogo}
            />
          </div>
        ) : (
          <span className={commonStyles.icon}>
            {senderInfo[message.sender]?.icon}
          </span>
        )}
        <span className={commonStyles.text}>
          {message.sender === USER ? (
            <span>{message.text}</span>
          ) : message.loading ? (
            <WaitingMessage />
          ) : message.identifier === dataIdentifier.grid ? (
            <MessageWithDatatable
              key={`${message?.id}${message?.intent}`}
              message={message}
            />
          ) : message.identifier === dataIdentifier.grids &&
            message?.data &&
            message.data.length > 0 ? (
              message.data.map((data, index) => (
              <>
                <MessageWithDatatable
                  key={`${message.id}${message.intent}${index}${data.intent}`}
                  message={data}
                  isSummaryData
                />
                {index < message.data.length ? (
                  <>
                    <br />
                    <br />
                  </>
                ) : (
                  ''
                )}
              </>
              ))
            ) : message.identifier === dataIdentifier.buttons ? (
            <ActionsTagList
              message={message}
              onActionClick={(data) => {
                handleActionClicked(data);
              }} />
            ) : message.identifier === dataIdentifier.chart ? (
            <MessageWithChart message={message} />
            ) : (
            <TextSummary message={message} />
            )}
        </span>
      </div>
      {message.sender === BOT && !message.loading && (
        <div className={commonStyles.feedbackDivPadding}>
          <UserFeedback id={message.id} />
        </div>
      )}
    </div>
  );
}

export default FormattedMessageRenderer;
