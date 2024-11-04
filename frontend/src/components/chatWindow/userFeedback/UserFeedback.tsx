/*
 * {COPYRIGHT-TOP}
 * IBM Confidential
 * (C) Copyright IBM Corp. 2019, 2022, 2023, 2024
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

import {
  ThumbsDown,
  ThumbsDownFilled,
  ThumbsUp,
  ThumbsUpFilled,
} from '@carbon/icons-react';
import { Button } from 'carbon-components-react';
import React, { useState } from 'react';
import en from 'src/locals/en.json';
import styles from './UserFeedback.module.scss';

interface UserFeedbackProps {
  id: string;
}

const UserFeedback: React.FC<UserFeedbackProps> = ({ id }) => {
  const [likeClicked, setLikeClicked] = useState(false);
  const [dislikeClicked, setDislikeClicked] = useState(false);

  const handleLike = () => {
    setLikeClicked(true);
    setDislikeClicked(false);
  };

  const handleDislike = () => {
    setDislikeClicked(true);
    setLikeClicked(false);
  };

  return (
    <div
      id={id}
      className={styles.userFeedbackContainer}>
      <Button
        hasIconOnly
        renderIcon={likeClicked ? ThumbsUpFilled : ThumbsUp}
        iconDescription={en.like}
        size="sm"
        className={styles.feedbackButton}
        onClick={handleLike}
      />
      <Button
        hasIconOnly
        renderIcon={dislikeClicked ? ThumbsDownFilled : ThumbsDown}
        iconDescription={en.disLike}
        size="sm"
        className={styles.feedbackButton}
        onClick={handleDislike}
      />
    </div>
  );
}

export default UserFeedback;
