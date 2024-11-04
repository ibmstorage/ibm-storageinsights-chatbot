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
  BOT,
  dataIdentifier,
  EXECUTE_PERVIOUS_ACTIONS_ROUTINE,
  GET_PERVIOUS_ACTIONS_ROUTINE,
  intentDescMap,
  MORNING_CUP_OF_COFFEE_ROUTINE,
  USER,
} from "src/utils/Constants";
import en from "src/locals/en.json";
import { botMarkdownMessage } from "src/utils/CommonUtil";

const ConversationHistoryTransformer = {
  getTransformedConversations(response: any) {
    const historyList: any = [];
    if (response) {
      let previous: any = null;
      response?.forEach((object: any) => {
        switch (object?.routine) {
          case MORNING_CUP_OF_COFFEE_ROUTINE: {
            const extractedData = object?.Response?.responseData;
            if (extractedData) {
              const consolidatedRoutineData = extractedData.map((object_) => ({
                text: object_?.description,
                sender: BOT,
                identifier: object_?.identifier,
                data:
                  object_?.intent === "storage-list"
                    ? object_?.data
                    : object_?.data?.data,
                intent: object_?.intent,
                id: Date.now(),
                loading: false,
              }));
              const morningCupOfCoffeeData = {
                text: "",
                sender: BOT,
                identifier: dataIdentifier.grids,
                data: consolidatedRoutineData,
                id: Date.now(),
                loading: false,
                link: object?.link,
              };
              const userInputMessage = {
                text: en.morningCupOfCoffeeQuery,
                sender: USER,
              };

              if (
                previous?.Response?.responseData?.intent !==
                "morning-cup-of-coffee"
              ) {
                historyList.push(userInputMessage);
              }

              historyList.push(morningCupOfCoffeeData);
            }

            break;
          }
          case GET_PERVIOUS_ACTIONS_ROUTINE: {
            const previousActionsList = object?.Response?.responseData;
            if (previousActionsList) {
              const textMessage = previousActionsList?.message;
              const previousActionsData = {
                text: textMessage,
                sender: BOT,
                identifier: previousActionsList.identifier,
                data: previousActionsList?.previous_actions,
                intent: previousActionsList?.intent,
                id: Date.now(),
                loading: false,
              };
              const userInputMessage = {
                text: en.previousActionsQuery,
                sender: USER,
              };
              historyList.push(userInputMessage, previousActionsData);
            }

            break;
          }
          case EXECUTE_PERVIOUS_ACTIONS_ROUTINE: {
            const previousActionsObject = object?.Response?.responseData;
            if (previousActionsObject) {
              const userMessage = {
                text: object?.Message,
                sender: USER,
                id: Date.now(),
                identifier: "TEXT",
              };

              const previousActionsData = {
                text: intentDescMap[previousActionsObject?.intent] ?? "",
                sender: BOT,
                identifier: previousActionsObject.identifier,
                data: botMarkdownMessage(previousActionsObject),
                intent: previousActionsObject?.intent,
                id: Date.now(),
                loading: false,
              };
              historyList.push(userMessage, previousActionsData);
            }

            break;
          }
          default: {
            const userMessage = {
              text: object.Message,
              sender: USER,
              id: Date.now(),
              identifier: "TEXT",
            };

            const responseData = object?.Response?.responseData;

            const botMessage = {
              text: intentDescMap[responseData?.intent] ?? "",
              data: botMarkdownMessage(responseData),
              sender: BOT,
              id: Date.now(),
              identifier: responseData?.identifier,
              intent: responseData?.intent,
              link: responseData?.link,
            };
            historyList.push(userMessage);
            if (responseData?.intent !== "morning-cup-of-coffee") {
              historyList.push(botMessage);
            }
          }
        }
        previous = object;
      });
    }
    return historyList;
  },
};

export default ConversationHistoryTransformer;
