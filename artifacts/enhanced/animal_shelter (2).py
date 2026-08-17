"""
MongoDB data access module for the Grazioso Salvare dashboard.

CS 499 enhancements include:
- Input validation
- Exception handling
- Logging
- Configurable MongoDB connection
- Optional projection
- Database-side sorting
- Result limiting
- Record counting
"""

import logging
from typing import Any, Sequence
from urllib.parse import quote_plus

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError


LOGGER = logging.getLogger(__name__)


class AnimalShelter:
    """Provide CRUD operations for the animals MongoDB collection."""

    def __init__(
        self,
        username: str,
        password: str,
        host: str = "localhost",
        port: int = 27017,
        database_name: str = "AAC",
        collection_name: str = "animals",
    ) -> None:
        """
        Create and verify the MongoDB connection.

        Args:
            username: MongoDB username.
            password: MongoDB password.
            host: MongoDB host name.
            port: MongoDB port number.
            database_name: Name of the MongoDB database.
            collection_name: Name of the MongoDB collection.

        Raises:
            ValueError: If required connection information is missing.
            ConnectionError: If MongoDB cannot be reached.
        """

        if not isinstance(username, str) or not username.strip():
            raise ValueError(
                "MongoDB username is required."
            )

        if not isinstance(password, str) or not password:
            raise ValueError(
                "MongoDB password is required."
            )

        if not isinstance(host, str) or not host.strip():
            raise ValueError(
                "MongoDB host is required."
            )

        if not isinstance(port, int) or port <= 0:
            raise ValueError(
                "MongoDB port must be a positive integer."
            )

        if (
            not isinstance(database_name, str)
            or not database_name.strip()
        ):
            raise ValueError(
                "Database name is required."
            )

        if (
            not isinstance(collection_name, str)
            or not collection_name.strip()
        ):
            raise ValueError(
                "Collection name is required."
            )

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

            # Confirm that MongoDB is available.
            self.client.admin.command("ping")

            self.database = self.client[database_name]
            self.collection = self.database[
                collection_name
            ]

            LOGGER.info(
                "Connected to database '%s' and collection '%s'.",
                database_name,
                collection_name,
            )

        except PyMongoError as error:
            LOGGER.exception(
                "Unable to connect to MongoDB."
            )

            raise ConnectionError(
                "The application could not connect to MongoDB."
            ) from error

    @staticmethod
    def _validate_dictionary(
        value: Any,
        argument_name: str,
        allow_empty: bool = False,
    ) -> None:
        """
        Validate dictionaries passed to CRUD methods.

        Args:
            value: Value to validate.
            argument_name: Name used in error messages.
            allow_empty: Whether an empty dictionary is acceptable.
        """

        if value is None:
            raise ValueError(
                f"{argument_name} cannot be None."
            )

        if not isinstance(value, dict):
            raise TypeError(
                f"{argument_name} must be a dictionary."
            )

        if not allow_empty and not value:
            raise ValueError(
                f"{argument_name} cannot be empty."
            )

    @staticmethod
    def _validate_limit(limit: int | None) -> None:
        """Validate an optional result limit."""

        if limit is None:
            return

        if not isinstance(limit, int):
            raise TypeError(
                "limit must be an integer or None."
            )

        if limit <= 0:
            raise ValueError(
                "limit must be greater than zero."
            )

    @staticmethod
    def _validate_sort(
        sort: Sequence[tuple[str, int]] | None,
    ) -> None:
        """
        Validate MongoDB sort instructions.

        Expected format:
            [("breed", 1), ("name", -1)]
        """

        if sort is None:
            return

        if not isinstance(sort, (list, tuple)):
            raise TypeError(
                "sort must be a list or tuple of field-direction pairs."
            )

        for sort_item in sort:
            if (
                not isinstance(sort_item, (list, tuple))
                or len(sort_item) != 2
            ):
                raise TypeError(
                    "Each sort item must contain a field and direction."
                )

            field, direction = sort_item

            if not isinstance(field, str) or not field.strip():
                raise ValueError(
                    "Sort field names must be non-empty strings."
                )

            if direction not in (
                ASCENDING,
                DESCENDING,
                1,
                -1,
            ):
                raise ValueError(
                    "Sort direction must be 1 or -1."
                )

    def create(
        self,
        data: dict[str, Any],
    ) -> bool:
        """
        Insert one animal record.

        Returns:
            True when MongoDB acknowledges the insertion.
        """

        self._validate_dictionary(
            data,
            "data",
        )

        try:
            result = self.collection.insert_one(data)

            LOGGER.info(
                "Created animal document with ID %s.",
                result.inserted_id,
            )

            return result.acknowledged

        except PyMongoError as error:
            LOGGER.exception(
                "Failed to create animal document."
            )

            raise RuntimeError(
                "The animal record could not be created."
            ) from error

    def read(
        self,
        query: dict[str, Any] | None = None,
        projection: dict[str, Any] | None = None,
        sort: Sequence[tuple[str, int]] | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Return animal records matching a MongoDB query.

        Args:
            query:
                MongoDB query dictionary. An empty dictionary retrieves
                all records.

            projection:
                Optional dictionary identifying fields to include or
                exclude. MongoDB's internal _id field is excluded by
                default.

            sort:
                Optional sequence of field-direction pairs.

                Example:
                    [("breed", 1), ("name", 1)]

            limit:
                Optional maximum number of records to return.

        Returns:
            A list of dictionaries containing animal records.
        """

        if query is None:
            query = {}

        self._validate_dictionary(
            query,
            "query",
            allow_empty=True,
        )

        if projection is None:
            projection = {"_id": False}
        else:
            self._validate_dictionary(
                projection,
                "projection",
                allow_empty=True,
            )

            # Prevent MongoDB ObjectId values from entering the DataFrame.
            projection = dict(projection)
            projection["_id"] = False

        self._validate_sort(sort)
        self._validate_limit(limit)

        try:
            cursor = self.collection.find(
                query,
                projection,
            )

            if sort:
                cursor = cursor.sort(list(sort))

            if limit is not None:
                cursor = cursor.limit(limit)

            results = list(cursor)

            LOGGER.info(
                "Read operation returned %d record(s).",
                len(results),
            )

            return results

        except PyMongoError as error:
            LOGGER.exception(
                "Failed to read animal documents."
            )

            raise RuntimeError(
                "Animal records could not be retrieved."
            ) from error

    def count(
        self,
        query: dict[str, Any] | None = None,
    ) -> int:
        """
        Count animal records that match a query.

        MongoDB performs the count without transferring every matching
        document into the application.
        """

        if query is None:
            query = {}

        self._validate_dictionary(
            query,
            "query",
            allow_empty=True,
        )

        try:
            total = self.collection.count_documents(
                query
            )

            LOGGER.info(
                "Count operation returned %d record(s).",
                total,
            )

            return total

        except PyMongoError as error:
            LOGGER.exception(
                "Failed to count animal documents."
            )

            raise RuntimeError(
                "Animal records could not be counted."
            ) from error

    def update(
        self,
        query: dict[str, Any],
        data: dict[str, Any],
    ) -> int:
        """
        Update matching records.

        Returns:
            Number of records modified.
        """

        self._validate_dictionary(
            query,
            "query",
        )

        self._validate_dictionary(
            data,
            "data",
        )

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
            LOGGER.exception(
                "Failed to update animal documents."
            )

            raise RuntimeError(
                "Animal records could not be updated."
            ) from error

    def delete(
        self,
        query: dict[str, Any],
    ) -> int:
        """
        Delete matching records.

        Returns:
            Number of records deleted.
        """

        self._validate_dictionary(
            query,
            "query",
        )

        try:
            result = self.collection.delete_many(
                query
            )

            LOGGER.info(
                "Deleted %d animal record(s).",
                result.deleted_count,
            )

            return result.deleted_count

        except PyMongoError as error:
            LOGGER.exception(
                "Failed to delete animal documents."
            )

            raise RuntimeError(
                "Animal records could not be deleted."
            ) from error

    def close(self) -> None:
        """Close the MongoDB client connection."""

        if hasattr(self, "client"):
            self.client.close()

            LOGGER.info(
                "MongoDB connection closed."
            )