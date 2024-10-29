# Copyright 2024. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sqlite3
from backend.constants.constants import *


class PreviousActionsDatabaseInitialisation:

    @staticmethod
    def initialize_intent_entity_database():
        """
        Initializes the database by creating the 'intents_and_entities' table if it does not already exist.

        Returns:
            None

        Raises:
            Exception: If an error occurs during the database initialization, an error message is printed.
        """
        try:
            with sqlite3.connect(INTENTS_AND_ENTITIES_FOR_PA) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS intents_and_entities (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    username TEXT,
                                    intent TEXT,
                                    entities TEXT,
                                    userQuery TEXT,
                                    tenantId TEXT
                                )"""
                )
                connection.commit()
                print(
                    "Database initialized successfully for ",
                    INTENTS_AND_ENTITIES_FOR_PA,
                )
        except Exception as e:
            print("Error initializing database:", e)
            raise e
