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

import React from "react";

import { Help, UserAvatarFilled } from "@carbon/icons-react";
import chatbotLogo from "src/assets/Querius_Logo.png";
import en from "src/locals/en.json";
import { useNavigate } from "react-router-dom";
import {
  IBM_DOCS_STORAGE_INSIGHTS_URL,
} from "src/utils/Constants";
import { Tooltip } from "@carbon/react";
import { getAuthCredentialByKey } from "src/utils/CommonUtil";
import MessageContainer from "./MessageContainer/messageContainer";
import styles from "./chatWindow.module.scss";

interface ChatWindowProps {
  newChat: () => void;
  selectedConversationId: string;
  updateConversationID: (id: string) => void;
  updateConversationList: () => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  newChat,
  selectedConversationId,
  updateConversationID,
  updateConversationList,
}) => {
  const [isDropdownOpen, setDropdownOpen] = React.useState<boolean>(false);
  const [isXApiKeyExpired, setIsXApiKeyExpired] =
    React.useState<boolean>(false);
  const iconReference = React.useRef(null);
  const dropdownReference = React.useRef(null);
  const navigate = useNavigate();
  const [open, setOpen] = React.useState<boolean>(false);

  React.useEffect(() => {
    if (isXApiKeyExpired) {
      setIsXApiKeyExpired(false);
    }
  }, [isXApiKeyExpired]);

  React.useEffect(() => {
    if (isDropdownOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isDropdownOpen]);

  const handleHelpClick = () => {
    window.open(IBM_DOCS_STORAGE_INSIGHTS_URL, "_blank");
  };

  const handleUserIconClick = () => {
    setDropdownOpen((previousState) => !previousState);
  };

  const logoutUser = () => {
    localStorage.removeItem("authCredentials");
    navigate("/sign-in");
  };

  const handleDropdownItemClick = (id: string) => {
    if (id === en.logoutId) {
      logoutUser();
    }
  };

  const handleClickOutside = (event: any) => {
    if (
      dropdownReference.current &&
      !dropdownReference?.current.contains(event.target) &&
      !iconReference?.current.contains(event.target)
    ) {
      setDropdownOpen(false);
    }
  };

  const username = getAuthCredentialByKey("userID") || en.username;
  const currentTenantId = getAuthCredentialByKey("tenantID");

  return (
    <div id="chatWindowContainer">
      <div className={styles.chatHeader}>
        <div id="logo-section">
          <img
            src={chatbotLogo}
            alt={en.chatbotLogo}
            className={styles.queriusLogo}
          />
        </div>
        <div className={styles.chatbotTitle}>{en.ibmStorageInsightsChatbot}</div>
        {currentTenantId && (
          <>
            <div className={styles.currentTenantId}>
              {en.activeTenant} {currentTenantId}
            </div>
            <div className={styles.verticalSeparator} />
          </>
        )}
        <div className={styles["help-icon"]} onClick={handleHelpClick}>
          <Help size="1.1rem" />
        </div>
        <div
          ref={iconReference}
          className={styles.userIcon}
          onClick={handleUserIconClick}
        >
          <span className={styles.icon}>
            <UserAvatarFilled
              size="1.3rem"
              fill="#F8FF73"
              className={styles.menuButtonIcon}
            />
          </span>
          {isDropdownOpen && (
            <div ref={dropdownReference} className={styles.dropdownContent}>
              <Tooltip
                align="left"
                open
                onClose={() => setOpen(!open)}
                label={username}
                kind="dark"
              >
                <div
                  className={styles.usernameMenuItem}
                  onClick={() => handleDropdownItemClick("username")}
                >
                  {username}
                </div>
              </Tooltip>

              <div
                className={styles.logoutMenuItem}
                onClick={() => handleDropdownItemClick("logout")}
              >
                {en.logoutId}
              </div>
            </div>
          )}
        </div>
      </div>
      <div className={styles["flex-container"]}>
        <div className={styles["chat-window"]}>
          <MessageContainer
            initiateNewChat={newChat}
            selectedConversationId={selectedConversationId}
            updateConversationID={updateConversationID}
            updateConversationList={updateConversationList}
            xApiKeyExpired={(flag) => setIsXApiKeyExpired(flag)}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatWindow;
