import uuid

import psycopg
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_postgres import PostgresChatMessageHistory

from chat_app.config import config


def get_chat_from_db(db_name: str | None = None) -> BaseChatMessageHistory:
    configs = config.get()
    match db_name or configs.database_provider:
        case "sqlite3":
            return SQLChatMessageHistory(
                session_id="test_session", connection="sqlite:///chat_app.db"
            )

        case "postgres":
            session_id = str(uuid.uuid4())

            conn_info = ""
            sync_connection = psycopg.connect(conn_info)

            # Create the table schema (only needs to be done once)
            table_name = "chat_history"
            PostgresChatMessageHistory.create_tables(sync_connection, table_name)
            return PostgresChatMessageHistory(
                table_name, session_id, sync_connection=sync_connection
            )

        case _:
            return SQLChatMessageHistory(
                session_id="test_session", connection_string="sqlite:///chat_app.db"
            )
