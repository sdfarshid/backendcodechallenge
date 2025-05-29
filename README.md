#  Backend Coding Challenge — GitHub Commits Collector

This repository contains the implementation of a backend coding challenge, built with **Python** and **FastAPI**, following **Domain-Driven Design (DDD)** and **CQRS** architectural principles. The goal is to build a scalable and extendable foundation for a future microservice-based system.

---

##  Tech Stack

- **Language**: Python
- **Framework**: FastAPI
- **Architecture**: Domain-Driven Design (DDD) + CQRS
- **Database**: PostgreSQL
- **Containerization**: Docker
- **ORM/DB Layer**: SQLAlchemy
- **Package Management**: Poetry / pip / Composer (if PHP-based alternative)

---

##  Challenge Description

You are asked to implement the following:

- Retrieve the **1000 most recent commits** (only the commit hashes) from a public GitHub repository.
- Store those commits in a database using a model, making sure **no duplicates** are saved.
- Build a route and view that displays **commits grouped by author** from the database.
- Structure your solution to be flexible for future support of **Bitbucket**, **GitLab**, and other VCS APIs.
- Include automated tests.
- The project must use **Composer** (if PHP) or **Docker** (for deployment).
  
---

##  Setup & Installation

Please refer to the [**`Setup.md`**](./setup.md) file for full environment setup instructions using Docker.

---

## ❓ QA & Design Approach

All architecture decisions, debugging strategies, and microservice readiness explanations are documented in the [**`QA.md`**](./Q-A.md) file.

---

## Requirements Checklist

- [x] Fetch and store latest 1000 GitHub commits
- [x] Avoid saving duplicate commits
- [x] Display commits by author
- [x] Designed for future GitLab/Bitbucket API support
- [x] Includes database model and route layer
- [x] Dockerized
- [x] Test coverage provided
- [x] Clear architectural documentation in `QA.md`

---

##  License

This project is created for technical evaluation purposes.

---

Feel free to fork and build upon it 🚀
