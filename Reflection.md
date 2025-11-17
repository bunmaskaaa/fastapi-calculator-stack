# Reflection – FastAPI, Docker, and PostgreSQL Integration

## Overview
This assignment taught me how to build a complete backend environment using **Docker Compose** to integrate a **FastAPI** web service with a **PostgreSQL** database and manage it through **pgAdmin**. Setting up these containers helped me understand how different services communicate within a virtualized environment and how containerization simplifies deployment.

---

## Key Learnings

1. **Containerization with Docker**
   - I learned how to use a `docker-compose.yml` file to define multiple services (FastAPI app, PostgreSQL, pgAdmin) and link them through a shared network.
   - Managing dependencies and ports through environment variables made setup reproducible and portable.

2. **Database Integration**
   - By connecting FastAPI to PostgreSQL via SQLAlchemy and psycopg2, I saw how backend services can interact with databases securely.
   - Writing SQL commands (CREATE, INSERT, SELECT, UPDATE, DELETE) in pgAdmin reinforced the concepts of relational databases and foreign keys.

3. **Service Networking**
   - Understanding that Docker Compose service names (like `db`) act as hostnames was crucial to connect pgAdmin and FastAPI with PostgreSQL.

4. **Practical SQL Application**
   - Executing SQL queries directly in pgAdmin gave me hands-on experience in managing one-to-many relationships and enforcing referential integrity between tables.

---

## Challenges & Solutions

- **Challenge:** pgAdmin initially failed to connect to PostgreSQL.
  - **Solution:** I used the Docker service name `db` as the hostname and verified environment variables in `docker-compose.yml`.
  
- **Challenge:** Docker daemon connection errors on macOS.
  - **Solution:** Restarted Docker Desktop, reset the context to `desktop-linux`, and verified connectivity with `docker version` and `docker info`.

- **Challenge:** Keeping multiple containers running consistently.
  - **Solution:** Used `depends_on` and checked logs with `docker compose logs` to debug service startup order.

---

## Workflow Reflection
Using **Git** and **GitHub** to manage this project made it easy to version control code and documentation. Each change was committed incrementally, allowing me to track my progress and maintain a clean history.  

Setting up Docker Compose and pgAdmin felt like working with a real-world development stack — the same process used in production-grade systems.

---

## Looking Ahead
In future projects, I plan to:
- Integrate automated database migrations using **Alembic**.
- Add **test automation** and continuous integration with **GitHub Actions**.
- Extend the FastAPI application to perform CRUD operations dynamically through endpoints instead of manual SQL queries.

---

**Student:** Hardik Rathod  
**Course:** Python for Web API Development  
**Date:** November 3, 2025