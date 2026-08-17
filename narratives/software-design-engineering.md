# Enhancement One: Software Design and Engineering

## Artifact Overview

The artifact I selected for this enhancement is the Grazioso Salvare Animal Shelter Dashboard, originally developed during CS 340: Client/Server Development. The project uses Python, MongoDB, Dash, Pandas, Plotly, and Dash Leaflet to create an interactive dashboard for working with animal shelter data. The application allows users to filter animal records according to rescue categories, view the resulting records in a data table, analyze breed distribution through a visualization, and display animal locations on an interactive map.

I selected this artifact because it demonstrates several areas of computer science working together within one application. The original project successfully met its functional requirements, but reviewing it later in CS 499 allowed me to identify opportunities to improve the overall software design, maintainability, security, and reliability of the application.

## Justification for Inclusion

I included this artifact in my ePortfolio because it demonstrates my growth as a software developer. The original version showed that I could create a functional client/server application and connect a user interface to a MongoDB database. The enhanced version demonstrates that I can revisit existing software, evaluate its design, identify weaknesses, and improve the implementation using better software engineering practices.

One important improvement involved separating configuration information from the application logic. The original project contained database credentials directly within the application code. During the enhancement, I moved configuration responsibilities into a separate `config.py` module and used environment variables for sensitive database credentials. This reduces the exposure of authentication information and makes the application easier to configure in different environments.

I also improved the `AnimalShelter` class. The enhanced version includes input validation, structured exception handling, logging, clearer method documentation, type hints, and improved MongoDB connection management. The CRUD methods now validate their input before executing database operations and provide meaningful errors when operations fail.

These changes make the code easier to understand, maintain, test, and extend. They also demonstrate the difference between simply creating software that works and designing software that can be maintained responsibly over time.

## Software Design and Engineering Improvements

The enhancement focused on improving the architecture and quality of the existing application.

The database access layer was redesigned to provide a clearer separation between the user interface and data management responsibilities. The `AnimalShelter` class is responsible for MongoDB operations while the dashboard handles presentation and user interaction.

The MongoDB connection process was also improved. Credentials are no longer intended to be hard-coded directly into the dashboard. Instead, the application retrieves configuration information through a separate configuration module backed by environment variables.

Error handling was another important improvement. Database operations are now wrapped in exception handling so failures can be reported in a controlled manner rather than causing unexpected application behavior. Logging was added to provide useful information about database connections and CRUD operations.

Input validation was added to CRUD methods to verify that the expected dictionary structures are provided before database operations occur. Type hints and docstrings were also incorporated to make the purpose and expected inputs and outputs of methods easier for another developer to understand.

Together, these improvements increased the modularity, readability, maintainability, reliability, and security of the application.

## Course Outcomes

This enhancement helped me make progress toward several Computer Science program outcomes.

The strongest connection is to the outcome requiring students to use well-founded techniques, skills, and tools in computing practices to implement solutions that deliver value and accomplish industry-specific goals. Enhancing the dashboard required me to evaluate an existing application and apply software engineering practices rather than simply adding functionality.

The enhancement also contributed to the security outcome. Moving sensitive configuration information away from the main application code demonstrates a stronger security mindset and an understanding that credentials should not be embedded directly in source code.

I also strengthened my ability to design and communicate technical solutions. The improved organization, documentation, naming, and separation of responsibilities make the application easier for another developer to understand and maintain.

Additional enhancements in the algorithms and data structures and database categories further demonstrate the remaining program outcomes across the completed ePortfolio.

## Reflection

The enhancement process taught me that software development does not end when an application begins working. My original project accomplished its intended purpose, but reviewing the code later showed me several areas where the implementation could be improved.

One of the biggest lessons I learned was the importance of separation of concerns. Database operations, configuration management, application logic, and presentation should have clearly defined responsibilities. Separating these responsibilities made the application easier to understand and reduced unnecessary dependencies between components.

I also developed a better understanding of secure configuration management. Hard-coded credentials may be convenient during early development, but they create unnecessary security risks. Using environment variables and a separate configuration module provided a more appropriate approach.

Another challenge was improving the existing code without changing the fundamental purpose of the application. I had to consider how each modification affected other components and ensure that the dashboard could continue communicating with MongoDB correctly.

Overall, this enhancement demonstrates my growth from building software primarily to satisfy functional requirements toward thinking about maintainability, security, reliability, documentation, and long-term software quality. The final artifact better represents the software engineering skills I have developed throughout the Computer Science program.
