/*
 * {COPYRIGHT-TOP}
 * IBM Confidential
 * (C) Copyright IBM Corp. 2024
 *
 * << 5608-WC0/5608-PC4 >>
 *
 * All Rights Reserved
 * Licensed Material - Property of IBM
 * The source code for this program is not published or otherwise
 * divested of its trade secrets, irrespective of what has
 * been deposited with the U. S. Copyright Office.
 *
 * U.S. Government Users Restricted Rights
 * - Use, duplication or disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
 * {COPYRIGHT-END}
 */

import React from 'react';
import styles from 'src/components/welcomeScreen/WelcomeScreen.module.scss';
import { Modal, Button } from 'carbon-components-react';
import imImage from 'src/assets/Querius_Logo.png';
import en from 'src/locals/en.json';

interface WelcomeScreenProps {
  isOpen: boolean;
  onClose: () => any;
  onConfigureApiKey: () => any;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ isOpen, onClose, onConfigureApiKey }) => {
  const handleClick = () => {
    window.location.href =
      'https://www.ibm.com/docs/en/storage-insights?topic=overview-storage-insights';
  };

  const handleConfigureApiKey = () => {
    onConfigureApiKey();
  };

  return (
    <Modal
      open={isOpen}
      onRequestClose={onClose}
      modalHeading=""
      size="sm"
      className={styles.modal}
      style={{ '--cds-overlay': 'rgba(0,0,0,0.5)' }}>
      <div>
        <img
          src={imImage}
          alt="im"
          className={styles.logo}
        />
      </div>
      <div>
        <h2 className={styles.welcomeMessage}>{en.welcomeMessage}</h2>
      </div>
      <div>
        <p className={styles.welcomeModalBotInformation}>
          {en.welcomeModalInformation}
        </p>
      </div>
      <div className={styles.buttonSet}>
        <Button
          kind="secondary"
          onClick={handleClick}>
          <span className={styles.buttonSetText}>{en.releaseNotes}</span>
        </Button>
        <br />
        <Button
          className={styles.button}
          onClick={handleConfigureApiKey}>
          <span className={styles.buttonSetText}>{en.configureApiKey}</span>
        </Button>
      </div>
    </Modal>
  );
};

export default WelcomeScreen;
