# Application Overview

Eprice is an application that show users market electricity price and additional related information, such as electricity consumption and production. For non-registered users, only the current 24 hour period is covered, and only the market price is shown. For registered users, also historical data is available for market price and for production/consumption. The data is represented with graphs and statistics.

For registered users there is also a chat-engine available, which has access to specific source material, and which augments the user queries with retrieved context information. 

---

## Services Overview

The system consists of multiple containerized services that work together to provide functionality for the Eprice application, including a database, backend server, client application, and additional components for migrations, testing, and a chat engine.

### 1. Database
- **Ports**: `5432` (default PostgreSQL port)
- **Purpose**: Stores application data, including user information and embeddings for retrieval.

### 2. Database Migrations
- **Purpose**: Handles database schema migrations.
- **Depends On**: `Database`

### 3. Server
- **Ports**: `8000`
- **Purpose**: Provides backend APIs for the client and other services.
- **Depends On**: `Database`
- **Additional Functionality**: Makes external API calls.

### 4. Client
- **Ports**: `5173` (Svelte client)
- **Purpose**: Frontend application for user interaction.
- **Depends On**: `Server`, `Chat Engine`

### 5. E2E Tests
- **Purpose**: Runs end-to-end tests for the system.
- **Depends On**: `Client`

### 6. Chat Engine
- **Ports**: `7860`
- **Purpose**: Provides a chat engine for interaction with the system.
- **Depends On**: `Database`

---


```plantuml

@startuml
title Main services and their interactions
skinparam rectangle {
    BackgroundColor #FDF6E3
    BorderColor #586e75
}
skinparam cloud {
    BackgroundColor #FDF6E3
    BorderColor #586e75
}

cloud "Docker Network\nmanages networking" as DockerNetwork

package "Database Layer" {
    [Database] <<container>> 
    [Database Migrations] <<container>> 
}

package "Backend Layer" {
    [Server] <<container>> 
    [Chat Engine] <<container>> 
}

package "Frontend Layer" {
    [Client] <<container>> 
    [E2E Tests] <<container>> 
}

cloud "External APIs" as ExternalAPIs

[Database Migrations] --> [Database] : Applies migrations
[Server] --> [Database] : Reads/Writes data
[Client] --> [Server] : API calls (port 8000)
[Client] --> [Chat Engine] : LLM service (port 7860)
[Chat Engine] --> [Database] : Reads/Writes embeddings\nand retrieves texts
[E2E Tests] --> [Client] : Tests frontend
[Server] --> ExternalAPIs : Makes external API calls

note right of Client
Runs on port 5173
end note

@enduml
```

## Additional Services Overview

### Data-preparation

- **Purpose**: Can be used independently to retrieve or update data. Saves data to a location that is available to migrations and the database.

### Backend-tests

- **Purpose**: Can be used to test backend functionality independently from the frontend. Beyond fault testing, backend-tests also give additional information and warnings which would be hidden from the e2e-tests.
- **Depends On**: Database and Server.

The backend tests are mainly for development purposes, as the e2e-tests should cover the main functionalities by the end of development.
