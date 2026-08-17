"""MongoDB data access module for the Grazioso Salvare dashboard."""

import logging
from typing import Any
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.errors import PyMongoError


LOGGER = logging.getLogger(__name__)


class AnimalShelter:
    """Provide CRUD operations for the animals collection in MongoDB."""

    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 27017,
        database_name: str = "AAC",
        collection_name: str = "animals",
    ) -> None:
        """Create the MongoDB connection."""

        if not username or not password:
            raise ValueError("MongoDB username and password are required.")

        safe_username = quote_plus(username)
        safe_password = quote_plus(password)

        connection_uri = (
            f"mongodb://{safe_username}:{safe_password}"
            f"@{host}:{port}/{database_name}"
        )

        try:
            self.client = MongoClient(
                connection_uri,
                serverSelectionTimeoutMS=5000,
            )

            self.client.admin.command("ping")

            self.database = self.client[database_name]
            self.collection = self.database[collection_name]

            LOGGER.info(
                "Connected to database '%s' and collection '%s'.",
                database_name,
                collection_name,
            )

        except PyMongoError as error:
            LOGGER.exception("Unable to connect to MongoDB.")
            raise ConnectionError(
                "The application could not connect to MongoDB."
            ) from error

    @staticmethod
    def _validate_dictionary(
        value: Any,
        argument_name: str,
        allow_empty: bool = False,
    ) -> None:
        """Validate dictionaries passed to CRUD methods."""

        if value is None:
            raise ValueError(f"{argument_name} cannot be None.")

        if not isinstance(value, dict):
            raise TypeError(f"{argument_name} must be a dictionary.")

        if not allow_empty and not value:
            raise ValueError(f"{argument_name} cannot be empty.")

    def create(self, data: dict[str, Any]) -> bool:
        """Insert one animal record."""

        self._validate_dictionary(data, "data")

        try:
            result = self.collection.insert_one(data)
            LOGGER.info(
                "Created animal document with ID %s.",
                result.inserted_id,
            )
            return result.acknowledged

        except PyMongoError as error:
            LOGGER.exception("Failed to create animal document.")
            raise RuntimeError(
                "The animal record could not be created."
            ) from error

    def read(
        self,
        query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Return animal records matching a MongoDB query."""

        if query is None:
            query = {}

        self._validate_dictionary(
            query,
            "query",
            allow_empty=True,
        )

        try:
            results = list(
                self.collection.find(
                    query,
                    {"_id": False},
                )
            )

            LOGGER.info(
                "Read operation returned %d record(s).",
                len(results),
            )

            return results

        except PyMongoError as error:
            LOGGER.exception("Failed to read animal documents.")
            raise RuntimeError(
                "Animal records could not be retrieved."
            ) from error

    def update(
        self,
        query: dict[str, Any],
        data: dict[str, Any],
    ) -> int:
        """Update records and return the modified count."""

        self._validate_dictionary(query, "query")
        self._validate_dictionary(data, "data")

        try:
            result = self.collection.update_many(
                query,
                {"$set": data},
            )

            LOGGER.info(
                "Update matched %d record(s) and modified %d record(s).",
                result.matched_count,
                result.modified_count,
            )

            return result.modified_count

        except PyMongoError as error:
            LOGGER.exception("Failed to update animal documents.")
            raise RuntimeError(
                "Animal records could not be updated."
            ) from error

    def delete(self, query: dict[str, Any]) -> int:
        """Delete records and return the deleted count."""

        self._validate_dictionary(query, "query")

        try:
            result = self.collection.delete_many(query)

            LOGGER.info(
                "Deleted %d animal record(s).",
                result.deleted_count,
            )

            return result.deleted_count

        except PyMongoError as error:
            LOGGER.exception("Failed to delete animal documents.")
            raise RuntimeError(
                "Animal records could not be deleted."
            ) from error

    def close(self) -> None:
        """Close the MongoDB connection."""

        if hasattr(self, "client"):
            self.client.close()
            LOGGER.info("MongoDB connection closed.")