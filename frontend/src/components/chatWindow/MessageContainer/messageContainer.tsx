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
import { Button } from 'carbon-components-react';
import { SendAlt, StopFilled } from '@carbon/icons-react';
import {
  fetchPreviousActionsList,
  fetchMorningCupOfCoffee,
  fetchPreviousActionsData,
  runUserQuery,
} from 'src/services/chatApiService';
import {
  BOT,
  ERR_BAD_REQUEST,
  ERR_BAD_RESPONSE,
  USER,
  dataIdentifier,
  UNAUTHORIZED_STATUS_CODE,
  intentDescMap,
} from 'src/utils/Constants';
import en from 'src/locals/en.json';
import { getConversationHistory } from 'src/services/conversationHistoryService';
import { TextArea } from '@carbon/react';
import {
  getAuthCredentialByKey
} from 'src/utils/CommonUtil';
import ConversationHistoryTransformer from 'src/services/transformers/ConversationHistoryTransformer';
import { Message } from 'src/typings/Message';
import FormattedMessageRenderer from '../messageComponents/FormattedMessageRenderer';
import commonStyles from '../messageComponents/Common.module.scss';
import TypingIndicator from '../../chatUtils/TypingIndicator';
import NewChatWindow from '../newChatWindow/newChatWindow';
import styles from './messageContainer.module.scss';
import MaskedLink from '../messageComponents/MaskedLink';

interface MessageContainerProps {
  initiateNewChat: () => any;
  selectedConversationId: string;
  updateConversationID: (id: string) => any;
  updateConversationList: () => any;
  xApiKeyExpired: (flag:boolean) => any;
}

const MessageContainer: React.FC<MessageContainerProps> = ({
  initiateNewChat,
  selectedConversationId,
  updateConversationID,
  updateConversationList,
  xApiKeyExpired,
}) => {
  const [messageInput, setMessageInput] = React.useState<string>('');
  const [welcomeCardVisible, setWelcomeCardVisible] =
    React.useState<boolean>(true);
  const messagesEndReference = React.useRef(null);
  const [isTyping, setIsTyping] = React.useState<boolean>(false);
  const [isBotTyping, setIsBotTyping] = React.useState<boolean>(false);
  const [messages, setMessages] = React.useState<any[]>([]);
  const inputReference = React.useRef(null);
  const username = getAuthCredentialByKey('userID');
  const [popoverOpen, setPopoverOpen] = React.useState<boolean>(false);
  const tenantId = getAuthCredentialByKey('tenantID');
  const storageInsightsURl = `https://dev.insights.ibm.com/gui/${tenantId}#dashboard?activeDashboardId=storageSystem`;

  React.useEffect(() => {
    if (inputReference && inputReference?.current) {
      inputReference?.current?.focus();
    }
  }, []);

  React.useEffect(() => {
    if (messages.length === 0) {
      setWelcomeCardVisible(true);
    }
    messagesEndReference.current?.scrollIntoView({ behavior: 'smooth' });
    updateConversationList();
  }, [messages]);

  React.useEffect(() => {
    if (selectedConversationId) {
      fetchConversationHistory();
    }
  }, [selectedConversationId]);

  React.useEffect(() => {
    const typingTimeout = setTimeout(() => {
      setIsTyping(false);
    }, 1000);

    return () => {
      clearTimeout(typingTimeout);
    };
  }, [isTyping]);

  React.useEffect(() => {
    if (!selectedConversationId) {
      setMessageInput('');
      setMessages([]);
      setWelcomeCardVisible(true);
    }
    setIsBotTyping(false);
    setIsTyping(false);
  }, [initiateNewChat, selectedConversationId]);

  const fetchConversationHistory = async () => {
    try {
      const response = await getConversationHistory(
        selectedConversationId,
        username,
        tenantId,
      );
      const failureStatus = response?.response?.status;
      if (failureStatus === UNAUTHORIZED_STATUS_CODE) {
        xApiKeyExpired(true);
      }

      const formattedHistory =
        ConversationHistoryTransformer.getTransformedConversations(response);
      if (welcomeCardVisible) {
        setWelcomeCardVisible(false);
      }
      setMessages(formattedHistory);

      updateConversationList();
    } catch {
      console.error('error getting list');
    }
  };

  const handleMessageInput = (value: string) => {
    setMessageInput(value);
    setIsTyping(true);
  };

  const textAreaStyles: React.CSSProperties = {
    height: `${Math.max(40, messageInput.length / 20) / 16}rem`,
    resize: 'none',
    outline: 'none',
    backgroundColor: '#303030',
    borderBottom: 'none',
  };

  const updateBotResponse = (updatedMessage: Message) => {
    setMessages((previousMessages) =>
      previousMessages.map((message) =>
        message.sender === BOT && message.loading ? updatedMessage : message,
      ),
    );
  };

  const addUserQuery = (userMessage: string) => {
    setMessages((previousMessages) => [
      ...previousMessages,
      { text: userMessage, sender: USER },
      { sender: BOT, loading: true },
    ]);
  };

  const updateBotErrorResponse = (errorText: string) => {
    const errorMessage = {
      sender: BOT,
      text: errorText,
      loading: false,
    };
    updateBotResponse(errorMessage);
  };

  const getSummaryData = async (isIntent = false) => {
    try {
      setMessageInput('');
      if (!isIntent) {
        addUserQuery(en.morningCupOfCoffeeQuery);
      }

      const summaryData = await fetchMorningCupOfCoffee(selectedConversationId);
      if (summaryData) {
        const { response, code, conversation_id, data } = summaryData;
        const failureStatus = response?.status;
        if (failureStatus === UNAUTHORIZED_STATUS_CODE) {
            xApiKeyExpired(true);
        } else if (
          code === ERR_BAD_REQUEST ||
          code === ERR_BAD_RESPONSE ||
          failureStatus === 204
        ) {
          const textMessage =
            response?.data?.detail?.message ?? en.summaryRequestError;
          updateBotErrorResponse(textMessage);
        } else {
          if (conversation_id && conversation_id !== selectedConversationId) {
            updateConversationID(conversation_id);
          }

          if (data) {
            const consolidatedRoutineData = data.map((object) => ({
              text: object?.description,
              sender: BOT,
              identifier: object?.identifier,
              data:
                object?.intent === 'storage-list'
                  ? object?.data
                  : object?.data?.data,
              intent: object?.intent,
              id: Date.now(),
              loading: false,
              link: object?.link,
            }));

            // Check if all objects in consolidatedRoutineData have empty data fields
            const allDataFieldsEmpty = consolidatedRoutineData.every(
              (item) => !item.data || item.data.length === 0,
            );

            if (allDataFieldsEmpty) {
              updateBotErrorResponse(en.summaryNoDataMessage);
              return;
            }

            const morningCupOfCoffeeData = {
              text: '',
              sender: BOT,
              identifier: dataIdentifier.grids,
              data: consolidatedRoutineData,
              id: Date.now(),
              loading: false,
            };
            if (isIntent) {
              setMessages((previousMessages) => {
                const updatedMessages =
                  previousMessages.length > 0
                    ? previousMessages.slice(0, -1)
                    : previousMessages;
                return [...updatedMessages, morningCupOfCoffeeData];
              });
            } else {
              setMessages([
                { text: en.morningCupOfCoffeeQuery, sender: USER },
                morningCupOfCoffeeData,
              ]);
            }
          }
        }
      }
    } catch (error) {
      updateBotErrorResponse(en.summaryRequestError);
      console.error('Error validating API key:', error);
    }
  };

  const retrievePreviousActionsList = async () => {
    try {
      setWelcomeCardVisible(false);
      setMessageInput('');
      addUserQuery(en.previousActionsQuery);
      const previousActionsList = await fetchPreviousActionsList(
        selectedConversationId,
      );
      const failureStatus = previousActionsList?.response?.status;
      const beErrorMessage =
        previousActionsList.message ??
        previousActionsList?.response?.data?.detail?.message;

      if (failureStatus === UNAUTHORIZED_STATUS_CODE) {
        xApiKeyExpired(true);
      } else if (
        previousActionsList?.code === ERR_BAD_REQUEST ||
        previousActionsList?.code === ERR_BAD_RESPONSE
      ) {
        const badRequestMessage = beErrorMessage ?? en.noActionsAvailable;
        updateBotErrorResponse(badRequestMessage);
      } else if (previousActionsList) {
        const responseConversationID = previousActionsList?.conversation_id;
        if (
          responseConversationID &&
          responseConversationID !== selectedConversationId
        ) {
          updateConversationID(responseConversationID);
        }
        const textMessage = previousActionsList?.previous_actions?.length
          ? beErrorMessage
          : en.noActionsAvailable;
        const previousActionsData = {
          text: textMessage,
          sender: BOT,
          identifier: previousActionsList.identifier,
          data: previousActionsList?.previous_actions,
          intent: previousActionsList?.intent,
          id: Date.now(),
          loading: false,
        };
        const userInputMessage = {
          text: en.previousActionsQuery,
          sender: USER,
        };
        const updatedMsgs = [userInputMessage, previousActionsData];
        setMessages(updatedMsgs);
      }
    } catch (error: any) {
      const errorMessage =
        error?.response?.data?.detail?.message ?? en.inValidQueryErrorMessage;
      updateBotErrorResponse(errorMessage);
      console?.error('Error fetching previous actions list:', error);
    }
  };

  const onPreviousActionClicked = async (actionData) => {
    try {
      setWelcomeCardVisible(false);
      setMessageInput('');
      addUserQuery(actionData?.userQuery);
      // setIsBotTyping(false);
      const previousActionsObject = await fetchPreviousActionsData(
        actionData,
        selectedConversationId,
      );
      const failureStatus = previousActionsObject?.response?.status;
      const beErrorMessage =
        previousActionsObject?.response?.data?.detail?.message;

      if (failureStatus === UNAUTHORIZED_STATUS_CODE) {
        xApiKeyExpired(true);
      } else if (
        previousActionsObject.code === ERR_BAD_RESPONSE ||
        previousActionsObject.code === ERR_BAD_REQUEST ||
        failureStatus === 204
      ) {
        const errorMessage = beErrorMessage ?? en.defaultErrMessage;
        updateBotErrorResponse(errorMessage);
      } else if (previousActionsObject) {
        const responseConversationID = previousActionsObject?.conversation_id;
        if (
          responseConversationID &&
          responseConversationID !== selectedConversationId
        ) {
          updateConversationID(responseConversationID);
        }
        if (previousActionsObject?.intent === 'morning-cup-of-coffee') {
          await getSummaryData(true);
          return;
        }
        const previousActionsData = {
          text: intentDescMap[previousActionsObject?.intent] ?? '',
          sender: BOT,
          identifier: previousActionsObject.identifier,
          data: previousActionsObject?.data,
          intent: previousActionsObject?.intent,
          id: Date.now(),
          loading: false,
        };
        // Check if all objects in consolidatedRoutineData have empty data fields
        const allDataFieldsEmpty =
          (previousActionsObject.identifier === 'grid' ||
            previousActionsObject.identifier === 'grids' ||
            previousActionsObject.identifier === 'chart') &&
          (!previousActionsObject?.data ||
            previousActionsObject?.data?.length === 0);

        if (allDataFieldsEmpty) {
          updateBotErrorResponse(en.noActionsAvailable);
          return;
        }
        updateBotResponse(previousActionsData);
      }
    } catch (error: any) {
      const errorMessage =
        error?.response?.data?.detail?.message ?? en.previousActionsQuery;
      updateBotErrorResponse(errorMessage);
      console?.error('Error fecthing previous actions data', error);
    }
  };

  const onRetrieveSummaryData = () => {
    setWelcomeCardVisible(false);
    getSummaryData();
  };

  const sendUserQuery = async (userQuery: string) => {
    try {
      const conversationId = selectedConversationId ?? '';
      addUserQuery(userQuery);
      setMessageInput('');
      const botResponseData = await runUserQuery(userQuery, conversationId);
      if (botResponseData?.intent === 'morning-cup-of-coffee') {
        await getSummaryData(true);
        return;
      }

      const failureStatus = botResponseData?.response?.status;
      if (failureStatus === UNAUTHORIZED_STATUS_CODE) {
        xApiKeyExpired(true);
      } else if (
        botResponseData.code === ERR_BAD_REQUEST ||
        botResponseData.code === ERR_BAD_RESPONSE ||
        failureStatus === 204
      ) {
        const errorMessage =
          botResponseData?.response?.data?.detail?.message ??
          en.defaultErrMessage;
        updateBotErrorResponse(errorMessage);
      } else if (botResponseData) {
        const responseConversationID = botResponseData?.conversation_id;
        if (
          responseConversationID &&
          responseConversationID !== selectedConversationId
        ) {
          updateConversationID(responseConversationID);
        }

        const botMessage = {
          text: intentDescMap[botResponseData?.intent] ?? '',
          sender: BOT,
          identifier: botResponseData?.identifier,
          data: botResponseData?.data,
          intent: botResponseData?.intent,
          id: Date.now(),
          loading: false,
          link: botResponseData?.link,
        };
        // Check if all objects in consolidatedRoutineData have empty data fields
        const allDataFieldsEmpty =
          (botResponseData.identifier === 'grid' ||
            botResponseData.identifier === 'grids' ||
            botResponseData.identifier === 'chart') &&
          (!botResponseData?.data || botResponseData?.data?.length === 0);

        if (allDataFieldsEmpty) {
          updateBotErrorResponse(en.noDataAvailable);
          return;
        }
        updateBotResponse(botMessage);
      }
    } catch (error: any) {
      const errorMessage =
        error?.response?.data?.detail?.message ?? en.defaultErrMessage;
      updateBotErrorResponse(errorMessage);
      console.error('Error fetching response for query:', error);
    }
  };

  const handleMessageSubmit = (isCapabilitiesQuery?: boolean) => {
    if (welcomeCardVisible) {
      setWelcomeCardVisible(false);
    }
    const userQueryInput = isCapabilitiesQuery
      ? en.chatbotCapabilitiesQuery
      : messageInput;
    sendUserQuery(userQueryInput);
    if (!messageInput) {
      /* empty */
    }
  };

  const handleKeyDown = (event: any) => {
    if (event.key === 'Enter' && !isBotTyping) {
      event.preventDefault();
      handleMessageSubmit();
    }
  };

  const fetchChatbotCapabilities = () => {
    setMessageInput(en.chatbotCapabilitiesQuery);
    handleMessageSubmit(true);
  };

  const onStopTypingClicked = () => {
    setIsBotTyping(false);
  };
  return (
    <div className="message-main-container">
      <div
        className={`${styles['message-content-container']} ${
          welcomeCardVisible || initiateNewChat?.newChat
            ? ''
            : styles['container-padding-bottom']
        }`}>
        {welcomeCardVisible || initiateNewChat?.newChat ? (
          <NewChatWindow
            onMorningCoffeeCardClick={() => onRetrieveSummaryData()}
            onPreviousActionCardClick={() => retrievePreviousActionsList()}
            onLearnMoreActionCardClick={() => fetchChatbotCapabilities()}
          />
        ) : (
          messages &&
          messages.map((message, index) => (
            <div
              key={index}
              className={`${commonStyles.message} ${
                message.sender === USER ? commonStyles.user : commonStyles.bot
              }`}>
              <FormattedMessageRenderer
                key={`${message?.id}${message?.intent}${message?.sender}`}
                message={message}
                handleActionClicked={(actionData) =>
                  onPreviousActionClicked(actionData)
                }
              />
            </div>
          ))
        )}
        <div ref={messagesEndReference} />
      </div>

      <div className={styles['input-container-wrapper']}>
        <TypingIndicator isTyping={isTyping} />
        <div
          onMouseOver={() => setPopoverOpen(true)}
          onMouseLeave={() => setPopoverOpen(false)}
          onFocus={() => setPopoverOpen(true)}>
          <div
            id="chatInputContainer"
            className={styles['input-container']}>
            <TextArea
              ref={inputReference}
              size="md"
              id="messageInput"
              labelText=""
              hideLabel
              placeholder={en.textInputPlaceholder}
              value={messageInput}
              onChange={(e) => handleMessageInput(e.target.value)}
              onKeyDown={handleKeyDown}
              light={false}
              className={styles['chat-input']}
              style={textAreaStyles}
            />
            {isBotTyping ? (
              <Button
                onClick={() => onStopTypingClicked()}
                hasIconOnly
                renderIcon={StopFilled}
                iconDescription="Stop"
                className={styles['send-button']}
                size="md"
              />
            ) : (
              <Button
                onClick={() => handleMessageSubmit()}
                hasIconOnly
                renderIcon={SendAlt}
                iconDescription="Send"
                className={styles['send-button']}
                disabled={!messageInput?.length}
                size="md"
              />
            )}
          </div>
        </div>
        <p className={styles.advisoryTextContent}>
          {en.advisoryMessage}
          <MaskedLink
            text={en.IbmStorageInsightsTenant}
            url={storageInsightsURl}
            hasUnderline={true}
          />
        </p>
      </div>
    </div>
  );
}
export default MessageContainer;
