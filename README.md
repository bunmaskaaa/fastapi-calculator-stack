# FastAPI Calculator Stack

This project is a full-stack calculator application built using **FastAPI + PostgreSQL + JWT Auth + Playwright E2E tests**.  
Users can register, log in, perform arithmetic operations, and store their calculation history securely.

---

## 🚀 Tech Stack

| Component | Technology |
|---------|-------------|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Auth | JWT (python-jose), Passlib (bcrypt) |
| Database | PostgreSQL |
| Frontend | Static HTML + Fetch API |
| Testing | Pytest (backend) + Playwright (full E2E browser tests) |
| CI/CD | GitHub Actions + Docker Hub |
| Deployment | Docker container image |

---

## 🔑 Features

- User registration and login using JWT
- Password hashing with bcrypt
- Protected calculation API tied to logged-in user
- View stored calculation history
- Frontend pages: `/static/register.html`, `/static/login.html`, `/static/calculator.html`
- Full CI/CD pipeline:
  1. Start PostgreSQL service
  2. Run **pytest**
  3. Run **Playwright E2E tests**
  4. Build & push Docker image to Docker Hub if all tests pass

---

## 📦 Running Locally

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt