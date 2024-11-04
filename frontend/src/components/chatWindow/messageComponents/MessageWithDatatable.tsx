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
import commonStyles from 'src/components/chatWindow/messageComponents/Common.module.scss';
import { Export } from '@carbon/icons-react';
import { Button } from 'carbon-components-react';
import { formatTableHeaders, formatTableRows } from 'src/utils/CommonUtil';
import en from 'src/locals/en.json';
import { exportTableFilename } from 'src/utils/Constants';
import PaginatedDatatable from './PaginatedDatatable';
import MaskedLink from './MaskedLink';


interface MessageWithDatatableProps {
  key: string | number;
  message: any;
  isSummaryData?: boolean;
}

interface Header {
  header: string;
  key: string;
}

const MessageWithDatatable: React.FC<MessageWithDatatableProps> = ({
  key,
  message,
  isSummaryData,
}) => {
  const exportToCSV = () => {
    const headers = Object.keys(message.data[0]);
    const headerData = formatTableHeaders(headers);
    const rowData = formatTableRows(message, headerData);
    const csvDataset = [headerData.map((header: Header) => header.header)];
    for (const row of rowData) {
      const rowData = headerData.map((header: Header) => row[header.key]);
      csvDataset.push(rowData);
    }
    const csvDataContent = csvDataset.map((row) => row.join(',')).join('\n');
    const blob = new Blob([csvDataContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${exportTableFilename}.csv`);
    document.body.append(link);
    link.click();
    link.remove();
  };

  return (
    <div id="dataTableContainer">
      <div>
          <div className={` ${commonStyles.bot}`}>
            <div className={commonStyles.infoDataTableContainer}>
              <div className={commonStyles.infoText}>
                {isSummaryData && message?.data?.length === 0 ? (
                  <span className={commonStyles.noDataMessageContainer}>
                      {message.text}
                    </span>
                ) : (
                  <div className={commonStyles.chatMessage}>{message.text}</div>
                )}
              </div>
              {message?.data?.length ? (
                <div className={commonStyles.exportButtonWrapper}>
                  <Button
                    key={`${message.intent}, ${message.id}`}
                    onClick={exportToCSV}
                    hasIconOnly
                    renderIcon={Export}
                    iconDescription={en.exportIconDesc}
                    size="md"
                    className={commonStyles.exportBtnBackground} />
                </div>
              ) : (
                ''
              )}
            </div>
          </div>
          {message?.data?.length ? (
            <PaginatedDatatable
              typingComplete
              message={message} />
          ) : (
            ''
          )}
          {message?.link ? (
            <p className={commonStyles.moreDetails}>
              {en.moreDetails}
              <MaskedLink
                text={en.IbmStorageInsights}
                url={message?.link} />
            </p>
          ) : (
            ''
          )}
        </div>
    </div>
  );
}

export default MessageWithDatatable;
