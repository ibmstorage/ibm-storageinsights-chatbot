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
import { LineChart } from '@carbon/charts-react';
import en from 'src/locals/en.json';
import { DARK_THEME_CONSTANT, GIB } from 'src/utils/Constants';
import commonStyles from './Common.module.scss';

interface MetricChartProperties {
  metricsDataMessage: any;
  typingComplete: any;
}
const MetricsChart: React.FC<MetricChartProperties> = ({
  metricsDataMessage,
  typingComplete,
}) => {
  const transformChartData = (messageData: any) => {
    const { data } = messageData;

    const metricKey = Object.keys(data[0]).find((key) => key !== 'timeStamp');
    const groupName = metricKey;
    const yAxisTitle =
      metricKey
        ?.replace(/_/g, ' ')
        .toLowerCase()
        .replace(/^\w/, (c) => c.toUpperCase());

    const transformedData = data.map((entry: any) => ({
      group: groupName,
      date: new Date(entry.timeStamp).toISOString(),
      value: entry[metricKey],
    }));

    return {
      data: transformedData,
      options: {
        title: '',
        axes: {
          bottom: {
            title: en.time,
            mapsTo: 'date',
            scaleType: 'time',
          },
          left: {
            mapsTo: 'value',
            title: yAxisTitle,
            scaleType: 'linear',
          },
        },
        color: {
          scale: {
            yAxisTitle: 'blue',
          },
        },
        curve: 'curveMonotoneX',
        height: '400px',
        theme: DARK_THEME_CONSTANT,
      },
    };
  };
  const formmatedChartData = transformChartData(metricsDataMessage);

  return (
    <div
      id="metricsLineChart"
      className={`${commonStyles['grid-container']} ${
        typingComplete ? commonStyles['grid-visible'] : ''
      }`}>
      <LineChart
        data={formmatedChartData.data}
        options={formmatedChartData.options}></LineChart>
    </div>
  );
}

export default MetricsChart;
