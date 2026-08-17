# Enhancement Three: Databases

## Artifact Overview

The artifact selected for my Database enhancement is the Grazioso Salvare Animal Shelter Dashboard, originally developed during CS 340: Client/Server Development. The project uses Python, MongoDB, Dash, Pandas, Plotly, and Dash Leaflet to create an interactive application for retrieving and displaying animal shelter information.

The original project required the development of a Python CRUD module that communicates with a MongoDB database containing animal shelter records. The dashboard uses this data access layer to retrieve animal information and allows users to filter records according to different rescue categories.

I selected this artifact for my database enhancement because database interaction is a central part of the application. Without the MongoDB database and the `AnimalShelter` data access class, the dashboard would not be able to retrieve or manage the information needed by the user. Enhancing this artifact gave me the opportunity to demonstrate my growth in database programming, security, validation, exception handling, query design, and software architecture.

## Justification for Inclusion

I included this artifact in my ePortfolio because it demonstrates both my original understanding of database programming and the improvements I have made since completing CS 340.

The original `AnimalShelter` class provided Create, Read, Update, and Delete operations for MongoDB. These CRUD operations allowed the application to insert animal records, retrieve records matching specific criteria, update existing records, and delete records.

Although the original implementation was functional, reviewing the project during CS 499 revealed several opportunities for improvement. The database layer could be made more secure, maintainable, reliable, and easier to reuse.

The enhanced version improves database connection management, input validation, exception handling, logging, configuration management, and the return values provided by CRUD operations. These improvements demonstrate a more complete understanding of how a database access layer should function within a professional application.

## Database Enhancements

One of the most significant improvements involved restructuring the MongoDB connection.

The original implementation contained connection information directly within the application code. In the enhanced version, the database username and password are obtained through configuration values rather than being embedded directly in the dashboard source code.

The application uses a separate `config.py` module to retrieve the `MONGO_USERNAME` and `MONGO_PASSWORD` environment variables. This creates a clearer separation between application logic and sensitive configuration information.

The enhanced `AnimalShelter` constructor also accepts database connection parameters such as the host, port, database name, and collection name. Providing these as parameters makes the class more reusable and easier to configure for different environments.

The username and password are processed using `quote_plus()` before being included in the MongoDB connection URI. This helps ensure that credentials containing special characters can be safely incorporated into the connection string.

## Improved CRUD Operations

The CRUD methods were also enhanced to provide clearer and more useful behavior.

The `create()` method validates the supplied animal data before attempting to insert it into MongoDB. After the insertion occurs, the method returns whether MongoDB acknowledged the operation.

The `read()` method accepts a MongoDB query dictionary and returns matching records as a list of dictionaries. If no query is provided, an empty dictionary can be used to retrieve all records. The MongoDB `_id` field is excluded from the returned results because it is not required by the dashboard.

The `update()` method validates both the query and the new data before executing `update_many()`. Instead of returning the complete MongoDB result object, the enhanced method returns the number of documents that were actually modified.

The `delete()` method performs similar validation before calling `delete_many()` and returns the number of records deleted.

These return values make the methods easier for other application components to use because they provide clear information about the result of each operation.

## Input Validation and Data Integrity

Another important enhancement involved adding centralized validation.

The enhanced `AnimalShelter` class includes a `_validate_dictionary()` helper method. This method verifies that values passed into CRUD operations are dictionaries and checks whether empty dictionaries should be permitted for a particular operation.

This was an important design decision because different database operations have different requirements. An empty query is acceptable when reading records because it can intentionally mean "retrieve all records." However, allowing an empty query for update or delete operations could unintentionally affect a large number of database records.

The enhanced implementation therefore requires meaningful query dictionaries for update and delete operations.

This validation improves reliability and demonstrates a stronger security mindset because potentially destructive operations are checked before they are sent to MongoDB.

## Exception Handling and Reliability

Database operations can fail for many reasons, including authentication problems, invalid connections, unavailable database services, or unexpected MongoDB errors.

The enhanced version addresses this by using exception handling around MongoDB operations.

The application imports `PyMongoError` and catches database-related exceptions within the CRUD methods. Instead of allowing low-level MongoDB exceptions to propagate throughout the application, the data access layer raises clearer application-level exceptions.

The MongoDB connection is also tested using a `ping` command when the `AnimalShelter` object is created. This verifies that the application can communicate successfully with the database rather than assuming that creating a `MongoClient` automatically means the database connection is working.

A `close()` method was also added to provide an explicit way to close the MongoDB client when the connection is no longer required.

Together, these improvements make database interaction more predictable and reliable.

## Logging

Logging was incorporated into the enhanced database layer to improve visibility into application behavior.

The `AnimalShelter` class records information about successful database connections, read operations, created records, updated records, deleted records, and connection closure.

Errors are also logged when database operations fail.

This is an improvement over relying only on print statements because logging provides a structured mechanism for tracking application behavior. In a larger application, this information could assist developers with troubleshooting, monitoring, and debugging database problems.

## Query Design and Efficiency

The dashboard relies heavily on MongoDB queries to retrieve animals that meet specific rescue requirements.

Instead of retrieving the entire animal collection and manually checking every record in Python, the dashboard constructs MongoDB queries containing the required conditions.

For example, rescue categories use fields such as `breed` and `sex_upon_outcome`. The `$in` operator allows the application to specify multiple acceptable breeds within a single query.

Allowing MongoDB to perform this filtering reduces the amount of unnecessary data transferred from the database to the dashboard.

The resulting records are then converted into a Pandas DataFrame for presentation, visualization, sorting, and additional user interaction.

This design demonstrates the importance of using the database management system for operations it is designed to perform rather than transferring unnecessary processing responsibilities to the client application.

## Security Improvements

Security was an important consideration during this enhancement.

One of the clearest improvements was removing the expectation that database credentials should be directly embedded within the dashboard code. Environment variables provide a safer mechanism for supplying authentication information to the application.

The actual `.env` file containing credentials should not be committed to source control. Only the application code and configuration structure should be included in the repository.

Input validation also contributes to database security. Requiring non-empty queries for update and delete operations reduces the possibility of accidentally modifying or deleting the entire collection.

The enhancement helped me understand that database security is not limited to passwords. It also involves validating operations, controlling configuration information, handling errors carefully, and designing methods that reduce opportunities for unintended data modification.

## Course Outcomes

This enhancement strongly supports the Computer Science program outcome requiring students to use well-founded techniques, skills, and tools in computing practices to implement solutions that deliver value and accomplish industry-specific goals.

MongoDB, PyMongo, Python, environment-based configuration, structured validation, and exception handling were used together to create a more reliable database layer for the Grazioso Salvare application.

The enhancement also demonstrates progress toward the security outcome. Moving credentials outside the main application code, validating database operations, protecting update and delete operations from empty queries, and handling database errors more carefully demonstrate a stronger security mindset.

The project also supports the algorithmic problem-solving outcome because database queries are designed to efficiently retrieve records according to specific conditions rather than requiring the application to process every database record manually.

Finally, the organization and documentation of the enhanced code support professional technical communication. Type hints, docstrings, logging messages, descriptive method names, and separation of responsibilities make the database layer easier for another developer to understand.

## Reflection

Enhancing the database portion of this project helped me understand the difference between simply connecting an application to a database and designing a dependable data access layer.

When I originally completed the project, my primary goal was ensuring that the CRUD operations worked and that the dashboard could retrieve the required information. During CS 499, I approached the same code differently. I considered what would happen if invalid information was provided, the database connection failed, credentials were exposed, or an update or delete operation received an unsafe query.

One challenge involved improving security without making the application unnecessarily difficult to configure. Moving credentials into environment variables required additional configuration, but it provided a much better separation between sensitive information and source code.

Another important lesson involved validation. An empty dictionary can have very different consequences depending on the database operation being performed. For a read operation, `{}` can appropriately represent retrieving all records. For an update or delete operation, however, an empty query could affect the entire collection. Recognizing and managing this difference helped strengthen my understanding of defensive database programming.

I also gained a better appreciation for error handling and logging. A database application should not assume that every operation will succeed. Designing predictable responses to failures makes the application easier to troubleshoot and maintain.

Overall, this enhancement demonstrates significant growth in my understanding of database development. The enhanced artifact does more than perform CRUD operations. It incorporates configuration management, validation, error handling, logging, query design, connection management, and security considerations into a more professional database access layer.

The final version better represents the database knowledge and software development practices I have developed throughout the Computer Science program.
