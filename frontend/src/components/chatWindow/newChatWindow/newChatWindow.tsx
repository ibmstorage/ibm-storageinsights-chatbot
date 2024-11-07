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

import React, { useState } from 'react';
import en from 'src/locals/en.json';
import { Popover, PopoverContent } from '@carbon/react';
import chatbotLogo from '../../../assets/Querius_Logo.png';
import styles from './newChatWindow.module.scss';

interface NewChatWindowProps {
  onMorningCoffeeCardClick: () => any;
  onPreviousActionCardClick: () => any;
  onLearnMoreActionCardClick: () => any;
}

const NewChatWindow: React.FC<NewChatWindowProps> = ({
  onMorningCoffeeCardClick,
  onPreviousActionCardClick,
  onLearnMoreActionCardClick,
}) => {
  const [selectedButton, setSelectedButton] = useState('');
  const isNewUser = localStorage.getItem('is_NewUser') === 'true';
  const [morningCupPopoverOpen, setMorningCupPopoverOpen] =
    React.useState(false);
  const [previousActionsPopoverOpen, setPreviousActionsPopoverOpen] =
    React.useState(false);
  const handlePreviousActionsClick = () => {
    onPreviousActionCardClick();
    setSelectedButton(en.previousActions);
  };

  const handleMorningCupOfCoffeeClick = () => {
    onMorningCoffeeCardClick();
    setSelectedButton(en.morningCupOfCoffee);
  };

  const handleLearnMoreClick = () => {
    onLearnMoreActionCardClick();
    setSelectedButton(en.learnMore);
  };

  return (
    <div>
      <div className={styles.newChatWindow}>
        <div>
          <img
            src={chatbotLogo}
            alt={en.queriusLogo}
            className={styles.chatLogo}
          />
        </div>
        <p className={styles.welcomeStatement}>
          <span className={styles.limeText}>{en.welcomeStatementStart}</span>
          <strong className={styles.blueText}>{en.ibmStorageInsightsChatbot}</strong>
          <span className={styles.limeText}>{en.welcomeStatementEnd}</span>
        </p>
      </div>
      <div className={styles.routineContainer}>
        <div
          onMouseOver={() => setMorningCupPopoverOpen(true)}
          onMouseLeave={() => setMorningCupPopoverOpen(false)}
          onFocus={() => setMorningCupPopoverOpen(true)}>
          <Popover
            className={styles.popoverContainer}
            open={false && morningCupPopoverOpen}
            bodyContent={en.selectAPIKey}
            triggerClassName="popover-trigger"
            tabIndex={0}
            align="bottom"
            highContrast>
            <button
              type="button"
              className={`${styles.routineButtons} ${
                selectedButton === en.morningCupOfCoffee
                  ? styles.morningCupOfTeaButton
                  : ''
              }`}
              onClick={handleMorningCupOfCoffeeClick}>
              <span className={styles.routineContent}>
                {en.morningCupOfCoffeTitle}
              </span>
              <p className={styles.cardTitle}>
                {en.morningCupOfCoffeeSubTitle}
              </p>
            </button>
            <PopoverContent className={styles.inputDisabledTooltip}>
              {en.selectAPIKey}
            </PopoverContent>
          </Popover>
        </div>

        <div
          onMouseOver={() => setPreviousActionsPopoverOpen(true)}
          onMouseLeave={() => setPreviousActionsPopoverOpen(false)}
          onFocus={() => setPreviousActionsPopoverOpen(true)}>
          <Popover
            className={styles.popoverContainer}
            open={false && previousActionsPopoverOpen}
            bodyContent={en.selectAPIKey}
            triggerClassName="popover-trigger"
            tabIndex={0}
            align="bottom"
            highContrast>
            <button
              type="button"
              className={`${styles.previousActionButton} ${
                selectedButton === en.previousActions
                  ? styles.pastEventsButton
                  : ''
              }`}
              disabled={isNewUser}
              onClick={handlePreviousActionsClick}>
              <span className={styles.routineContent}>
                {en.previousActionsTitle}
              </span>
              <p className={styles.cardTitle}>{en.previousActionsSubTitle}</p>
            </button>
            <PopoverContent className={styles.inputDisabledTooltip}>
              {en.selectAPIKey}
            </PopoverContent>
          </Popover>
        </div>
        <button
          type="button"
          className={`${styles.learnMoreButton} ${
            selectedButton === en.learnMore ? styles.learnMoreButton : ''
          }`}
          onClick={handleLearnMoreClick}>
          <span className={styles.routineContent}>{en.learnMoreTitle}</span>
          <p className={styles.cardTitle}>{en.learnMoreSubTitle}</p>
        </button>
      </div>
    </div>
  );
}

export default NewChatWindow;
