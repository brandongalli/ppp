
# Project Overview

Thank you for reviewing my home-test. This project demonstrates a full-stack solution with a FastAPI + Slim(PHP) backend and a Next.js frontend, designed to handle asynchronous tasks, CRUD operations, and relational data management.

## Summary

### Project Components
- **Frontend**: Built with Next.js, providing a user interface for interacting with the backend.
- **Backend**: FastAPI microservice handling incoming requests, processing tasks asynchronously, and managing API routes.
- **PHP Proxy**: An additional Slim(PHP) API acts as a proxy, forwarding requests to the FastAPI service.
- **Database**: MySQL instance, managed through Docker, stores application data.
- **Queueing**: Redis instance, managed through Docker, supports asynchronous task handling.

### Key Features
1. **Code Structure and Styling**:
   - Adherence to general coding standards for Next.js, Python, and PHP.
   - Modular project structure for maintainability and scalability.
   
2. **Frontend Development**:
   - Built with Next.js for a fast, interactive UI.
   
3. **Backend Development**:
   - FastAPI microservice with CRUD endpoints, async task handling, and JWT-based authorization.
   
4. **Data Generation**:
   - Faker-powered database seeding to populate dummy data for testing.

### Areas for Improvement
Due to time constraints, some enhancements could not be implemented:
- **Error Handling**: Validations are fully implemented only for `Player` creation. Other endpoints may raise `500` errors, which could be handled with additional try-except blocks.
- **Database Design**: Some constraints like enforcing unique combinations (e.g., `Player number + Team name`) are not yet defined.

---

## Project Structure

The project is structured to maintain separation between frontend, backend, and database configurations. Below are key backend modules and their purposes:

- `auth/`: Manages user authentication and authorization.
- `game/`: Handles game-related entities like `Game` and `Stadium`.
- `player/`: Contains player-related models and endpoints.
- `db_config.py`: Database configuration and initialization.
- `worker/`: Celery tasks for async processing.
- `populate_database.py`: Populates the database with dummy data using Faker.

---

## How to Run the Project

### Prerequisites
- Install Docker and Docker Compose.

### Steps
1. Clone the repository and navigate to the project directory.
2. Run the following command to start all services:
   ```bash
   docker compose up
   ```

   ```
   docker compose exec fastapi alembic upgrade head
   ```

### Environment Configuration
1. Copy and paste the environment variables from `env.example` to `.env.local`.
2. Or simply rename `env.example` to `.env.local`.

---

## Testing and Usage

### Setting Up
1. **Create a User**:
   - Register a new user using the `/register` endpoint on FastAPI.
   
2. **Populate Database**:
   - Use the `/populate-db` endpoint to generate dummy data for testing.

3. **Access the Frontend**:
   - Navigate to `http://localhost:3000` in your browser.

### API Endpoints
- **Health Check**: `/healthcheck` – Simple endpoint to verify server status.
- **Authorization**: Token-based authentication with JWT via the `/token` endpoint.
- **CRUD Operations**: 
   - `Player`, `Team`, and `Game` management.
   - Ranking and Stadium endpoints for additional functionality.


## Additional Notes

### Tech Stack
- **Frontend**: Next.js
- **Backend**: FastAPI, Python
- **Proxy API**: Slim(PHP) (bridges between frontend and backend)
- **Database**: MySQL (Dockerized)
- **Queueing**: Redis (Dockerized)

### Improvements for Production
- Enhanced validations and exception handling.
- Database indexing and constraints for unique identifiers (e.g., `Player number + Team`).
- Advanced error handling to prevent unhandled exceptions from returning `500` errors.
