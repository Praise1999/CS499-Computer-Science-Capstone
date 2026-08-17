# Enhancement Two: Algorithms and Data Structures

## Artifact Overview

The artifact selected for my Algorithms and Data Structures enhancement is the Grazioso Salvare Animal Shelter Dashboard, originally developed during CS 340: Client/Server Development. The application was created using Python and MongoDB and uses Dash to provide an interactive interface for viewing and analyzing animal shelter records.

The dashboard allows users to retrieve animal information from a MongoDB database, filter animals according to rescue requirements, display the results in a searchable and sortable table, visualize breed distributions, and display the location of selected animals on an interactive map.

I selected this artifact for my CS 499 ePortfolio because it provided an opportunity to demonstrate how algorithms and data structures can improve the way an application processes, organizes, searches, and presents data.

## Justification for Inclusion

I included this artifact because the application works with a large collection of animal records and requires decisions about how that information should be retrieved and processed.

The original application successfully filtered animals according to different rescue categories, including water rescue, mountain or wilderness rescue, and disaster or individual tracking. However, reviewing the project during CS 499 helped me recognize that the filtering process itself represents an important algorithmic component of the application.

Instead of treating every animal record equally, the application creates specific MongoDB query structures based on the rescue category selected by the user. These queries use fields such as breed and sex upon outcome to determine which animals satisfy the required conditions.

The enhanced version improves the organization of this filtering logic and provides a clearer relationship between user selections, query construction, database retrieval, and the data displayed to the user.

## Algorithms and Data Structures Enhancement

One of the major areas of improvement involved the filtering algorithm used by the dashboard.

The application supports multiple rescue categories. Each category requires a different combination of characteristics. For example, a water rescue search may require specific breeds and a particular sex classification, while mountain or wilderness rescue requires a different group of breeds.

The dashboard translates the selected category into a MongoDB query dictionary. Python dictionaries provide an appropriate data structure because they represent the relationship between database fields and the values or conditions used to search those fields.

For breed filtering, the application uses MongoDB's `$in` operator. This allows several acceptable breeds to be represented as a collection and evaluated through one database query instead of manually iterating through every animal record in Python.

This design is important because filtering is performed by MongoDB before the records are returned to the dashboard. Rather than retrieving every document from the database and then checking every record individually in the application, the database returns records that satisfy the specified conditions.

The resulting records are converted into a Pandas DataFrame. The DataFrame provides a structured representation of the retrieved information and supports efficient manipulation of rows and columns.

The dashboard's DataTable also provides native sorting and filtering capabilities. This gives the user another level of interaction with the results without requiring separate algorithms to be manually implemented for every table operation.

## Data Processing and Visualization

The enhancement also demonstrates how data structures support other parts of the application.

After records are retrieved, they are converted into dictionaries and DataFrames depending on how the information is being used. MongoDB queries use dictionary structures, database results are represented as lists of dictionaries, and Pandas DataFrames provide tabular structures for analysis and visualization.

The visualization component uses the filtered DataFrame to calculate and display the distribution of animal breeds through a Plotly pie chart. This means the visualization responds to the current dataset instead of displaying information from the entire database regardless of the selected filter.

The map component also works with the filtered dataset. When a user selects a row, the application identifies the corresponding record and retrieves the latitude and longitude values required to position the marker.

These interactions demonstrate how the same structured dataset can support multiple operations, including filtering, sorting, visualization, and geographic representation.

## Algorithmic Efficiency and Trade-Offs

An important part of this enhancement was considering where data processing should occur.

One possible design would be to retrieve all animal records from MongoDB and use Python loops to examine each record. While this approach could work for a small dataset, it would become increasingly inefficient as the number of records grows.

The enhanced approach pushes filtering responsibilities to MongoDB. The application constructs a query that describes the required conditions and allows the database management system to identify matching documents.

This reduces the amount of unnecessary data transferred between MongoDB and the dashboard and reduces the amount of processing required by the application.

There is a trade-off in this design because the application becomes more dependent on MongoDB's query language. However, for a database-driven application, using the database engine for filtering is more appropriate than reproducing the same filtering process manually in Python.

This enhancement helped me understand that algorithm design involves more than choosing a particular sorting or searching algorithm. It also involves deciding where computation should occur, selecting appropriate data structures, reducing unnecessary operations, and considering the performance implications of different design choices.

## Course Outcomes

This enhancement most directly demonstrates the Computer Science program outcome requiring students to design and evaluate computing solutions using algorithmic principles and computer science practices while managing trade-offs involved in design choices.

The dashboard uses structured query logic to solve the problem of identifying animals that satisfy specific rescue requirements. The use of dictionaries, lists, DataFrames, database queries, and interactive filtering demonstrates my ability to select and use data structures according to the needs of an application.

The enhancement also supports the outcome related to implementing computing solutions that deliver value and accomplish industry-specific goals. In the context of Grazioso Salvare, efficiently identifying animals with characteristics appropriate for different rescue roles provides meaningful functionality for the intended organization.

The project also contributes to professional communication because the dashboard transforms raw database records into tables, visualizations, and maps that make the information easier for users to understand and use when making decisions.

## Reflection

Enhancing this artifact changed the way I think about algorithms and data structures. Earlier in the Computer Science program, I often associated algorithms primarily with traditional examples such as sorting algorithms, searching algorithms, loops, and recursion. This project helped me see algorithmic thinking in a broader context.

The process of translating a user's rescue selection into a structured database query is itself an algorithmic process. The application receives an input, determines the appropriate conditions, constructs a query, retrieves matching records, transforms the results into useful data structures, and presents those results to the user.

One challenge was deciding which operations should be handled by Python and which should be handled by MongoDB. Processing everything within Python would have been straightforward, but it would also require retrieving unnecessary records. Allowing MongoDB to perform the filtering provides a cleaner and more scalable solution.

I also gained a stronger appreciation for choosing appropriate data structures. Dictionaries are effective for representing query conditions, lists of dictionaries work naturally with MongoDB results, and DataFrames provide useful functionality for manipulating and visualizing tabular data.

Overall, this enhancement demonstrates my ability to analyze an existing computing solution and improve the way it organizes and processes information. It also shows my growth in understanding that good algorithm design requires consideration of efficiency, scalability, readability, and the trade-offs associated with different implementation approaches.
