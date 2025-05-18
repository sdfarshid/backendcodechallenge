# SETUP Guide for GitHub Fetcher Service

## Requirements

- **Docker** and **Docker Compose** must be installed on your machine before proceeding.
- Clone the project and make sure you have the `Python/fetcher` directory available (contains necessary config and Docker files).

## Environment Configuration

- Copy the `.env.example` file to `.env`:

  ```bash
  cp .env.example .env
  ```

- Fill in the actual values in `.env` file.  
- ❗️ **Important**: The `POSTGRES_HOST` should be the **same name** as the database service name defined in the Docker Compose file. It's already set correctly as `fetcher_db`, do **not change** it unless you modify the Docker service name.

## Running the Project

1. Go to the fetcher directory:

   ```bash
   cd Python/fetcher
   ```

2. Start the services:

   ```bash
   docker compose up -d
   ```

## Database Setup

- The database tables are managed using **Alembic**.
- To run the migrations inside the container:

  ```bash
  docker exec -it fetcher_app alembic upgrade head
  ```

## FastAPI Server

- Once the container is running, FastAPI will be available on the port you set in the `.env` file (`APP_PORT`, default is `8004`).
- You can access the root endpoint in your browser:

  ```
  http://localhost:8004/
  ```

## GitHub Token

- You must add your **GitHub API Token** in the `.env` file under:

  ```env
  GITHUB_TOKEN=your_token_here
  GITHUB_REPO=nodejs/node
  ```

## Fetching Commits

You can fetch commits using three different methods:

### 1. FastAPI Swagger UI (Manual)

Visit:
```
http://localhost:8004/docs
```
Use available endpoints to fetch and store commits manually.

---

### 2. Docker CLI Execution

Enter the container and run the fetch script:

```bash
docker exec -it fetcher_app /bin/bash
```
```bash
python -m app.scripts.fetch_commits --count 20
```

> This method fetches the latest commits in the background.

---

### 3. Main Root Endpoint

The root FastAPI endpoint serves as the main entry point for service info and health-checks:

```
http://localhost:8004/
```

---

## Running Tests

To run tests:

1. Enter the container:

   ```bash
   docker exec -it fetcher_app /bin/bash
   ```

2. Navigate to the tests folder:

   ```bash
   cd tests
   ```

3. Run all tests:

   ```bash
   pytest
   ```

4. Run a specific test file:

   ```bash
   pytest test_fetcher_factory.py
   ```

---

## Example `.env` Structure

```env
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=fetcher_db
POSTGRES_PORT=5435
APP_PORT=8004
GITHUB_TOKEN=
GITHUB_REPO=nodejs/node
```
