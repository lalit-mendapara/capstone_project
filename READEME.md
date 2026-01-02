How to Run the Project

Follow these steps to get the system running on your local machine using Docker.

### 1. Prerequisites
- [Docker](https://www.docker.com/get-started) installed on your machine.
- An **OpenRouter API Key** for the AI model.

### 2. Clone the Repository
```bash
git clone "repo link"
cd capstone_project

# Create a .env file in the root directory and add the following:
# Database Settings
DB_URL=""
# Redis Settings
REDIS_URL=""

# Vector DB Settings
QDRANT_URL=""

# AI Model Settings (OpenRouter)
OPENROUTER_KEY=your_api_key_here
OPENROUTER_BASE_URL=""
MODEL=""

# Run the following command to start all services (API, Worker, DB, Redis, Qdrant):
docker-compose up --build