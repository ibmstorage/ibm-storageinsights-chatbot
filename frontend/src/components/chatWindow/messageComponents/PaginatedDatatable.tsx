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

import {
  DataTable,
  Pagination,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from 'carbon-components-react';
import React, { useState } from 'react';
import { columnListMap } from 'src/utils/Constants';
import { formatTableHeaders, formatTableRows } from 'src/utils/CommonUtil';
import en from 'src/locals/en.json';
import styles from './Common.module.scss';
import commonStyles from './Common.module.scss';
import { PaginationDetails } from 'src/typings/PaginationDetails';
import { Message } from 'src/typings/Message';

interface PaginatedDatatableProps {
  typingComplete: boolean;
  message: Message
}

const PaginatedDatatable: React.FC<PaginatedDatatableProps> = ({
  typingComplete,
  message,
}) => {
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(5);
  let headersData = [];
  let rowData = [];

  const changePaginationState = (pageInfo: PaginationDetails) => {
    if (page !== pageInfo.page) {
      setPage(pageInfo.page);
    }
    if (pageSize !== pageInfo.pageSize) {
      setPageSize(pageInfo.pageSize);
    }
  };

  if (
    message &&
    message.data &&
    message.intent &&
    columnListMap[message.intent]
  ) {
    const headers = columnListMap[message.intent];
    headersData = formatTableHeaders(headers);
    rowData = formatTableRows(message, headersData);
  }

  return (
    <div
      className={`${styles['grid-container']} ${
        typingComplete ? styles['grid-visible'] : ''
      }`}>
      <DataTable
        rows={rowData}
        isSortable
        headers={headersData}
        size="md">
        {({ rows, headers, getTableProps, getHeaderProps, getRowProps }) => (
          <Table {...getTableProps()}>
            <TableHead>
              <TableRow>
                {headers?.map((header: any) => (
                  <TableHeader {...getHeaderProps({ header })}>
                    {header.header}
                  </TableHeader>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows
                .slice((page - 1) * pageSize)
                .slice(0, pageSize)
                .map((row: any, index: number) => {
                  const rowId = row.id || index;
                  return (
                    <TableRow
                      id={rowId}
                      key={rowId}
                      {...getRowProps({ row })}>
                      {row.cells.map((cell: any, cellIndex: number) => (
                        <TableCell
                          key={cellIndex}
                          className={
                            cell.info.header === 'ip_address'
                              ? commonStyles.columnWordBreak
                              : ''
                          }>
                          {cell.value}
                        </TableCell>
                      ))}
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        )}
      </DataTable>
      {rowData.length > 0 ? (
        <Pagination
          backwardText={en.previousPage}
          forwardText={en.nextPage}
          itemsPerPageText={en.itemsPerPage}
          onChange={changePaginationState}
          page={page}
          pageSize={pageSize}
          pageSizes={[5, 10, 20, 50]}
          totalItems={rowData.length}
        />
      ) : (
        ''
      )}
    </div>
  );
};

export default PaginatedDatatable;
