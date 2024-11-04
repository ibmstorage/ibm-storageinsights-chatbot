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
import { v4 as uuidv4 } from 'uuid';
import ChatHistoryPanel from 'src/components/chatHistoryPanel/chatHistoryPanel';
import ChatWindow from 'src/components/chatWindow/chatWindow';
import MyModal from 'src/components/welcomeScreen/WelcomeScreen';
import styles from 'src/components/chatDashboard/chatDashboard.module.scss';

const ChatDashboard: React.FC = () => {
  const [newChat, setNewChat] = React.useState<boolean>(false);
  const [showWelcomeBanner, setShowWelcomeBanner] =
    React.useState<boolean>(false);
  const [reloadHistoryListKey, setReloadHistoryListKey] =
    React.useState<number>(0);

  React.useEffect(() => {
    // Determine if the user is new and update the login count for returning users,
    // which will inform whether to display the welcome banner for first-time users.
    const isNewUser = JSON.parse(localStorage.getItem('is_NewUser') || 'false');
    const loginCount = parseInt(localStorage.getItem('login_count') || '0', 10);
    if (!isNewUser) {
      localStorage.setItem('login_count', (loginCount + 1).toString());
    }
    localStorage.setItem('login_count', (loginCount + 1).toString());
  }, []);

  const generateUUID = (): string => {
    return uuidv4();
  };

  const [selectedConversationId, setSelectedConversationId] =
    React.useState<string>(generateUUID());

  const handleConversationChange = (conversationId: string) => {
    setSelectedConversationId(conversationId);
  };

  const updateConversationID = (conversationId: string) => {
    setSelectedConversationId(conversationId);
  };
  const handleNewChatClicked = () => {
    setNewChat(!newChat);
    setSelectedConversationId(generateUUID());
  };

  const updateConversationList = () => {
    setReloadHistoryListKey((prevFlag) => prevFlag + 1);
  };

  const handleConfigureApiKey = () => {
    setShowWelcomeBanner(false);
  };

  return (
    <div
      id="chatbotContainer"
      className={`${styles['chatbot-container']} carbon-darker-theme`}>
      <div
        id="chatbotMainContent"
        className={styles['chatbot-main-content']}>
        <ChatHistoryPanel
          handleConversationChange={handleConversationChange}
          onNewChatClicked={handleNewChatClicked}
          reloadHistoryListKey={reloadHistoryListKey}
          selectedConversationId={selectedConversationId}></ChatHistoryPanel>
        <div
          id="chatWindow"
          className={styles['chatbot-window']}>
          <div className="App">
            <ChatWindow
              newChat={newChat}
              selectedConversationId={selectedConversationId}
              updateConversationID={updateConversationID}
              updateConversationList={updateConversationList}></ChatWindow>
          </div>
        </div>
      </div>
      {showWelcomeBanner && (
        <MyModal
          isOpen={showWelcomeBanner}
          onClose={() => setShowWelcomeBanner(false)}
          onConfigureApiKey={handleConfigureApiKey}
        />
      )}
    </div>
  );
};

export default ChatDashboard;
