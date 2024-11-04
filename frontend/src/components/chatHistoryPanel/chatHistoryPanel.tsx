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

import React, { useState, useEffect } from 'react';
import { TrashCan, Edit, AddComment } from '@carbon/icons-react';
import styles from 'src/components/chatHistoryPanel/chatHistoryPanel.module.scss';
import en from 'src/locals/en.json';
import {
  getConversationList,
  renameConversationTitle,
  deleteConversationHistory,
} from 'src/services/conversationHistoryService';
import { formatTimestamp, getAuthCredentialByKey } from 'src/utils/CommonUtil';
import { UNAUTHORIZED_STATUS_CODE } from 'src/utils/Constants';

interface ChatHistoryPanelProperties {
  onNewChatClicked: () => void;
  handleConversationChange: (conversationId: string) => void;
  reloadHistoryListKey: string;
  selectedConversationId: string | null;
}

const ChatHistoryPanel: React.FC<ChatHistoryPanelProperties> = ({
  onNewChatClicked,
  handleConversationChange,
  reloadHistoryListKey,
  selectedConversationId,
}) => {
  const [chats, setChats] = useState<Conversation[]>([]);
  const [editingIndex, setEditingIndex] = useState<any>(null);
  const [editValue, setEditValue] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const username = getAuthCredentialByKey('userID');

  useEffect(() => {
    const fetchConversationList = async () => {
      try {
        const response = await getConversationList(username, tenantId);
        if (response && Array.isArray(response)) {
          const sortedConversations = sortConversations(response);
          setChats(sortedConversations);
        }
      } catch (error) {
        console.error('error getting list');
      }
    };
    fetchConversationList();
  }, [reloadHistoryListKey, username]);

  const tenantId = getAuthCredentialByKey('tenantID');

  const renameConversation = async (
    newName: string,
    conversation_id: string,
  ) => {
    const payload: any = {
      new_title: newName,
      conversation_id: conversation_id,
      username: username,
      tenant_id: tenantId,
    };
    const noOfRowUpdated = await renameConversationTitle(payload);
    if (noOfRowUpdated && Number(noOfRowUpdated) > 0) {
      return true;
    } else {
      return false;
    }
  };

  const handleDelete = async (index: number) => {
    try {
      const conversationId = chats[index]?.conversation_id;
      const payload = {
        conversation_ids: [conversationId],
        username,
        tenant_id: tenantId,
      };
      const response = await deleteConversationHistory(payload);
      if (response?.message) {
        const updatedChats = [...chats];
        updatedChats.splice(index, 1);
        setChats(sortConversations(updatedChats));
        setChats(updatedChats);
        if (conversationId === selectedConversationId) {
          onNewChatClicked();
        }
      } else {
        console.error('Failed to delete conversation:', response?.detail);
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const handleEdit = (index: number) => {
    setEditingIndex(index);
    setEditValue(chats[index]?.conversation_title);
  };

  const handleEditChange = (e: any) => {
    setEditValue(e.target.value);
  };

  const handleEditConfirm = async (index: number) => {
    if (chats[index]?.conversation_title !== editValue) {
      const isRenameSuccess = await renameConversation(
        editValue,
        chats[index]?.conversation_id,
      );

      const updatedChats = [...chats];

      if (isRenameSuccess) {
        updatedChats[index] = {
          ...updatedChats[index],
          conversation_title: editValue,
        };
        setChats(sortConversations(updatedChats));
      }
      setChats(updatedChats);
    }
    setEditingIndex(null);
  };

  const handleSearchChange = (e) => {
    const query = e.target.value.toLowerCase();
    setSearchQuery(query);
  };

  const filteredChats = chats.filter((chat) =>
    chat?.conversation_title
      ?.toLowerCase()
      ?.includes(searchQuery.toLowerCase()),
  );

  const sortConversations = (conversations: Conversation[]) => {
    return conversations.sort((a, b) => {
      const dateA = new Date(a.recent_timestamp).getTime();
      const dateB = new Date(b.recent_timestamp).getTime();

      return dateB - dateA;
    });
  };

  const handleEditButtonClick = (event: any, index: number) => {
    event.stopPropagation();
    handleEdit(index);
  };

  const handleDeleteButtonClick = (event: any, index: number) => {
    event.stopPropagation();
    handleDelete(index);
  };

  return (
    <div
      id="chatLeftPanel"
      className={styles.leftPanelContainer}>
      <div id="newChatAndSearchSection">
        <button
          className={styles.renderNewChat}
          onClick={() => onNewChatClicked()}>
          {en.newChat} &nbsp; <AddComment />
        </button>
        <div className={styles.searchContainer}>
          <input
            type="text"
            placeholder={en.searchInputPlaceholder}
            className={styles.searchInput}
            value={searchQuery}
            onChange={handleSearchChange}
          />
        </div>
      </div>
      <div
        id="chatHistorySection"
        className={styles.chatList}>
        <ul className={styles.chatOptions}>
          {filteredChats.map((chat: Conversation, index: number) => (
            <li
              key={index}
              className={styles.chatListDetails}
              onClick={() => handleConversationChange(chat?.conversation_id)}>
              <div
                className={`${styles.listItem} ${
                  chat?.conversation_id === selectedConversationId
                    ? styles.activeChat
                    : ''
                }`}>
                {editingIndex === index ? (
                  <input
                    type="text"
                    value={editValue}
                    onChange={handleEditChange}
                    autoFocus
                    onBlur={() => handleEditConfirm(index)}
                  />
                ) : (
                  <>
                    <div id="chatListInfoContainer">
                      <p className={styles.chatListInfo}>
                        {chat?.conversation_title}
                      </p>
                      <small className={styles.chatHistoryTimestamp}>
                        {chat?.recent_timestamp
                          ? formatTimestamp(chat?.recent_timestamp)
                          : ' '}
                      </small>
                    </div>
                    <div className={styles.alterChatButtons}>
                      <button
                        className={styles.iconButton}
                        onClick={(event) =>
                          handleEditButtonClick(event, index)
                        }>
                        <Edit className={styles.editChat} />
                      </button>
                      <button
                        className={styles.iconButton}
                        onClick={(event) =>
                          handleDeleteButtonClick(event, index)
                        }>
                        <TrashCan className={styles.deleteChat} />
                      </button>
                    </div>
                  </>
                )}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChatHistoryPanel;
