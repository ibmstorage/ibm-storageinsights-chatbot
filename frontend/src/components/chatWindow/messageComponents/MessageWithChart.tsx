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
import commonStyles from "src/components/chatWindow/messageComponents/Common.module.scss";
import en from "src/locals/en.json";
import { Message } from "src/typings/Message";
import MetricsChart from "./MetricsChart";
import MaskedLink from "./MaskedLink";

interface MessageWithChartProps {
  message: Message;
}

const MessageWithChart: React.FC<MessageWithChartProps> = ({ message }) => {
  const { text, link } = message;
  return (
    <div id="MessageChartContainer">
      <div>
        <div className={`${commonStyles.bot}`}>
          <div className={commonStyles.infoDataTableContainer}>
            <div
              className={`${commonStyles.infoText} ${commonStyles.chatMessage}`}
            >
              {text}
            </div>
          </div>
        </div>
        {message?.data?.length ? (
          <MetricsChart metricsDataMessage={message} typingComplete />
        ) : (
          <></>
        )}
        {message?.data?.length && message?.link ? (
          <p className={commonStyles.moreDetails}>
            {en.moreDetails}
            <MaskedLink text={en.IbmStorageInsights} url={link} />
          </p>
        ) : (
          <></>
        )}
      </div>
    </div>
  );
};

export default MessageWithChart;
